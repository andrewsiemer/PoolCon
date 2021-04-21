'''
models.py: Create SQLAlchemy models from the Base class
'''

from sqlalchemy import Column, Integer, String, DateTime

from include.database import Base

class Temperature(Base):
    __tablename__ = "temperature"

    timestamp = Column(DateTime, primary_key=True, index=True) 
    pool_temp = Column(Integer)
    air_temp = Column(Integer)

class Status(Base):
    __tablename__ = "status"

    timestamp = Column(DateTime, primary_key=True, index=True) 
    equipment = Column(String)
    status = Column(String)

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True) 
    equipment = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)