import pandas as pd

from app.database.database import SessionLocal
from app.models.police_station import PoliceStation

df = pd.read_csv("dataset/CaseMaster.csv")

db = SessionLocal()
try:
    imported = 0

    # Remove duplicate PoliceStationNo values
    unique_stations = df.drop_duplicates(subset=["PoliceStationNo"])

    for _, row in unique_stations.iterrows():

        # Check if station already exists
        existing_station = db.query(PoliceStation).filter(
            PoliceStation.station_name == str(row["PoliceStationNo"])
        ).first()

        if existing_station:
            continue

        station = PoliceStation(
            station_name=str(row["PoliceStationNo"]),
            district=str(row["District"]),
            city=str(row["District"]),   # Temporary
            state="Karnataka"            # Temporary
        )

        db.add(station)
        imported += 1

    db.commit()

    print(f"✅ Imported {imported} police stations.")

except Exception as e:
    db.rollback()
    print("❌ Error:", e)

finally:
    db.close()