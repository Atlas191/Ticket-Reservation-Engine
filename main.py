from fastapi import FastAPI,Response,Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.redis_client import redis_client
from app.routers import auth
from app.models.tables import User
from app.deps import get_current_user,require_admin
App = FastAPI(title="Yayyyy")
App.include_router(auth.router)



@App.get('/health')
def health(response : Response, db : Session = Depends(get_db)):
  status = {'app': 'ok','db': 'ok','redis':'ok'}
  try:
    db.execute(text('SELECT 1'))
  except Exception as e:
    print("DB error:", e)
    status["db"] = "down"

  try:
    redis_client.ping()
  except:
    status['redis'] = 'down'

  if 'down' in status.values():
    response.status_code = 503
  return status

@App.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}

@App.get("/admin-only")
def admin_only(user: User = Depends(require_admin)):
    return {"ok": True}