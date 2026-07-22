from pydantic import BaseModel


class AccusedCreate(BaseModel):
    fir_id: int
    name: str
    age: int
    gender: str
    address: str
    criminal_history: str
    risk_score: float


class AccusedResponse(BaseModel):
    id: int
    fir_id: int
    name: str
    age: int
    gender: str
    address: str
    criminal_history: str
    risk_score: float

    class Config:
        from_attributes = True