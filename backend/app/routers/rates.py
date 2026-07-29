from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/rates", tags=["Rates"])


def _get_or_create_gold(db: Session) -> models.GoldRate:
    rate = db.query(models.GoldRate).order_by(models.GoldRate.id.desc()).first()
    if not rate:
        rate = models.GoldRate(rate_per_gram_22k=6500, rate_per_gram_24k=7100)
        db.add(rate)
        db.commit()
        db.refresh(rate)
    return rate


def _get_or_create_silver(db: Session) -> models.SilverRate:
    rate = db.query(models.SilverRate).order_by(models.SilverRate.id.desc()).first()
    if not rate:
        rate = models.SilverRate(rate_per_gram=85, rate_per_kg=85000)
        db.add(rate)
        db.commit()
        db.refresh(rate)
    return rate


@router.get("/gold", response_model=schemas.GoldRateOut)
def get_gold_rate(db: Session = Depends(get_db)):
    return _get_or_create_gold(db)


@router.put("/gold", response_model=schemas.GoldRateOut)
def update_gold_rate(
    payload: schemas.GoldRateUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    rate = _get_or_create_gold(db)
    rate.rate_per_gram_22k = payload.rate_per_gram_22k
    rate.rate_per_gram_24k = payload.rate_per_gram_24k
    db.commit()
    db.refresh(rate)
    return rate


@router.get("/silver", response_model=schemas.SilverRateOut)
def get_silver_rate(db: Session = Depends(get_db)):
    return _get_or_create_silver(db)


@router.put("/silver", response_model=schemas.SilverRateOut)
def update_silver_rate(
    payload: schemas.SilverRateUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    rate = _get_or_create_silver(db)
    rate.rate_per_gram = payload.rate_per_gram
    rate.rate_per_kg = payload.rate_per_kg
    db.commit()
    db.refresh(rate)
    return rate
