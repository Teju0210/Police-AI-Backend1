from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    police_station = Column(String, nullable=False)
    area = Column(String)
    pincode = Column(String)