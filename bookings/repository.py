from database import async_session_maker
from sqlalchemy import select
from bookings.models import Bookings




class BookingRepository:
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(Bookings)
            bookings = await session.execute(query)
            return bookings.scalars().all()







