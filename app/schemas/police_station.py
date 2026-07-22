from pydantic import BaseModel

class PoliceStationCreate(BaseModel):
    station_name: str
    district: str
    city: str
    state: str


class PoliceStationResponse(BaseModel):
    id: int
    station_name: str
    district: str
    city: str
    state: str

    class Config:
        from_attributes = True