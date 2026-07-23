from typing import Optional
from pydantic import BaseModel


class AccusedCreate(BaseModel):
    fir_id: int
    name: str
    age: int
    gender: str
    address: str
    criminal_history: Optional[str] = None
    risk_score: Optional[float] = None


class AccusedResponse(BaseModel):
    id: int
    fir_id: int
    name: str
    age: int
    gender: str
    address: str
    criminal_history: Optional[str] = None
    risk_score: Optional[float] = None

    class Config:
        from_attributes = True