import string
from fastapi import HTTPException,status
from sqlalchemy import select,func
from app.schemas.data_models import EventCreate
from sqlalchemy.orm import Session
from app.models.tables import Event,Seat



def create_event(body : EventCreate,admin_id : int,db : Session) -> Event:
  event = db.scalar(select(Event).where(func.lower(Event.name) == body.name.strip().lower()))
  if event:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="event with the name already exist")

  new_Event = Event(name = body.name.strip(), venue = body.venue, starts_at = body.starts_at,created_by = admin_id)

  db.add(new_Event)
  db.flush()

  seats = [
      Seat(event_id=new_Event.id, label=f"{row}{num}", price=body.price)
      for row in string.ascii_uppercase[:body.rows]
      for num in range(1, body.seats_per_row + 1)
        ]

  db.add_all(seats)
  db.commit()
  db.refresh(new_Event)
  return new_Event


def list_events(skip: int, limit: int, db: Session) -> dict:
  items = db.scalars(select(Event).order_by(Event.starts_at).offset(skip).limit(limit)).all()

  total = db.scalar(select(func.count()).select_from(Event))

  return {"items" : items,"total": total,"skip" : skip,"limit": limit}



def get_seat_map(event_id : int, db : Session) -> list[Seat]:
  event = db.get(Event,event_id)
  if event is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='event not found.....')

  return db.scalars(select(Seat).where(Seat.event_id == event_id).order_by(Seat.id)).all()



  
  