from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy import Float, Text


class FIR(Base):
    __tablename__ = "firs"

    id = Column(Integer, primary_key=True, index=True)
    fir_number = Column(String, unique=True)
    crime_type_id = Column(Integer, ForeignKey("crime_types.id"))
    police_station_id = Column(Integer, ForeignKey("police_stations.id"))
    location = Column(String)
    incident_date = Column(Date)
    status = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    crime_description = Column(Text)

    year = Column(Integer)
    month = Column(Integer)
    case_category = Column(String)
    gravity_offence = Column(String)
    crime_sub_head = Column(String)

    victims = relationship("Victim", back_populates="fir")
    accused = relationship("Accused", back_populates="fir")
    arrest_surrenders = relationship("ArrestSurrender", back_populates="fir")