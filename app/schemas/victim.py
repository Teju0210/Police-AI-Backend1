from pydantic import BaseModel

class VictimCreate(BaseModel):
    fir_id: int
    age: int
    gender: str
    victim_master_id: int
    gender_id: int


class VictimResponse(BaseModel):
    id: int
    fir_id: int
    age: int
    gender: str
    victim_master_id: int
    gender_id: int

    class Config:
        from_attributes = True