from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings



engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine,_class=AsyncSession, expire_on_commit=False)


# Добавил новый класс чтобы в будущем поработать с миграцией и алеибик
class Base(DeclarativeBase):
    pass