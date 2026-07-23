from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.crime_type import CrimeType
from app.schemas.crime_type import CrimeTypeCreate, CrimeTypeResponse
from app.auth.role_checker import require_role

router = APIRouter(
    prefix="/crime-types",
    tags=["Crime Types"]
)


# CREATE CRIME TYPE
@router.post("/")
def create_crime_type(
    crime: CrimeTypeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    new_crime = CrimeType(
        crime_name=crime.crime_name,
        ipc_section=crime.ipc_section,
        description=crime.description
    )

    db.add(new_crime)
    db.commit()
    db.refresh(new_crime)

    return {
        "message": "Crime Type Created Successfully",
        "id": new_crime.id
    }


# GET ALL CRIME TYPES
@router.get("/", response_model=list[CrimeTypeResponse])
def get_all_crime_types(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    return db.query(CrimeType).all()


# GET CRIME TYPE BY ID
@router.get("/{crime_id}", response_model=CrimeTypeResponse)
def get_crime_type_by_id(
    crime_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    crime = db.query(CrimeType).filter(CrimeType.id == crime_id).first()

    if not crime:
        raise HTTPException(
            status_code=404,
            detail="Crime Type Not Found"
        )

    return crime


# UPDATE CRIME TYPE
@router.put("/{crime_id}")
def update_crime_type(
    crime_id: int,
    updated_crime: CrimeTypeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    crime = db.query(CrimeType).filter(CrimeType.id == crime_id).first()

    if not crime:
        raise HTTPException(
            status_code=404,
            detail="Crime Type Not Found"
        )

    crime.crime_name = updated_crime.crime_name
    crime.ipc_section = updated_crime.ipc_section
    crime.description = updated_crime.description

    db.commit()
    db.refresh(crime)

    return {
        "message": "Crime Type Updated Successfully",
        "crime": crime
    }


# DELETE CRIME TYPE
@router.delete("/{crime_id}")
def delete_crime_type(
    crime_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    crime = db.query(CrimeType).filter(CrimeType.id == crime_id).first()

    if not crime:
        raise HTTPException(
            status_code=404,
            detail="Crime Type Not Found"
        )

    db.delete(crime)
    db.commit()

    return {
        "message": "Crime Type Deleted Successfully"
    }