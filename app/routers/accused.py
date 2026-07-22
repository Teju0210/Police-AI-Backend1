from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.accused import Accused
from app.schemas.accused import AccusedCreate, AccusedResponse
from app.auth.dependencies import get_current_user
from app.auth.role_checker import require_role

router = APIRouter(prefix="/accused", tags=["Accused"])



@router.post("/")
def create_accused(
    accused: AccusedCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    new_accused = Accused(
        fir_id=accused.fir_id,
        name=accused.name,
        age=accused.age,
        gender=accused.gender,
        address=accused.address
    )

    db.add(new_accused)
    db.commit()
    db.refresh(new_accused)

    return {
        "message": "Accused Created Successfully",
        "id": new_accused.id
    }


@router.get("/", response_model=list[AccusedResponse])
def get_all_accused(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Accused).all()


@router.get("/{accused_id}", response_model=AccusedResponse)
def get_accused_by_id(
    accused_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    accused = db.query(Accused).filter(Accused.id == accused_id).first()

    if not accused:
        raise HTTPException(status_code=404, detail="Accused Not Found")

    return accused


@router.put("/{accused_id}")
def update_accused(
    accused_id: int,
    updated_accused: AccusedCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    accused = db.query(Accused).filter(Accused.id == accused_id).first()

    if not accused:
        raise HTTPException(status_code=404, detail="Accused Not Found")

    accused.fir_id = updated_accused.fir_id
    accused.name = updated_accused.name
    accused.age = updated_accused.age
    accused.gender = updated_accused.gender
    accused.address = updated_accused.address

    db.commit()
    db.refresh(accused)

    return {
        "message": "Accused Updated Successfully",
        "accused": accused
    }



@router.delete("/{accused_id}")
def delete_accused(
    accused_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    accused = db.query(Accused).filter(Accused.id == accused_id).first()

    if not accused:
        raise HTTPException(status_code=404, detail="Accused Not Found")

    db.delete(accused)
    db.commit()

    return {
        "message": "Accused Deleted Successfully"
    }