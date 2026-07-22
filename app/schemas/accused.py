from pydantic import BaseModel

class AccusedCreate(BaseModel):
    fir_id: int
    name: str
    age: int
    gender: str
    address: str


class AccusedResponse(BaseModel):
    id: int
    fir_id: int
    name: str
    age: int
    gender: str
    address: str

    class Config:
        from_attributes = True