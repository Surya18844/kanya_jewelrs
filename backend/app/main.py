import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.routers import (
    admin_auth, categories, products, gallery, rates, contact, upload,
)

app = FastAPI(
    title="Kanya Jewelers API",
    description="Backend API for the Kanya Jewelers showcase website and admin panel.",
    version="1.0.0",
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Static files (local image fallback) ----------------
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(os.path.join(static_dir, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ---------------- Global error handling ----------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid input.", "errors": exc.errors()},
    )


@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A database error occurred. Please try again later."},
    )


# ---------------- Routers ----------------
app.include_router(admin_auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(gallery.router)
app.include_router(rates.router)
app.include_router(contact.router)
app.include_router(upload.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Kanya Jewelers API"}


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
