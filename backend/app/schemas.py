import datetime as dt
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- Auth ----------
class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Category ----------
class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Product ----------
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    is_active: bool
    category: Optional[CategoryOut] = None
    created_at: dt.datetime


# ---------- Gallery ----------
class GalleryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_url: str
    caption: Optional[str]
    created_at: dt.datetime


# ---------- Rates ----------
class GoldRateUpdate(BaseModel):
    rate_per_gram_22k: float = Field(..., gt=0)
    rate_per_gram_24k: float = Field(..., gt=0)


class GoldRateOut(GoldRateUpdate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    updated_at: dt.datetime


class SilverRateUpdate(BaseModel):
    rate_per_gram: float = Field(..., gt=0)
    rate_per_kg: float = Field(..., gt=0)


class SilverRateOut(SilverRateUpdate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    updated_at: dt.datetime


# ---------- Contact ----------
class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    phone: str = Field(..., min_length=7, max_length=30)
    email: Optional[EmailStr] = None
    message: str = Field(..., min_length=5)


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    phone: str
    email: Optional[str]
    message: str
    created_at: dt.datetime
    is_read: bool


# ---------- Upload ----------
class UploadResponse(BaseModel):
    url: str
