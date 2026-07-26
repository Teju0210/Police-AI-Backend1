from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Accused(Base):
    __tablename__ = "accused"

    id = Column(Integer, primary_key=True, index=True)

    fir_id = Column(Integer, ForeignKey("firs.id"))

    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    address = Column(String)

    criminal_history = Column(String)

    risk_score = Column(Float)

    fir = relationship("FIR", back_populates="accused")