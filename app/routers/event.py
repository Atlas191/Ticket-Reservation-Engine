from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.deps import get_current_user, require_admin
from app.models.tables import User
from app.schemas.data_models import EventCreate, EventOut, EventPage, SeatOut
from app.services.event_services import create_event,list_events,get_seat_map

router = APIRouter(prefix='/events',tags=['events'])


@router.post("",response_model=EventOut,status_code=201,description="Admin creates a event")
def create(body: EventCreate, db: Session = Depends(get_db), admin : User = Depends(require_admin)):
  return create_event(body,admin.id,db)


@router.get("",response_model=EventPage)
def list_all(skip: int =Query(0,ge=0),limit : int = Query(1,ge=1,le=100),db: Session = Depends(get_db),user:User = Depends(get_current_user)):
  return list_events(skip, limit, db)


@router.get("/{event_id}/seats",response_model=list[SeatOut])
def seat_map(event_id : int, db: Session = Depends(get_db), user : User = Depends(get_current_user)):
  return get_seat_map(event_id,db)