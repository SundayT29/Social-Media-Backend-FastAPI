from sqlalchemy import Enum, ForeignKey, Integer, String, DateTime, Column, Date
from datetime import datetime, timedelta
from database import Base
from .enums import Gender

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    created_dt = Column(DateTime, default=datetime.utcnow())
    dob = Column(Date)
    gender = Column(Enum(Gender))
    profile_pic = Column(String)
    bio = Column(String(100))
    location = Column(String(100))
