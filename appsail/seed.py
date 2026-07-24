import pandas as pd
from datetime import datetime
import app.main
from app.database.database import SessionLocal, Base, engine
from app.models.fir import FIR
from app.models.victim import Victim
from app.models.accused import Accused
from app.models.evidence import Evidence
from app.models.arrest_surrender import ArrestSurrender
from app.models.officer import Officer

def seed_database():
    # Drop all existing tables to start fresh
    Base.metadata.drop_all(bind=engine)
    # Make sure all tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    print("Seeding all FIRs from CaseMaster.csv...")
    try:
        df = pd.read_csv("data/CaseMaster.csv")
        
        # Insert all rows from the dataset
        firs_to_insert = []
        for index, row in df.iterrows():
            try:
                date_obj = datetime.strptime(str(row['CrimeRegisteredDate']), "%Y-%m-%d").date()
            except:
                date_obj = None

            fir = FIR(
                fir_number=str(row.get('CrimeNo', '')),
                police_station_id=int(row.get('PoliceStationNo', 0)) if pd.notna(row.get('PoliceStationNo')) else None,
                location=str(row.get('District', '')),
                incident_date=date_obj,
                status=str(row.get('CaseStatus', 'Open')),
                latitude=float(row.get('latitude', 0.0)) if pd.notna(row.get('latitude')) else None,
                longitude=float(row.get('longitude', 0.0)) if pd.notna(row.get('longitude')) else None,
                year=int(row.get('Year', 0)) if pd.notna(row.get('Year')) else None,
                month=int(row.get('Month', 0)) if pd.notna(row.get('Month')) else None,
                case_category=str(row.get('CaseCategory', '')),
                gravity_offence=str(row.get('GravityOffence', '')),
                crime_sub_head=str(row.get('CrimeSubHead', ''))
            )
            firs_to_insert.append(fir)

        db.add_all(firs_to_insert)
        db.commit()
        
        print(f"Successfully seeded {len(firs_to_insert)} FIRs!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
