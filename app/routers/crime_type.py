from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.crime_type import CrimeType
from app.schemas.crime_type import CrimeTypeCreate, CrimeTypeResponse
router = APIRouter(
    prefix="/crime-types",
    tags=["Crime Types"]
)


@router.post("/")
def create_crime_type(crime: CrimeTypeCreate, db: Session = Depends(get_db)):

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


@router.get("/", response_model=list[CrimeTypeResponse])
def get_all_crime_types(db: Session = Depends(get_db)):
    return db.query(CrimeType).all()


@router.get("/{crime_id}", response_model=CrimeTypeResponse)
def get_crime_type_by_id(crime_id: int, db: Session = Depends(get_db)):

    crime = db.query(CrimeType).filter(CrimeType.id == crime_id).first()

    if not crime:
        raise HTTPException(status_code=404, detail="Crime Type Not Found")

    return crime


@router.put("/{crime_id}")
def update_crime_type(
    crime_id: int,
    updated_crime: CrimeTypeCreate,
    db: Session = Depends(get_db)
):

    crime = db.query(CrimeType).filter(CrimeType.id == crime_id).first()

    if not crime:
        raise HTTPException(status_code=404, detail="Crime Type Not Found")

    crime.crime_name = updated_crime.crime_name
    crime.ipc_section = updated_crime.ipc_section
    crime.description = updated_crime.description

    db.commit()
    db.refresh(crime)

    return {
        "message": "Crime Type Updated Successfully",
        "crime": crime
    }


@router.delete("/{crime_id}")
def delete_crime_type(crime_id: int, db: Session = Depends(get_db)):

    crime = db.query(CrimeType).filter(CrimeType.id == crime_id).first()

    if not crime:
        raise HTTPException(status_code=404, detail="Crime Type Not Found")

    db.delete(crime)
    db.commit()

    return {
        "message": "Crime Type Deleted Successfully"
    }