from bookings.repository import BookingRepository
from fastapi import APIRouter


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings():
    return await BookingRepository.find_all()




