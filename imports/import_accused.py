import pandas as pd

from app.database.database import SessionLocal
from app.models.accused import Accused
from app.models.fir import FIR


df = pd.read_csv("dataset/Accused.csv")

db = SessionLocal()

try:
    imported = 0

    for _, row in df.iterrows():

        # Find matching FIR
        fir = db.query(FIR).filter(
            FIR.id == int(row["CaseMasterID"])
        ).first()

        if not fir:
            continue

        # Skip duplicate accused
        existing = db.query(Accused).filter(
            Accused.fir_id == fir.id,
            Accused.name == str(row["PersonID"])
        ).first()

        if existing:
            continue


        accused = Accused(
            fir_id=fir.id,
            name=str(row["PersonID"]),
            age=int(row["AgeYear"]),
            gender=str(row["GenderID"]),
            address=str(row["District"]),
            criminal_history=str(row["RepeatIdentity"]),
            risk_score=0.0
        )

        db.add(accused)
        imported += 1


        if imported % 100 == 0:
            print(f"Imported {imported} accused...")


    db.commit()

    print(f"\n✅ Imported {imported} accused records.")


except Exception as e:
    db.rollback()
    print("❌ Error:", e)


finally:
    db.close()