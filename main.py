from typing import List
import time
import json

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from include.database import SessionLocal, engine
import include.models as models

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
    'pool-filter': 'ON',
    'pool-heater': 'OFF',
    'pool-temp': '40 ºF',
    'air-temp': '12 ºF',
    'water-valve': 'ON',
    'water-level': 'Low',
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
        await manager.broadcast(f"Client #{client_id} left the chat")

sched = BackgroundScheduler(daemon=True)
sched.start()

temp = 0
@sched.scheduled_job('interval', seconds=5)
def update_sensors():
    global pool_data, temp
    temp = temp + 1
    pool_data['pool-temp'] = str(temp) + 'ºF'

def toggle_event(event: str):
    global pool_data
    if 'pool-filter' in event:
        if pool_data['pool-filter'] == 'OFF':
            pool_data['pool-filter'] = 'ON'
        else:
            pool_data['pool-filter'] = 'OFF'
    if 'pool-heater' in event:
        if pool_data['pool-heater'] == 'OFF':
            pool_data['pool-heater'] = 'ON'
        else:
            pool_data['pool-heater'] = 'OFF'
    if 'water-valve' in event:
        if pool_data['water-valve'] == 'OFF':
            pool_data['water-valve'] = 'ON'
        else:
            pool_data['water-valve'] = 'OFF'