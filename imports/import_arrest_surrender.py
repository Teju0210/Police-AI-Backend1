import pandas as pd

from app.database.database import SessionLocal
from app.models.arrest_surrender import ArrestSurrender
from app.models.fir import FIR


df = pd.read_csv("dataset/ArrestSurrender.csv")

db = SessionLocal()

try:
    imported = 0

    for _, row in df.iterrows():

        fir = db.query(FIR).filter(
            FIR.id == int(row["CaseMasterID"])
        ).first()

        if not fir:
            continue


        existing = db.query(ArrestSurrender).filter(
            ArrestSurrender.accused_master_id == int(row["AccusedMasterID"]),
            ArrestSurrender.fir_id == fir.id
        ).first()

        if existing:
            continue


        arrest = ArrestSurrender(
            fir_id=fir.id,
            accused_master_id=int(row["AccusedMasterID"]),
            arrest_surrender_type_id=str(row["ArrestSurrenderTypeID"]),
            arrest_surrender_date=pd.to_datetime(
                row["ArrestSurrenderDate"]
            ),
            district=str(row["District"])
        )

        db.add(arrest)
        imported += 1


        if imported % 100 == 0:
            print(f"Imported {imported} arrest records...")


    db.commit()

    print(f"\n✅ Imported {imported} arrest/surrender records.")


except Exception as e:
    db.rollback()
    print("❌ Error:", e)


finally:
    db.close()