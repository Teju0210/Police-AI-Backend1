from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.fir import FIR
from app.models.victim import Victim
from app.models.accused import Accused
from app.models.evidence import Evidence

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/fir/{fir_id}")
def generate_fir_report(
    fir_id: int,
    db: Session = Depends(get_db)
):

    fir = db.query(FIR).filter(
        FIR.id == fir_id
    ).first()

    if not fir:
        raise HTTPException(
            status_code=404,
            detail="FIR not found"
        )


    victims = db.query(Victim).filter(
        Victim.fir_id == fir_id
    ).all()


    accused = db.query(Accused).filter(
        Accused.fir_id == fir_id
    ).all()


    evidence = db.query(Evidence).filter(
        Evidence.fir_id == fir_id
    ).all()


    file_name = f"FIR_Report_{fir_id}.pdf"


    document = SimpleDocTemplate(
        file_name,
        pagesize=letter
    )


    styles = getSampleStyleSheet()

    content = []


    content.append(
        Paragraph(
            "FIR Investigation Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))


    # FIR Details
    content.append(
        Paragraph(
            "FIR Details",
            styles["Heading2"]
        )
    )

    details = [
        f"FIR Number: {fir.fir_number}",
        f"Location: {fir.location}",
        f"Incident Date: {fir.incident_date}",
        f"Status: {fir.status}",
        f"Crime Description: {fir.crime_description}",
        f"Category: {fir.case_category}",
        f"Gravity: {fir.gravity_offence}",
        f"Crime Sub Head: {fir.crime_sub_head}"
    ]


    for item in details:
        content.append(
            Paragraph(item, styles["Normal"])
        )


    content.append(Spacer(1, 12))


    # Victims
    content.append(
        Paragraph(
            "Victims",
            styles["Heading2"]
        )
    )


    for v in victims:
        content.append(
            Paragraph(
                f"Age: {v.age}, Gender: {v.gender}",
                styles["Normal"]
            )
        )


    content.append(Spacer(1, 12))


    # Accused
    content.append(
        Paragraph(
            "Accused",
            styles["Heading2"]
        )
    )


    for a in accused:
        content.append(
            Paragraph(
                f"""
                Name: {a.name},
                Age: {a.age},
                Gender: {a.gender},
                Address: {a.address},
                Risk Score: {a.risk_score}
                """,
                styles["Normal"]
            )
        )


    content.append(Spacer(1,12))


    # Evidence
    content.append(
        Paragraph(
            "Evidence",
            styles["Heading2"]
        )
    )


    for e in evidence:
        content.append(
            Paragraph(
                f"""
                Type: {e.evidence_type},
                Description: {e.description},
                Collected By: {e.collected_by}
                """,
                styles["Normal"]
            )
        )


    document.build(content)


    return FileResponse(
        file_name,
        media_type="application/pdf",
        filename=file_name
    )