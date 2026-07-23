from pydantic import BaseModel
from datetime import date


class FIRCreate(BaseModel):
    fir_number: str
    crime_type_id: int
    police_station_id: int
    location: str
    incident_date: date
    status: str
    description: str
    latitude: float
    longitude: float
    crime_description: str

    year: int
    month: int
    case_category: str
    gravity_offence: str
    crime_sub_head: str


class FIRResponse(BaseModel):
    id: int
    fir_number: str
    crime_type_id: int
    police_station_id: int
    location: str
    incident_date: date
    status: str
    description: str
    latitude: float
    longitude: float
    crime_description: str

    year: int
    month: int
    case_category: str
    gravity_offence: str
    crime_sub_head: str

    class Config:
        from_attributes = True