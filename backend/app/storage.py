"""
Image storage abstraction.

If Cloudinary credentials are configured, images are uploaded to
Cloudinary and the returned secure URL is stored in PostgreSQL.
Otherwise, images are saved to local disk under app/static/uploads
and served by FastAPI's StaticFiles mount (useful for local dev).
"""
import os
import uuid

from fastapi import UploadFile, HTTPException

from app.config import settings

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE_MB = 8

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

if settings.cloudinary_enabled:
    import cloudinary
    import cloudinary.uploader

    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


def _validate_file(file: UploadFile, contents: bytes):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only JPG, PNG or WEBP images are allowed.")
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Image must be smaller than {MAX_FILE_SIZE_MB}MB.")


async def save_image(file: UploadFile, folder: str = "kanya-jewelers") -> str:
    """Save the uploaded image and return a publicly accessible URL."""
    contents = await file.read()
    _validate_file(file, contents)

    if settings.cloudinary_enabled:
        import cloudinary.uploader
        result = cloudinary.uploader.upload(contents, folder=folder, resource_type="image")
        return result["secure_url"]

    # Local disk fallback
    ext = os.path.splitext(file.filename or "")[1].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(contents)
    return f"{settings.backend_base_url}/static/uploads/{filename}"


def delete_local_image(url: str):
    """Best-effort deletion of a locally stored image given its URL."""
    if settings.cloudinary_enabled:
        return
    filename = url.rsplit("/", 1)[-1]
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass
