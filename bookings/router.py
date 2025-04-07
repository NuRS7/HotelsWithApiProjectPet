from bookings.repository import BookingRepository
from fastapi import APIRouter, Request, Depends
from bookings.schemas import SBooking, SNewBooking
from users.dependencies import get_current_user
from users.models import Users
from exceptions import RoomCannotBeBooked
from fastapi_versioning import version

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingRepository.find_all(user_id=user.id)


#     print(request.cookies)
#     print(request.headers)
#     print(request.url)
#     print(request.client)
# {'csrftoken': 'hiGEuYKezMc4pRWJh6p6mtrK6BvgvZEF', 'sessionid': '1os1lwv21eq812d9u6atk0wvm1i9zr5w'}
# Headers({'host': '127.0.0.1:8000', 'connection': 'keep-alive', 'sec-ch-ua-platform': '"Windows"', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple
# WebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'accept': 'application/json', 'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google
#  Chrome";v="134"', 'sec-ch-ua-mobile': '?0', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'http://127.0.0.1:
# 8000/docs', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9,ru;q=0.8', 'cookie': 'csrftoken=hiGEuYKezMc4pRWJh6p6mtrK6BvgvZEF; sessionid=1os1lwv21eq812d9u6atk0wvm1i9zr5w'})
# http://127.0.0.1:8000/bookings


@router.post("")
@version(2)
async def add_booking(booking: SNewBooking, user: Users = Depends(get_current_user)):
    await BookingRepository.add(
        user.id, booking.room_id, booking.date_from, booking.date_to
    )
    if not booking:
        raise RoomCannotBeBooked

    return booking


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingRepository.delete(id=booking_id, user_id=current_user.id)
