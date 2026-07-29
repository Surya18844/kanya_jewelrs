from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth
from app.storage import delete_local_image

router = APIRouter(prefix="/api/gallery", tags=["Gallery"])


@router.get("", response_model=list[schemas.GalleryOut])
def list_gallery(db: Session = Depends(get_db)):
    return db.query(models.Gallery).order_by(models.Gallery.created_at.desc()).all()


@router.post("", response_model=schemas.GalleryOut, status_code=201)
def add_gallery_image(
    image_url: str,
    caption: str = "",
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    item = models.Gallery(image_url=image_url, caption=caption or None)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{image_id}", status_code=204)
def delete_gallery_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    item = db.query(models.Gallery).filter(models.Gallery.id == image_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Image not found.")
    delete_local_image(item.image_url)
    db.delete(item)
    db.commit()
    return None
