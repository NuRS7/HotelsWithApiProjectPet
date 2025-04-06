from datetime import date, datetime, timedelta
from typing import List

from fastapi import Query

from hotels.rooms.repository import RoomRepository
from hotels.rooms.shemas import SRoomInfo
from hotels.router import router


@router.get("/{hotel_id}/rooms")

async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SRoomInfo]:
    rooms = await RoomRepository.find_all(hotel_id, date_from, date_to)
    return rooms
