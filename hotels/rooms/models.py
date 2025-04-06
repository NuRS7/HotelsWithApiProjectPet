from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base



#model Room
class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id=Column(Integer,ForeignKey('hotels.id', ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services=Column(JSON, nullable=False)
    quantity=Column(Integer, nullable=False)
    image_id=Column(Integer, nullable=False)

    hotel = relationship("Hotels", back_populates="rooms")
    booking = relationship("Bookings", back_populates="room")



    def __str__(self):
        return f"Номер {self.name}"