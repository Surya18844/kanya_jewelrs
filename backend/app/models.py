import datetime as dt

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
)
from sqlalchemy.orm import relationship

from app.database import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    category = relationship("Category", back_populates="products")


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class GoldRate(Base):
    __tablename__ = "gold_rates"

    id = Column(Integer, primary_key=True, index=True)
    rate_per_gram_22k = Column(Numeric(10, 2), nullable=False)
    rate_per_gram_24k = Column(Numeric(10, 2), nullable=False)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)


class SilverRate(Base):
    __tablename__ = "silver_rates"

    id = Column(Integer, primary_key=True, index=True)
    rate_per_gram = Column(Numeric(10, 2), nullable=False)
    rate_per_kg = Column(Numeric(10, 2), nullable=False)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(150), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    is_read = Column(Boolean, default=False)
