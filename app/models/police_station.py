from sqlalchemy import Column, Integer, String
from app.database.database import Base

class PoliceStation(Base):
    __tablename__ = "police_stations"

    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String, nullable=False)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, default="Karnataka")