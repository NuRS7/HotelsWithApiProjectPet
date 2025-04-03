from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_HOST="localhost"
DB_PORT=5433
DB_USER="posgres"
DB_PASS="Nursultan321n"
DB_NAME="hotels"

DATABASE_URL=f"postgresql+asyncpg"
engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine,_class_=AsyncSession, expire_on_commit=False)