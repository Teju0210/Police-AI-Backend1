from pydantic import BaseModel


class EvidenceCreate(BaseModel):
    fir_id: int
    evidence_type: str
    description: str
    collected_by: str
    file_path: str


class EvidenceResponse(BaseModel):
    id: int
    fir_id: int
    evidence_type: str
    description: str
    collected_by: str
    file_path: str

    class Config:
        from_attributes = True