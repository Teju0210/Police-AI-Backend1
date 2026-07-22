from pydantic import BaseModel

class OfficerCreate(BaseModel):
    name: str
    rank: str
    badge_number: str
    phone: str