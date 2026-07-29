from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=list[schemas.ProductOut])
def list_products(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by product name"),
    category_slug: Optional[str] = Query(None, description="Filter by category slug"),
    active_only: bool = Query(True),
):
    query = db.query(models.Product).options(joinedload(models.Product.category))

    if active_only:
        query = query.filter(models.Product.is_active.is_(True))
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    if category_slug:
        query = query.join(models.Category).filter(models.Category.slug == category_slug)

    return query.order_by(models.Product.created_at.desc()).all()


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .options(joinedload(models.Product.category))
        .filter(models.Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


@router.post("", response_model=schemas.ProductOut, status_code=201)
def create_product(
    payload: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    if payload.category_id:
        category = db.query(models.Category).filter(models.Category.id == payload.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Selected category does not exist.")
    product = models.Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    payload: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    data = payload.model_dump(exclude_unset=True)
    if "category_id" in data and data["category_id"] is not None:
        category = db.query(models.Category).filter(models.Category.id == data["category_id"]).first()
        if not category:
            raise HTTPException(status_code=400, detail="Selected category does not exist.")

    for field, value in data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    from app.storage import delete_local_image
    if product.image_url:
        delete_local_image(product.image_url)

    db.delete(product)
    db.commit()
    return None
