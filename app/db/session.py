from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,expire_on_commit=False)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()