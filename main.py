from dataclasses import Field

import fastapi
from fastapi import FastAPI, Query, Depends
from typing import Optional
from pydantic import BaseModel
from datetime import date


from bookings.router import router as booking_router
app = FastAPI()
app.include_router(booking_router)

class HotelsSearchArgs:
    def __init__(
            self,
            location:str,
            data_from: date,
            data_to: date,
            has_spa:Optional[bool] = None,
            stars:Optional[int] = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.data_from = data_from
        self.data_to = data_to
        self.has_spa = has_spa
        self.stars = stars



class SHotel(BaseModel):
    address: str
    name:str
    stars:int

@app.get("/hotels")
async def get_hotels(
        search_args:HotelsSearchArgs = Depends()
)-> list[SHotel]:
    hotels =[{
        "addres":"Туркестан Бекзат Саттарханов",
        "name":"MHotrl",
        "stars":5
    }]
    return search_args

class SBooking(BaseModel):
    room_id:int
    data_from: date
    data_to: date

@app.post("bookings")
async def add_booking(booking: SBooking):
    pass