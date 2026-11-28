from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.deps import get_current_user
from app.models.tables import User
from app.schemas.data_models import BookingOut
from app.services.booking_services import cancel_booking

router = APIRouter(prefix="/bookings",tags=['Bookings'])

@router.delete("/{booking_id}",response_model=BookingOut)
def cancel(booking_id : int, db : Session = Depends(get_db), user : User = Depends(get_current_user)):
  return cancel_booking(booking_id,user.id,db)