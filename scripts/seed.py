from datetime import datetime, timedelta, timezone
from decimal import Decimal

from app.db.session import SessionLocal
from app.models.tables import User, Event, Seat


def seed():
  db = SessionLocal()
  try:
      admin = User(
          email="admin@example.com",
          password_hash="placeholder",
          role="admin",
      )
      db.add(admin)
      db.flush()

      event = Event(
        name="Coldplay Live",
        venue="DY Patil Stadium, Mumbai",
        starts_at=datetime.now(timezone.utc) + timedelta(days=30),
        created_by=admin.id,
      )
      db.add(event)
      db.flush()

      seats = [
        Seat(event_id=event.id, label=f"{row}{num}", price=Decimal("500.00"))
        for row in "ABCDEFGHIJ"
        for num in range(1, 11)
      ]
      db.add_all(seats)

      db.commit()
      print(f"Seeded 1 admin, 1 event, {len(seats)} seats")
  finally:
    db.close()


if __name__ == "__main__":
    seed()