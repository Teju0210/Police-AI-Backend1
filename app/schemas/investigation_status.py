from pydantic import BaseModel

class InvestigationStatusCreate(BaseModel):
    fir_id: int
    status: str
    investigating_officer: str
    remarks: str


class InvestigationStatusResponse(BaseModel):
    id: int
    fir_id: int
    status: str
    investigating_officer: str
    remarks: str

    class Config:
        from_attributes = True