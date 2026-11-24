from sqlalchemy.orm import Session
from sqlalchemy import  select
from fastapi import Depends,HTTPException,status
from app.db.session import get_db
from app.models.tables import User
from app.core.security import hash_password,verify_password



def register_user(email : str, password:str, db: Session) -> User:
  exisiting = db.scalar(select(User).where(User.email == email))
  if exisiting:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Email already exist')

  new_user = User(email = email,password_hash = hash_password(password))

  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


def authenticate(email : str, password:str, db: Session) -> User:
  user = db.scalar(select(User).where(User.email == email))
  """
  db.scalar(select(...)) runs the query and returns the first row, or None. It replaces your execute plus scalar_one_or_none pair.
  """

  if user is None or not verify_password(password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
    )
  return user