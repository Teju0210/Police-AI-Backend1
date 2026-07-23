from pydantic import BaseModel

class CrimeTypeCreate(BaseModel):
    crime_name: str
    ipc_section: str
    description: str


class CrimeTypeResponse(BaseModel):
    id: int
    crime_name: str
    ipc_section: str
    description: str

    class Config:
        from_attributes = True