'''
crud.py: Reusable functions to interact with the data in the database.
CRUD comes from: Create, Read, Update, and Delete.
'''

from datetime import datetime, timedelta

from sqlalchemy import func

from include.database import SessionLocal
import include.models as models
from include.models import Temperature, Status

def get_temp_chart_data():
    db = SessionLocal()
    labels = []
    pool = []
    air = []

    entries = db.query(Temperature.timestamp).all()
    for i in entries:
        print(type(i[0]))
        labels.append(i[0].strftime('%-H %p'))
        entry = db.query(Temperature).filter(Temperature.timestamp==i[0]).first()
        pool.append(entry.pool_temp)
        air.append(entry.air_temp)
    
    db.close()

    return labels, pool, air

def get_pump_chart_data():
    db = SessionLocal()
    labels = []
    pump = []

    # for hour in range(0,24):
    #     events = db.query(Status).filter(Status.equipment=='pool-pump', int(Status.timestamp.strftime('%-H'))==hour).all()
    #     for event in events:
    #         print(event.timestamp)
    #         print(event.status)
    
    db.close()

    return labels, pump

def add_temp(pool_temp, air_temp):
    db = SessionLocal()

    entry = Temperature()
    entry.timestamp = datetime.now()
    entry.pool_temp = pool_temp
    entry.air_temp = air_temp

    db.add(entry)
    db.commit()
    db.refresh(entry)

    while db.query(Temperature).count() > 24:
        result = db.query(Temperature,func.min(Temperature.timestamp))
        db.delete(db.query(Temperature).filter(Temperature.timestamp==result[0][1]).first())
    
    db.commit()
    db.close()

def add_status(equipment, status):
    db = SessionLocal()
    now = datetime.now()

    entry = Status()
    entry.timestamp = now
    entry.equipment = equipment
    entry.status = status

    db.add(entry)
    db.commit()
    db.refresh(entry)

    entries = db.query(Status.timestamp).all()
    for i in entries:
        if i[0] < now - timedelta(days=1):
            db.delete(db.query(Status).filter(Status.timestamp==i[0]).first())
    
    db.commit()
    db.close()