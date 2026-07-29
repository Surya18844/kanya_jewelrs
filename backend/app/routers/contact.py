from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/contact", tags=["Contact"])


@router.post("", response_model=schemas.ContactMessageOut, status_code=201)
def submit_contact_message(payload: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    message = models.ContactMessage(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("", response_model=list[schemas.ContactMessageOut])
def list_contact_messages(
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    return db.query(models.ContactMessage).order_by(models.ContactMessage.created_at.desc()).all()


@router.patch("/{message_id}/read", response_model=schemas.ContactMessageOut)
def mark_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    message = db.query(models.ContactMessage).filter(models.ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Enquiry not found.")
    message.is_read = True
    db.commit()
    db.refresh(message)
    return message


@router.delete("/{message_id}", status_code=204)
def delete_contact_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    message = db.query(models.ContactMessage).filter(models.ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Enquiry not found.")
    db.delete(message)
    db.commit()
    return None
