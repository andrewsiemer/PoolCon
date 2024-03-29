import time, json, threading
from typing import List
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from include.database import SessionLocal, engine
import include.models as models
import include.crud as crud
from include.components import Relay, WaterSensor, DS18B20, DHT11, PHsensor, ORPsensor
from include.chartjs import PumpGraph, TempGraph

app = FastAPI() # define application

# location of web service static files and html templates
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

models.Base.metadata.create_all(bind=engine)

# task scheduler
sched = BackgroundScheduler(daemon=True)
sched.start()

# components definition
pool_pump = Relay(2)
pool_heater = Relay(3)
water_temp = DS18B20()
air_temp = DHT11(8)
water_valve = Relay(4)
water_level = WaterSensor()
ph_sensor = PHsensor(0)
orp_sensor = ORPsensor(1)
pump_chart = PumpGraph()
pump_chart.labels.grouped, pump_chart.data.PumpUsage.data = crud.get_pump_chart_data()
temp_chart = TempGraph()
temp_chart.labels.grouped, temp_chart.data.PoolTemperature.data, temp_chart.data.AirTemperature.data = crud.get_temp_chart_data()

updating = False

# data structure
pool_data = {
    'time': str(datetime.now().strftime('%A, %B %-d, %-H:%M %p')),
    'pool-pump': 'OFF',
    'pool-heater': 'OFF',
    'pool-temp': str(round(water_temp.read())) + ' ºF',
    'air-temp': str(round(air_temp.read_temp())) + ' ºF',
    'water-valve': 'OFF',
    'water-level': str(water_level.read()) + ' %',
    'ph-level': str(round(ph_sensor.read())),
    'orp-level': str(round(orp_sensor.read())) + ' mV',
    'pump-chart': '', #pump_chart.get(),
    'temp-chart': temp_chart.get(),
    'schedule-tbl': '',
    'schedule-opt': '',
    'pump-time': '...',
    'heater-time': '...',
    'water-time': '...'
}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
def home(request: Request):
    '''
    Returns dashboard endpoint
    '''
    return templates.TemplateResponse('index.html', { 'request': request })

@app.post("/add")
async def add(request: Request, equipment: str = Form(...), start_time: str = Form(...) , end_time: str = Form(...)):
    '''
    Add a scheduled event
    '''
    global sched
    start_datetime = datetime.strptime(start_time, '%I:%M %p')
    end_datetime = datetime.strptime(end_time, '%I:%M %p')

    if start_datetime < end_datetime and not crud.get_event_id(equipment, start_datetime, end_datetime):
        crud.add_event(equipment, start_datetime, end_datetime)
        event_id = crud.get_event_id(equipment, start_datetime, end_datetime)
        
        sched.add_job(control_relay, 'cron', hour=start_datetime.strftime('%-H'), minute=start_datetime.strftime('%-M'), args=[equipment,'ON'], id=str(event_id)+'_ON')
        sched.add_job(control_relay, 'cron', hour=end_datetime.strftime('%-H'), minute=end_datetime.strftime('%-M'), args=[equipment,'OFF'], id=str(event_id)+'_OFF')
        update_schedule()
    else:
        print('Invalid time range.')
    
    return templates.TemplateResponse('index.html', { 'request': request })

# control relay from a scheduled event
def control_relay(equipment, state):
    if 'Pool Pump' in equipment:
        if state == 'ON':
            pool_pump.on()
            pool_data['pool-pump'] = state
            crud.add_status('pool-pump', state)
        else:
            pool_pump.off()
            pool_data['pool-pump'] = state
            crud.add_status('pool-pump', state)
    elif 'Pool Heater' in equipment:
        if state == 'ON':
            pool_heater.on()
            pool_data['pool-heater'] = state
            if pool_data['pool-pump'] == 'OFF':
                pool_pump.on()
                pool_data['pool-pump'] = state
                crud.add_status('pool-pump', state)
        else:
            pool_heater.off()
            pool_data['pool-heater'] = state
    elif 'Water Valve' in equipment:
        if state == 'ON':
            water_valve.on()
            pool_data['pool-pump'] = state
            crud.add_status('pool-pump', state)
        else:
            water_valve.off()
            pool_data['pool-pump'] = state
            crud.add_status('pool-pump', state)

@app.post("/remove")
def remove(request: Request, event_id: str = Form(...)):
    '''
    Remove a scheduled event
    '''
    global sched
    crud.remove_event(event_id)

    sched.remove_job(str(event_id)+'_ON')
    sched.remove_job(str(event_id)+'_OFF')
    update_schedule()

    return templates.TemplateResponse('index.html', { 'request': request })

@app.post("/delete")
def delete(request: Request):
    '''
    Delete all scheduled events
    '''
    global sched
    jobs = crud.get_event_list()

    for event_id in jobs:
        crud.remove_event(event_id)
        
        sched.remove_job(str(event_id)+'_ON')
        sched.remove_job(str(event_id)+'_OFF')

    update_schedule()
    return templates.TemplateResponse('index.html', { 'request': request })

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    '''
    Client WebSocket function
    '''
    global pool_data
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            client, event = data.split(' ')
            print('Client: ' + client + '\tEvent: ' + event)
            if 'toggle' in event:
                toggle_event(event)
            elif 'load-schedule' in event:
                pool_data['schedule-opt'] = crud.get_schedule_options()
            await manager.broadcast(json.dumps(pool_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} exited.")

@sched.scheduled_job('interval', start_date=str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)),seconds=5, max_instances=3)
def start_update_thread():
    '''
    Starts a thread to update component readings
    '''
    global updating
    x = threading.Thread(target=update_sensors)
    updating = True
    x.start()
    x.join()
    updating = False

# fetches updates from all components
def update_sensors():
    global pool_data
    pool_data['time'] = str(datetime.now().strftime('%A, %B %-d, %-I:%M %p'))
    pool_data['pool-temp'] = str(round(water_temp.read())) + ' ºF'
    pool_data['air-temp'] = str(round(air_temp.read_temp())) + ' ºF'
    pool_data['water-level'] = str(water_level.read()) + ' %'
    pool_data['ph-level'] = str(round(ph_sensor.read()))
    pool_data['orp-level'] = str(round(orp_sensor.read())) + ' mV'
    #pool_data['pump-chart'] = pump_chart.get()
    pool_data['temp-chart'] = temp_chart.get()
    pool_data['schedule-tbl'] = crud.get_schedule_table()
    pool_data['pump-time'] = str(round(pool_pump.stopwatch.duration) // 3600) + ' hr ' + str((round(pool_pump.stopwatch.duration) % 3600) // 60) + ' mins ' + str(round(pool_pump.stopwatch.duration) % 60) + ' secs'
    pool_data['heater-time'] = str(round(pool_heater.stopwatch.duration) // 3600) + ' hr ' + str((round(pool_heater.stopwatch.duration) % 3600) // 60) + ' mins ' + str(round(pool_heater.stopwatch.duration) % 60) + ' secs'
    pool_data['water-time'] = str(round(water_valve.stopwatch.duration) // 3600) + ' hr ' + str((round(water_valve.stopwatch.duration) % 3600) // 60) + ' mins ' + str(round(water_valve.stopwatch.duration) % 60) + ' secs'

# fetches the schedule for the UI table
def update_schedule():
    global pool_data
    pool_data['schedule-tbl'] = crud.get_schedule_table()

# handles toggle event for the relays
def toggle_event(event: str):
    global pool_data, pool_pump, updating
    while updating:
        time.sleep(0.1)
    
    if not updating:
        updating = True
    if 'pool-pump' in event:
        status = pool_pump.toggle()
        pool_data['pool-pump'] = status
        crud.add_status('pool-pump', status)
    if 'pool-heater' in event:
        status = pool_heater.toggle()
        if status == 'ON' and pool_data['pool-pump'] == 'OFF':
            pool_data['pool-pump'] = pool_pump.toggle()
            crud.add_status('pool-pump', status)
        pool_data['pool-heater'] = status
    if 'water-valve' in event:
        pool_data['water-valve'] = water_valve.toggle()
    updating = False

@sched.scheduled_job('interval', start_date=str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)), seconds=5, max_instances=1)
def record_temp():
    '''
    Records the current temperatures to the db and updates UI temperature chart
    '''
    pool_temp = int(pool_data['pool-temp'].replace(' ºF', ''))
    air_temp = int(pool_data['air-temp'].replace(' ºF', ''))

    crud.add_temp(pool_temp, air_temp)

    temp_chart.labels.grouped, temp_chart.data.PoolTemperature.data, temp_chart.data.AirTemperature.data = crud.get_temp_chart_data()

@app.on_event("shutdown")
def shutdown_event():
    '''
    Global shutdown function
    '''
    global sched
    sched.shutdown()

# import scheduled events from db on startup
jobs = crud.get_event_list()
for event_id in jobs:
    event = crud.get_event(event_id)
    sched.add_job(control_relay, 'cron', hour=event.start_time.strftime('%-H'), minute=event.start_time.strftime('%-M'), args=[event.equipment,'ON'], id=str(event_id)+'_ON')
    sched.add_job(control_relay, 'cron', hour=event.end_time.strftime('%-H'), minute=event.end_time.strftime('%-M'), args=[event.equipment,'OFF'], id=str(event_id)+'_OFF')