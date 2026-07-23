from sqlalchemy import Column, Integer, String
from app.database.database import Base

class CrimeType(Base):
    __tablename__ = "crime_types"

    id = Column(Integer, primary_key=True, index=True)
    crime_name = Column(String, nullable=False)
    ipc_section = Column(String)
    description = Column(String)