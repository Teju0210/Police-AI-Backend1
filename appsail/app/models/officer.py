from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    officer_name = Column(String, nullable=False)
    badge_number = Column(String, unique=True)
    rank = Column(String)
    police_station = Column(String)
    contact_number = Column(String)
    phone = Column(String)