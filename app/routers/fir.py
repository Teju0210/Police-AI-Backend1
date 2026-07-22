from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.fir import FIR
from app.schemas.fir import FIRCreate, FIRResponse

from app.auth.dependencies import get_current_user
from app.auth.role_checker import require_role

router = APIRouter(
    prefix="/firs",
    tags=["FIR"]
)


# CREATE FIR
@router.post("/")
def create_fir(
    fir: FIRCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    new_fir = FIR(
        fir_number=fir.fir_number,
        crime_type_id=fir.crime_type_id,
        police_station_id=fir.police_station_id,
        location=fir.location,
        incident_date=fir.incident_date,
        status=fir.status,
        description=fir.description,
        latitude=fir.latitude,
        longitude=fir.longitude,
        crime_description=fir.crime_description,
        year=fir.year,
        month=fir.month,
        case_category=fir.case_category,
        gravity_offence=fir.gravity_offence,
        crime_sub_head=fir.crime_sub_head
    )

    db.add(new_fir)
    db.commit()
    db.refresh(new_fir)

    return {
        "message": "FIR Created Successfully",
        "id": new_fir.id
    }


# GET ALL FIRS
@router.get("/", response_model=list[FIRResponse])
def get_all_firs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
    require_role(["Admin", "Investigator", "Officer"])
)
):

    return db.query(FIR).all()


# GET FIR BY ID
@router.get("/{fir_id}", response_model=FIRResponse)
def get_fir_by_id(
    fir_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
    require_role(["Admin", "Investigator", "Officer"])
)
):

    fir = db.query(FIR).filter(FIR.id == fir_id).first()

    if not fir:
        raise HTTPException(
            status_code=404,
            detail="FIR Not Found"
        )

    return fir


# UPDATE FIR
@router.put("/{fir_id}")
def update_fir(
    fir_id: int,
    updated_fir: FIRCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    fir = db.query(FIR).filter(FIR.id == fir_id).first()

    if not fir:
        raise HTTPException(
            status_code=404,
            detail="FIR Not Found"
        )

    fir.fir_number = updated_fir.fir_number
    fir.crime_type_id = updated_fir.crime_type_id
    fir.police_station_id = updated_fir.police_station_id
    fir.location = updated_fir.location
    fir.incident_date = updated_fir.incident_date
    fir.status = updated_fir.status
    fir.description = updated_fir.description
    fir.latitude = updated_fir.latitude
    fir.longitude = updated_fir.longitude
    fir.crime_description = updated_fir.crime_description

    # New dataset fields
    fir.year = updated_fir.year
    fir.month = updated_fir.month
    fir.case_category = updated_fir.case_category
    fir.gravity_offence = updated_fir.gravity_offence
    fir.crime_sub_head = updated_fir.crime_sub_head

    db.commit()
    db.refresh(fir)

    return {
        "message": "FIR Updated Successfully",
        "fir": fir
    }


@router.delete("/{fir_id}")
def delete_fir(
    fir_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    fir = db.query(FIR).filter(FIR.id == fir_id).first()

    if not fir:
        raise HTTPException(
            status_code=404,
            detail="FIR Not Found"
        )

    db.delete(fir)
    db.commit()

    return {
        "message": "FIR Deleted Successfully"
    }