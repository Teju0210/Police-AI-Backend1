from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.victim import Victim
from app.schemas.victim import VictimCreate, VictimResponse
from app.auth.dependencies import get_current_user
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
router = APIRouter(prefix="/victims", tags=["Victims"])


@router.post("/")
def create_victim(
    victim: VictimCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    new_victim = Victim(
        fir_id=victim.fir_id,
        name=victim.name,
        age=victim.age,
        gender=victim.gender,
        address=victim.address
    )

    db.add(new_victim)
    db.commit()
    db.refresh(new_victim)

    return {
        "message": "Victim Created Successfully",
        "id": new_victim.id
    }


@router.get("/", response_model=list[VictimResponse])
def get_all_victims(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    victims = db.query(Victim).all()
    return victims


@router.get("/{victim_id}")
def get_victim_by_id(
    victim_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(status_code=404, detail="Victim Not Found")

    return victim


@router.put("/{victim_id}")
def update_victim(
    victim_id: int,
    updated_victim: VictimCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(status_code=404, detail="Victim Not Found")

    victim.fir_id = updated_victim.fir_id
    victim.name = updated_victim.name
    victim.age = updated_victim.age
    victim.gender = updated_victim.gender
    victim.address = updated_victim.address

    db.commit()
    db.refresh(victim)

    return {
        "message": "Victim Updated Successfully",
        "victim": victim
    }


@router.delete("/{victim_id}")
def delete_victim(
    victim_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(status_code=404, detail="Victim Not Found")

    db.delete(victim)
    db.commit()

    return {
        "message": "Victim Deleted Successfully"
    }