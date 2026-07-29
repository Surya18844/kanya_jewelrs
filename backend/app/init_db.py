"""
Creates all tables (if they don't exist) and seeds:
  - default categories
  - default admin account (from env vars)
  - default gold/silver rates

Run with:  python -m app.init_db
"""
from app.database import Base, engine, SessionLocal
from app import models, auth
from app.config import settings

DEFAULT_CATEGORIES = [
    ("Gold Jewellery", "gold-jewellery"),
    ("Silver Jewellery", "silver-jewellery"),
    ("Rings", "rings"),
    ("Necklaces", "necklaces"),
    ("Chains", "chains"),
    ("Bangles", "bangles"),
    ("Earrings", "earrings"),
    ("Pendants", "pendants"),
    ("Bridal Collection", "bridal-collection"),
    ("Men's Collection", "mens-collection"),
]


def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed categories
        for name, slug in DEFAULT_CATEGORIES:
            exists = db.query(models.Category).filter(models.Category.slug == slug).first()
            if not exists:
                db.add(models.Category(name=name, slug=slug))
        db.commit()

        # Seed default admin
        admin_exists = db.query(models.Admin).filter(
            models.Admin.username == settings.default_admin_username
        ).first()
        if not admin_exists:
            db.add(models.Admin(
                username=settings.default_admin_username,
                password_hash=auth.hash_password(settings.default_admin_password),
            ))
            db.commit()
            print(f"Seeded default admin user: {settings.default_admin_username}")

        # Seed default rates
        if not db.query(models.GoldRate).first():
            db.add(models.GoldRate(rate_per_gram_22k=6500, rate_per_gram_24k=7100))
        if not db.query(models.SilverRate).first():
            db.add(models.SilverRate(rate_per_gram=85, rate_per_kg=85000))
        db.commit()

        print("Database initialized successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    init()
