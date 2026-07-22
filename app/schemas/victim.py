from pydantic import BaseModel

class VictimCreate(BaseModel):
    fir_id: int
    name: str
    age: int
    gender: str
    address: str


class VictimResponse(BaseModel):
    id: int
    fir_id: int
    name: str
    age: int
    gender: str
    address: str

    class Config:
        from_attributes = True