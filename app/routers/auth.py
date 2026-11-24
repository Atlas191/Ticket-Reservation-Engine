from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.data_models import UserOut,RegisterIn,TokenOut
from sqlalchemy.orm import Session
from sqlalchemy import  select
from app.models.tables import User
from app.core.security import hash_password,verify_password,create_access_token
from app.db.session import get_db
from app.services.auth_services import register_user,authenticate

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post('/register',response_model=UserOut,status_code=201)
def register(body : RegisterIn,db : Session = Depends(get_db)):
  return register_user(body.email,body.password,db)

@router.post('/login',response_model=TokenOut)
def login(form : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
  user = authenticate(form.username,form.password,db)
  token = create_access_token(user.id,user.role)
  return TokenOut(access_token=token)