import pandas as pd

from app.database.database import SessionLocal
from app.models.victim import Victim
from app.models.fir import FIR

# Read Victim dataset
df = pd.read_csv("dataset/Victim.csv")

db = SessionLocal()

try:
    imported = 0

    for _, row in df.iterrows():

        # Find corresponding FIR using CaseMasterID
        fir = db.query(FIR).filter(
            FIR.id == int(row["CaseMasterID"])
        ).first()

        if not fir:
            continue

        # Skip duplicate victim
        existing = db.query(Victim).filter(
            Victim.victim_master_id == int(row["VictimMasterID"])
        ).first()

        if existing:
            continue

        victim = Victim(
            fir_id=fir.id,
            age=int(row["AgeYear"]),
            gender=str(row["GenderID"]),
            victim_master_id=int(row["VictimMasterID"]),
            gender_id=1 if str(row["GenderID"]) == "M" else 2
        )

        db.add(victim)
        imported += 1

        if imported % 100 == 0:
            print(f"Imported {imported} victims...")

    db.commit()

    print(f"\n✅ Imported {imported} victims.")

except Exception as e:
    db.rollback()
    print("❌ Error:", e)

finally:
    db.close()