from fastapi import APIRouter, Depends, UploadFile, File

from app import models, auth, schemas
from app.storage import save_image

router = APIRouter(prefix="/api/upload", tags=["Upload"])


@router.post("/image", response_model=schemas.UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_admin: models.Admin = Depends(auth.get_current_admin),
):
    url = await save_image(file)
    return schemas.UploadResponse(url=url)
