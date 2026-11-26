from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.tables import Seat,Booking,Event
from datetime import datetime,timezone,timedelta
from app.core.config import settings



def hold_seats(event_id : int, seat_ids : list[int], user_id : int, db : Session) -> Booking:
  ids = sorted(set(seat_ids))
  event = db.get(Event,event_id)

  if event is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='There is no such event')

  stmt = (select(Seat).where(Seat.id.in_(ids),Seat.event_id == event_id)
        .order_by(Seat.id).with_for_update())
  
  seats = db.scalars(stmt).all()

  if(len(seats) != len(ids)):
    db.rollback()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Seats not Availabe in the event')

  now = datetime.now(timezone.utc)
  for seat in seats:
    holdable = seat.status == "AVAILABLE" or (seat.status == 'HELD' and seat.hold_expires_at < now)
    if not holdable:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= 'Seat not Available')
    

  expire_at_time = now + timedelta(minutes=settings.hold_minutes)

  total =0
  for seat in seats:
    total += seat.price

  new_booking = Booking(user_id = user_id, event_id = event_id,total_amount = total,status = 'HELD',expires_at = expire_at_time)

  db.add(new_booking)
  db.flush()

  for seat in seats:
    seat.status = "HELD"
    seat.booking_id = new_booking.id
    seat.hold_expires_at = expire_at_time

  db.commit()
  db.refresh(new_booking)
  return new_booking
      