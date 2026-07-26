from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Victim(Base):
    __tablename__ = "victims"

    id = Column(Integer, primary_key=True, index=True)

    fir_id = Column(Integer, ForeignKey("firs.id"))

    age = Column(Integer)

    gender = Column(String)

    victim_master_id = Column(Integer)

    gender_id = Column(Integer)

    fir = relationship("FIR", back_populates="victims")