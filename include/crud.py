'''
crud.py: Reusable functions to interact with the data in the database.
CRUD comes from: Create, Read, Update, and Delete.
'''

from datetime import datetime, timedelta

from sqlalchemy import func

from include.database import SessionLocal
import include.models as models
from include.models import Temperature, Status, Schedule

def get_temp_chart_data():
    db = SessionLocal()
    labels = []
    pool = []
    air = []

    entries = db.query(Temperature.timestamp).all()
    length = len(entries) - 1
    for i in range(0,24):
        labels.append(entries[length - i][0].strftime('%-I:%M %p'))
        entry = db.query(Temperature).filter(Temperature.timestamp==entries[length - i][0]).first()
        
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

    # while db.query(Temperature).count() > 24:
    #     print('herre')
    #     result = db.query(Temperature,func.min(Temperature.timestamp))
    #     db.delete(db.query(Temperature).filter(Temperature.timestamp==result[0][1]).first())

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

def get_schedule_table():
    db = SessionLocal()
    table = ''

    entries = db.query(Schedule.id).all()
    for id in entries:
        entry = db.query(Schedule).filter(Schedule.id==id[0]).first()
        table += '<tr role="row"><td class="sorting_1">' + entry.equipment + '</td><td>' + entry.start_time.strftime('%-I:%M %p') + '</td><td>' + entry.end_time.strftime('%-I:%M %p') + '</td></tr>'

    db.close()

    return table

def get_schedule_options():
    db = SessionLocal()
    options = ''

    entries = db.query(Schedule.id).all()
    for id in entries:
        entry = db.query(Schedule).filter(Schedule.id==id[0]).first()
        options += '<option value=' + str(entry.id) + '>' + entry.equipment + ', ' + entry.start_time.strftime('%-I:%M %p') + ' - ' + entry.end_time.strftime('%-I:%M %p') + '</option>'

    db.close()

    return options

def get_event(event_id):
    db = SessionLocal()
    event = db.query(Schedule).filter(Schedule.id==event_id).first()
    db.close()
    return event

def get_event_id(equipment, start_time, end_time):
    db = SessionLocal()
    ret = db.query(Schedule).filter(Schedule.equipment==equipment,Schedule.start_time==start_time,Schedule.end_time==end_time).first()
    if ret:
        ret = ret.id
    db.close()
    return ret

def get_next_id():
    db = SessionLocal()
        
    last = db.query(Schedule,func.max(Schedule.id))
    if last[0][1]:
        result = last[0][1] + 1
    else:
        result = 1

    return result

def get_event_list():
    db = SessionLocal()
    ids = []
    
    entries = db.query(Schedule.id).all()
    for entry in entries:
        ids.append(entry[0])

    db.close()
    return ids

def add_event(equipment, start_time, end_time):
    db = SessionLocal()

    entry = Schedule()
    entry.id = get_next_id()
    entry.equipment = equipment
    entry.start_time = start_time
    entry.end_time = end_time

    db.add(entry)
    db.commit()
    db.close()

def remove_event(event_id):
    db = SessionLocal()

    db.delete(db.query(Schedule).filter(Schedule.id==event_id).first())
    
    db.commit()
    db.close()

def delete_schedule():
    db = SessionLocal()

    entries = db.query(Schedule.id).all()
    for entry in entries:
        db.delete(db.query(Schedule).filter(Schedule.id==entry.id).first())
    
    db.commit()
    db.close()