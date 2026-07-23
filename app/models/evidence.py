from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)

    fir_id = Column(Integer, ForeignKey("firs.id"))

    evidence_type = Column(String)
    description = Column(String)
    collected_by = Column(String)
    file_path = Column(String)

    fir = relationship("FIR", back_populates="evidence")