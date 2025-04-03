from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASS:str
    DB_NAME:str

# Осы жерге .env данныйларды коямыз
    class Config:
        env_file = '.env'
settings = Settings()

print(settings.DB_HOST)

#python.exe .\config.py чекинг