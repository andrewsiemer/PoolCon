import time, json
from typing import List
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from include.database import SessionLocal, engine
import include.models as models
import include.crud as crud
from include.components import Relay, WaterSensor, DS18B20, DHT11, PHsensor, ORPsensor
from include.chartjs import LineGraph

app = FastAPI()

# location of web service static files and html templates
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

models.Base.metadata.create_all(bind=engine)

# task scheduler
sched = BackgroundScheduler(daemon=True, max_instances=3)
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
pump_chart = LineGraph()
pump_chart.labels.grouped, pump_chart.data.PumpUsage.data = crud.get_pump_chart_data()
temp_chart = LineGraph()
temp_chart.labels.grouped, temp_chart.data.PoolTemperature.data, temp_chart.data.AirTemperature.data = crud.get_temp_chart_data()

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
    'schedule-table': '',
    'schedule-opt': ''
}

def get_db():
    '''
    Create database session
    '''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

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
    return templates.TemplateResponse('index.html', { 'request': request })

@app.get("/add")
async def add(request: Request):
    json_param = await request.json()
    print(json_param)

    # start_datetime = datetime.strptime(start_time, '%I:%M %p')
    # end_datetime = datetime.strptime(end_time, '%I:%M %p')

    # if start_datetime < end_datetime:
    #     crud.add_event(equipment, start_datetime, end_datetime)
    #     event_id = crud.get_event_id(equipment, start_datetime, end_datetime)
        
    #     sched.add_job(control_relay, 'cron', hour=start_datetime.strftime('%-H'), minute=start_datetime.strftime('%-M'), args=[equipment,'ON'], id=str(event_id)+'_ON')
    #     sched.add_job(control_relay, 'cron', hour=end_datetime.strftime('%-H'), minute=end_datetime.strftime('%-M'), args=[equipment,'OFF'], id=str(event_id)+'_OFF')
    # else:
    #     print('Invalid time range.')

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

@app.delete("/remove")
def remove(request: Request, job: str = Form(...)):
    parse = job.partition(', ')
    print(parse)
    equipment = parse[0]
    start_time, sep, end_time = parse[2].partition(' - ')

    start_datetime = datetime.strptime(start_time, '%I:%M %p')
    end_datetime = datetime.strptime(end_time, '%I:%M %p')

    event_id = crud.get_event_id(equipment, start_datetime, end_datetime)
    crud.remove_event(event_id)

    sched.remove_job(str(event_id)+'_ON')
    sched.remove_job(str(event_id)+'_OFF')

@app.delete("/delete")
def delete(request: Request):
    jobs = crud.get_event_list()

    for event_id in jobs:
        sched.remove_job(str(event_id)+'_ON')
        sched.remove_job(str(event_id)+'_OFF')

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    global pool_data
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            client, event = data.split(' ')
            print('Client: ' + client + '\tEvent: ' + event)
            if 'status-update' in event:
                update_sensors()
            elif 'toggle' in event:
                toggle_event(event)
            elif 'load-schedule' in event:
                pool_data['schedule-opt'] = crud.get_schedule_options()
            await manager.broadcast(json.dumps(pool_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} exited.")

def update_sensors():
    global pool_data

    pool_data['time'] = str(datetime.now().strftime('%A, %B %-d, %-H:%M %p'))
    pool_data['pool-temp'] = str(round(water_temp.read())) + ' ºF'
    pool_data['air-temp'] = str(round(air_temp.read_temp())) + ' ºF'
    pool_data['water-level'] = str(water_level.read()) + ' %'
    pool_data['ph-level'] = str(round(ph_sensor.read()))
    pool_data['orp-level'] = str(round(orp_sensor.read())) + ' mV'
    pool_data['pump-chart'] = '', #pump_chart.get()
    pool_data['temp-chart'] = temp_chart.get()
    pool_data['schedule-table'] = crud.get_schedule_table()

def toggle_event(event: str):
    global pool_data, pool_pump
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

@sched.scheduled_job('interval', start_date=str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)), minutes=1)
def record_temp():
    update_sensors()
    
    pool_temp = int(pool_data['pool-temp'].replace(' ºF', ''))
    air_temp = int(pool_data['air-temp'].replace(' ºF', ''))
    crud.add_temp(pool_temp, air_temp)

    temp_chart.labels.grouped, temp_chart.data.PoolTemperature.data, temp_chart.data.AirTemperature.data = crud.get_temp_chart_data()

@app.on_event("shutdown")
def shutdown_event():
    global sched
    sched.shutdown()