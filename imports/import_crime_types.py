import pandas as pd

from app.database.database import SessionLocal
from app.models.crime_type import CrimeType

# Read CaseMaster dataset
df = pd.read_csv("dataset/CaseMaster.csv")

db = SessionLocal()

try:
    imported = 0

    # Get unique CrimeHead values
    crime_heads = df["CrimeHead"].dropna().unique()

    for crime in crime_heads:

        # Skip if already exists
        existing = db.query(CrimeType).filter(
            CrimeType.crime_name == str(crime)
        ).first()

        if existing:
            continue

        new_crime = CrimeType(
            crime_name=str(crime),
            ipc_section="Unknown",
            description=str(crime)
        )

        db.add(new_crime)
        imported += 1

    db.commit()

    print(f"✅ Imported {imported} crime types.")

except Exception as e:
    db.rollback()
    print("❌ Error:", e)

finally:
    db.close()