from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from database import Base

# Модель hotel
class Hotels(Base):
    __tablename__ = 'hotels'

    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    location=Column(String, nullable=False)
    services=Column(JSON)
    room_quantity=Column(Integer, nullable=False)
    image_id=Column(Integer)



#model Room
class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id=Column(Integer, ForeignKey('hotels.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services=Column(JSON, nullable=False)
    quantity=Column(Integer, nullable=False)
    image_id=Column(Integer)



