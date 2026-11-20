from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env',extra='ignore')

  database_url : str
  redis_url : str
  webhook_secret : str
  jwt_secret : str
  hold_minutes : int

settings = Settings()




