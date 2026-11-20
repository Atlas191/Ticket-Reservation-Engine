from fastapi import FastAPI,Response,Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.redis_client import redis_client

App = FastAPI(title="Yayyyy")

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