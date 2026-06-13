import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

ALLOWED_PAYMENT_TYPES = {"image/jpeg", "image/png", "image/jpg", "application/pdf"}
ALLOWED_PAYMENT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}


def save_product_image(file: UploadFile) -> str:
    settings = get_settings()

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido. Use JPG o PNG",
        )

    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extensión no permitida. Use .jpg, .jpeg o .png",
        )

    content = file.file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Archivo excede {settings.max_upload_size_mb}MB",
        )

    upload_dir = Path(settings.upload_dir) / "products"
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = upload_dir / filename
    filepath.write_bytes(content)

    return f"/uploads/products/{filename}"


def delete_product_image(image_path: Optional[str]) -> None:
    if not image_path:
        return
    settings = get_settings()
    relative = image_path.lstrip("/")
    if relative.startswith("uploads/"):
        filepath = Path(relative)
    else:
        filepath = Path(settings.upload_dir) / "products" / Path(relative).name

    if filepath.exists():
        filepath.unlink()


def save_payment_proof(file: UploadFile) -> str:
    settings = get_settings()

    if file.content_type not in ALLOWED_PAYMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido. Use JPG, PNG o PDF",
        )

    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_PAYMENT_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extensión no permitida. Use .jpg, .jpeg, .png o .pdf",
        )

    content = file.file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Archivo excede {settings.max_upload_size_mb}MB",
        )

    upload_dir = Path(settings.upload_dir) / "payments"
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = upload_dir / filename
    filepath.write_bytes(content)

    return f"/uploads/payments/{filename}"
