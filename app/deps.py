import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.tables import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
  token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> User:
    try:
      payload = decode_access_token(token)
      user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
      raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get(User, user_id)
    
    if user is None:
      raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
      raise HTTPException(status_code=403, detail="Admin only")
    return user