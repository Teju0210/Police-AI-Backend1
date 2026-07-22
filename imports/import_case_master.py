import pandas as pd

from app.database.database import SessionLocal
from app.models.fir import FIR
from app.models.crime_type import CrimeType
from app.models.police_station import PoliceStation

df = pd.read_csv("dataset/CaseMaster.csv")

db = SessionLocal()

try:
    imported = 0

    for _, row in df.iterrows():

        # Skip if FIR already exists
        existing_fir = db.query(FIR).filter(
            FIR.fir_number == str(row["CrimeNo"])
        ).first()

        if existing_fir:
            continue

        # Find Police Station
        police_station = db.query(PoliceStation).filter(
            PoliceStation.station_name == str(row["PoliceStationNo"])
        ).first()

        if not police_station:
            continue

        # Find Crime Type
        crime_type = db.query(CrimeType).filter(
            CrimeType.crime_name == str(row["CrimeHead"])
        ).first()

        if not crime_type:
            continue

        # Create FIR
        new_fir = FIR(
            fir_number=str(row["CrimeNo"]),
            crime_type_id=crime_type.id,
            police_station_id=police_station.id,
            location=str(row["District"]),
            incident_date=pd.to_datetime(row["CrimeRegisteredDate"]).date(),
            status=str(row["CaseStatus"]),
            description=str(row["CrimeSubHead"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            crime_description=str(row["CrimeSubHead"]),
            year=int(row["Year"]),
            month=int(row["Month"]),
            case_category=str(row["CaseCategory"]),
            gravity_offence=str(row["GravityOffence"]),
            crime_sub_head=str(row["CrimeSubHead"])
        )

        db.add(new_fir)
        imported += 1

        # Show progress every 100 records
        if imported % 100 == 0:
            print(f"Imported {imported} FIRs...")

    db.commit()

    print(f"\n✅ Imported {imported} FIR records.")

except Exception as e:
    db.rollback()
    print("❌ Error:", e)

finally:
    db.close()