from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class ArrestSurrender(Base):
    __tablename__ = "arrest_surrender"

    id = Column(Integer, primary_key=True, index=True)

    fir_id = Column(Integer, ForeignKey("firs.id"))

    accused_master_id = Column(Integer)

    arrest_surrender_type_id = Column(String)

    arrest_surrender_date = Column(Date)

    district = Column(String)

    fir = relationship("FIR", back_populates="arrest_surrenders")