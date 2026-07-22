from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.victim import Victim
from app.schemas.victim import VictimCreate, VictimResponse
from app.auth.role_checker import require_role

router = APIRouter(
    prefix="/victims",
    tags=["Victims"]
)


# CREATE VICTIM
@router.post("/")
def create_victim(
    victim: VictimCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    new_victim = Victim(
        fir_id=victim.fir_id,
        age=victim.age,
        gender=victim.gender,
        victim_master_id=victim.victim_master_id,
        gender_id=victim.gender_id
    )

    db.add(new_victim)
    db.commit()
    db.refresh(new_victim)

    return {
        "message": "Victim Created Successfully",
        "id": new_victim.id
    }


# GET ALL VICTIMS
@router.get("/", response_model=list[VictimResponse])
def get_all_victims(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):
    return db.query(Victim).all()


# GET VICTIM BY ID
@router.get("/{victim_id}", response_model=VictimResponse)
def get_victim_by_id(
    victim_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(status_code=404, detail="Victim Not Found")

    return victim


# UPDATE VICTIM
@router.put("/{victim_id}")
def update_victim(
    victim_id: int,
    updated_victim: VictimCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(status_code=404, detail="Victim Not Found")

    victim.fir_id = updated_victim.fir_id
    victim.age = updated_victim.age
    victim.gender = updated_victim.gender
    victim.victim_master_id = updated_victim.victim_master_id
    victim.gender_id = updated_victim.gender_id

    db.commit()
    db.refresh(victim)

    return {
        "message": "Victim Updated Successfully",
        "victim": victim
    }


# DELETE VICTIM
@router.delete("/{victim_id}")
def delete_victim(
    victim_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    victim = db.query(Victim).filter(Victim.id == victim_id).first()

    if not victim:
        raise HTTPException(status_code=404, detail="Victim Not Found")

    db.delete(victim)
    db.commit()

    return {
        "message": "Victim Deleted Successfully"
    }