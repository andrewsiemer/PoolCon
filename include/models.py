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