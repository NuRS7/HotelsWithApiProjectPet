from pydantic_settings import BaseSettings
from pydantic import model_validator

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: str = ""

    @model_validator(mode="after")
    def set_database_url(cls, values):
        values.DATABASE_URL = f"postgresql+asyncpg://{values.DB_USER}:{values.DB_PASS}@{values.DB_HOST}:{values.DB_PORT}/{values.DB_NAME}"
        return values


    SECRET_KEY: str
    ALGORITHM: str

    # Осы жерге .env данныйларды коямыз
    class Config:
        env_file = ".env"

settings = Settings()




# DATABASE_URL=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(settings.DATABASE_URL)
#python.exe .\config.py чекинг