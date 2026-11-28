import asyncio
from app.db.session import SessionLocal
from datetime import datetime,timezone
from sqlalchemy import select
from app.models.tables import Booking,Seat

def clean_once() -> int:
  db = SessionLocal()
  try:
    now = datetime.now(timezone.utc)
    exp_bookings = db.scalars(select(Booking).where(Booking.status == 'HELD', Booking.expires_at < now).with_for_update(skip_locked=True)).all()

    for b in exp_bookings:
      seats = db.scalars(select(Seat).where(Seat.booking_id == b.id, Seat.status == 'HELD').order_by(Seat.id).with_for_update()).all()
      
      for seat in seats:
        seat.status = 'AVAILABLE'
        seat.booking_id = None
        seat.hold_expires_at = None
  
      b.status = "EXPIRED"
  
    db.commit()

    return len(exp_bookings)
  finally:
    db.close()


async def run_cleaner(interval : int = 30):
  while True:
    try:
      count = await asyncio.to_thread(clean_once)
      if count:
        print(f"sweeper: expired {count} bookings")
    except Exception as e:
        print("sweeper error:", e)
    await asyncio.sleep(interval)

