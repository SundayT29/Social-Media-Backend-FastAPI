from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from .enums import Gender

class UserBase(BaseModel):
    email: str
    username: str
    name: str
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_pic: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_pic: Optional[str] = None

class User(UserBase):
    id: int
    created_dt: datetime

    class Config:
        from_attributes = True