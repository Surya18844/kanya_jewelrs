from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/admin", tags=["Admin Auth"])


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == payload.username).first()
    if not admin or not auth.verify_password(payload.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )
    token = auth.create_access_token(subject=admin.username)
    return schemas.Token(access_token=token)


@router.get("/me")
def me(current_admin: models.Admin = Depends(auth.get_current_admin)):
    return {"username": current_admin.username, "id": current_admin.id}
