from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.evidence import Evidence
from app.schemas.evidence import EvidenceCreate, EvidenceResponse
from app.auth.role_checker import require_role

router = APIRouter(
    prefix="/evidence",
    tags=["Evidence"]
)


# CREATE
@router.post("/")
def create_evidence(
    evidence: EvidenceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    new_evidence = Evidence(
        fir_id=evidence.fir_id,
        evidence_type=evidence.evidence_type,
        description=evidence.description,
        collected_by=evidence.collected_by,
        file_path=evidence.file_path
    )

    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)

    return {
        "message": "Evidence Created Successfully",
        "id": new_evidence.id
    }


# GET ALL
@router.get("/", response_model=list[EvidenceResponse])
def get_all_evidence(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    return db.query(Evidence).all()


# GET BY ID
@router.get("/{evidence_id}", response_model=EvidenceResponse)
def get_evidence_by_id(
    evidence_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator", "Officer"]))
):

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence Not Found")

    return evidence


# UPDATE
@router.put("/{evidence_id}")
def update_evidence(
    evidence_id: int,
    updated: EvidenceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "Investigator"]))
):

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence Not Found")

    evidence.fir_id = updated.fir_id
    evidence.evidence_type = updated.evidence_type
    evidence.description = updated.description
    evidence.collected_by = updated.collected_by
    evidence.file_path = updated.file_path

    db.commit()
    db.refresh(evidence)

    return {
        "message": "Evidence Updated Successfully",
        "evidence": evidence
    }


# DELETE
@router.delete("/{evidence_id}")
def delete_evidence(
    evidence_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):

    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence Not Found")

    db.delete(evidence)
    db.commit()

    return {
        "message": "Evidence Deleted Successfully"
    }