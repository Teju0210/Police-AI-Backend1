from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.investigation_status import InvestigationStatus
from app.schemas.investigation_status import (
    InvestigationStatusCreate,
    InvestigationStatusResponse
)
from app.auth.dependencies import get_current_user
from app.auth.role_checker import require_role

router = APIRouter(
    prefix="/investigation-status",
    tags=["Investigation Status"]
)



@router.post("/")
def create_status(
    status: InvestigationStatusCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_status = InvestigationStatus(
        fir_id=status.fir_id,
        status=status.status,
        investigating_officer=status.investigating_officer,
        remarks=status.remarks
    )

    db.add(new_status)
    db.commit()
    db.refresh(new_status)

    return {
        "message": "Investigation Status Created Successfully",
        "id": new_status.id
    }


@router.get("/", response_model=list[InvestigationStatusResponse])
def get_all_status(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(InvestigationStatus).all()



@router.get("/{status_id}", response_model=InvestigationStatusResponse)
def get_status_by_id(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    status = db.query(InvestigationStatus).filter(
        InvestigationStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(status_code=404, detail="Status Not Found")

    return status



@router.put("/{status_id}")
def update_status(
    status_id: int,
    updated_status: InvestigationStatusCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    status = db.query(InvestigationStatus).filter(
        InvestigationStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(status_code=404, detail="Status Not Found")

    status.fir_id = updated_status.fir_id
    status.status = updated_status.status
    status.investigating_officer = updated_status.investigating_officer
    status.remarks = updated_status.remarks

    db.commit()
    db.refresh(status)

    return {
        "message": "Investigation Status Updated Successfully",
        "status": status
    }



@router.delete("/{status_id}")
def delete_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):
    status = db.query(InvestigationStatus).filter(
        InvestigationStatus.id == status_id
    ).first()

    if not status:
        raise HTTPException(status_code=404, detail="Status Not Found")

    db.delete(status)
    db.commit()

    return {
        "message": "Investigation Status Deleted Successfully"
    }