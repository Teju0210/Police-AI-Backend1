from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.police_station import PoliceStation
from app.schemas.police_station import PoliceStationCreate, PoliceStationResponse
from app.auth.role_checker import require_role

router = APIRouter(
    prefix="/police-stations",
    tags=["Police Stations"]
)


# CREATE POLICE STATION
@router.post("/")
def create_police_station(
    station: PoliceStationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    new_station = PoliceStation(
        station_name=station.station_name,
        district=station.district,
        city=station.city,
        state=station.state
    )

    db.add(new_station)
    db.commit()
    db.refresh(new_station)

    return {
        "message": "Police Station Created Successfully",
        "id": new_station.id
    }


# GET ALL POLICE STATIONS
@router.get("/", response_model=list[PoliceStationResponse])
def get_all_police_stations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    return db.query(PoliceStation).all()


# GET POLICE STATION BY ID
@router.get("/{station_id}", response_model=PoliceStationResponse)
def get_police_station_by_id(
    station_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    station = db.query(PoliceStation).filter(
        PoliceStation.id == station_id
    ).first()

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Police Station Not Found"
        )

    return station


# UPDATE POLICE STATION
@router.put("/{station_id}")
def update_police_station(
    station_id: int,
    updated_station: PoliceStationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    station = db.query(PoliceStation).filter(
        PoliceStation.id == station_id
    ).first()

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Police Station Not Found"
        )

    station.station_name = updated_station.station_name
    station.district = updated_station.district
    station.city = updated_station.city
    station.state = updated_station.state

    db.commit()
    db.refresh(station)

    return {
        "message": "Police Station Updated Successfully",
        "station": station
    }


# DELETE POLICE STATION
@router.delete("/{station_id}")
def delete_police_station(
    station_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    station = db.query(PoliceStation).filter(
        PoliceStation.id == station_id
    ).first()

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Police Station Not Found"
        )

    db.delete(station)
    db.commit()

    return {
        "message": "Police Station Deleted Successfully"
    }