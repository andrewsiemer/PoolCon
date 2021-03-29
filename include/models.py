'''
models.py: Create SQLAlchemy models from the Base class
'''

from sqlalchemy import Column, Integer, String, DateTime

from include.database import Base

class Schedule(Base):
    __tablename__ = "schedule"

    device_id = Column(String, primary_key=True, index=True) # device library identifier
    push_token = Column(String)
