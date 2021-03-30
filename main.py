from typing import List
from datetime import datetime, timedelta
import time
import json

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from include.database import SessionLocal, engine
import include.models as models
from include.models import Temperature
from include.DS18B20 import DS18B20
from include.grove import Relay, WaterSensor

app = FastAPI()

# location of web service static files and html templates
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

models.Base.metadata.create_all(bind=engine)

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

pool_data = {
    'pool-pump': 'OFF',
    'pool-heater': 'OFF',
    'pool-temp': '40 ºF',
    'air-temp': '12 ºF',
    'water-valve': 'OFF',
    'water-level': '100%',
    'ph-level': '7',
    'orp-level': '650 mv'
}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    global pool_data
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            client, event = data.split(' ')
            print('Client: ' + client + '\tEvent: ' + event)
            if 'toggle' in event:
                toggle_event(event)
            await manager.broadcast(json.dumps(pool_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} exited.")

sched = BackgroundScheduler(daemon=True)
sched.start()

water_temp = DS18B20()
pool_pump = Relay(22)
pool_heater = Relay(23)
water_valve = Relay(24)
water_level = WaterSensor()

@sched.scheduled_job('interval', seconds=1)
def update_sensors():
    global pool_data

    pool_data['pool-temp'] = str(water_temp.read()) + ' ºF'
    pool_data['water-level'] = str(water_level.read()) + ' %'

@sched.scheduled_job('interval', start_date=str(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)), seconds=5)
def record_temp():
    db = SessionLocal()

    hour = Temperature()
    hour.time = datetime.now()
    hour.pool_temp = int(pool_data['pool-temp'].replace(' ºF', ''))
    hour.air_temp = int(pool_data['air-temp'].replace(' ºF', ''))

    db.add(hour)
    db.commit()
    db.refresh(hour)

    if db.query(Temperature).count() > 12:
        print('Too many')
        oldest = hour.time
    
        times = db.query(Temperature.time).all()
        for time in times:
            if time < oldest:
                oldest = time
        
        db.delete(db.query(Temperature).filter(Temperature.time==oldest).first())
        db.commit()

    db.close()
    return hour

def toggle_event(event: str):
    global pool_data, pool_pump
    if 'pool-pump' in event:
        pool_data['pool-pump'] = pool_pump.toggle()
    if 'pool-heater' in event:
        pool_data['pool-heater'] = pool_heater.toggle()
    if 'water-valve' in event:
        pool_data['water-valve'] = water_valve.toggle()
