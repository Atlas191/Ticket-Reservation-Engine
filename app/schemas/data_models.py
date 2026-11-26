from typing import Literal
from pydantic import BaseModel, EmailStr, Field,ConfigDict
from datetime import datetime
from decimal import Decimal

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Literal["user", "admin"]

    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class EventCreate(BaseModel):
    name : str = Field(min_length=5, max_length=100)
    venue : str = Field(min_length=10, max_length=150)
    starts_at : datetime
    rows : int = Field(ge=1, le=20)
    seats_per_row : int = Field(ge=5,le=50)
    price : Decimal = Field(gt=10,max_digits=10,decimal_places=2)


class EventOut(BaseModel):
    id : int
    name : str
    venue : str
    starts_at : datetime

    model_config = ConfigDict(from_attributes=True)

class EventPage(BaseModel):
    items : list[EventOut]
    total : int
    skip : int
    limit : int

class SeatOut(BaseModel):
    id : int
    label : str
    price : Decimal
    status : str

    model_config = ConfigDict(from_attributes=True)

class HoldIn(BaseModel):
    seat_ids : list[int] = Field(min_length=1, max_length=6)

class BookingOut(BaseModel):
    id: int
    event_id : int
    status : str
    total_amount : Decimal
    expires_at : datetime

    model_config = ConfigDict(from_attributes= True)

