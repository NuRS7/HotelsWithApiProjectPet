from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from database import Base

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    # принципе бағаларды есептеуге болатын алгоритмді қосуға болады
    # жалпы оны фронтта қосады бірақ бэкендтеде қосуға болады
    total_cost=Column(Integer, Computed("(date_to-date_from)*price"))
    total_days=Column(Integer, Computed("date_to-date_from"))

