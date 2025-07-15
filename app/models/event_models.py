from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime

class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = Field(None, max_length=200)
    attendees: List[EmailStr]

    @validator('end_datetime')
    def check_datetime_order(cls, v, values):
        start = values.get('start_datetime')
        if start and v <= start:
            raise ValueError('end_datetime must be after start_datetime')
        return v

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    location: Optional[str] = Field(None, max_length=200)
    attendees: Optional[List[EmailStr]]

    @validator('end_datetime')
    def check_datetime_order(cls, v, values):
        start = values.get('start_datetime')
        if start and v and v <= start:
            raise ValueError('end_datetime must be after start_datetime')
        return v

class Event(EventBase):
    id: int

class ErrorResponse(BaseModel):
    detail: str
