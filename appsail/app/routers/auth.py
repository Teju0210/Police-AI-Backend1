from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.login import LoginRequest

from app.auth.hash import verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    token = create_access_token(
        {
            "id": db_user.id,
            "email": db_user.email,
            "role": db_user.role,
            "name": db_user.name
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role,
        "name": db_user.name
    }