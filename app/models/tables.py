from app.db.base import Base
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime,func,String,ForeignKey,JSON,Numeric,Index,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship



class User(Base):

  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True)
  email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
  password_hash : Mapped[str] = mapped_column(String(300),nullable=False)
  role : Mapped[str] = mapped_column(String(20),default='user')
  created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())


class Event(Base):

  __tablename__ = 'events'
  __table_args__ = (
        UniqueConstraint("name", "venue", "starts_at", name="uq_event_name_venue_start"),
    )

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(100),nullable=False)
  venue : Mapped[str] = mapped_column(String(150),nullable=False)
  starts_at : Mapped[datetime] = mapped_column(DateTime(timezone=True))
  created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
  created_by : Mapped[int] = mapped_column(ForeignKey("users.id"))

  seats : Mapped[list["Seat"]] = relationship(back_populates='event',cascade='all, delete-orphan')

class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint("event_id", "label", name="uq_seat_event_label"),
        Index("ix_seats_event_status", "event_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    label: Mapped[str] = mapped_column(String(10))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(20), default="AVAILABLE")
    booking_id: Mapped[int | None] = mapped_column(ForeignKey("bookings.id"), nullable=True)
    hold_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    event: Mapped["Event"] = relationship(back_populates="seats")


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        Index("ix_bookings_user_created", "user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    status: Mapped[str] = mapped_column(String(20), default="HELD")
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    payment_ref: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class WebhookEvent(Base):

  __tablename__ = 'webhook_events'
  id : Mapped[int] = mapped_column(primary_key=True)
  provider_event_id : Mapped[str] = mapped_column(String(100),unique=True)
  payload : Mapped[dict] = mapped_column(JSON)
  received_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
