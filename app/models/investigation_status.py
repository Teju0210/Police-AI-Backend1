from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class InvestigationStatus(Base):
    __tablename__ = "investigation_status"

    id = Column(Integer, primary_key=True, index=True)
    fir_id = Column(Integer, ForeignKey("firs.id"))
    status = Column(String)
    investigating_officer = Column(String)
    remarks = Column(String)