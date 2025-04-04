from bookings.repository import BookingRepository
from fastapi import APIRouter
from bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingRepository.find_by_id(1)




