from typing import List, Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.auth import MessageResponse
from app.schemas.catalog import ProductCreate, ProductResponse, ProductUpdate
from app.services.catalog_service import ProductService

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("/public", response_model=List[ProductResponse])
def list_public_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Catálogo público de productos activos (sin autenticación)."""
    return ProductService(db).list_products(skip, limit, search, category_id, only_active=True)


@router.get("", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    only_active: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("products.read")),
):
    return ProductService(db).list_products(skip, limit, search, category_id, only_active)


@router.get("/low-stock", response_model=List[ProductResponse])
def list_low_stock(
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("inventory.read")),
):
    return ProductService(db).get_low_stock()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("products.read")),
):
    return ProductService(db).get_product(product_id)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.create")),
):
    return ProductService(db).create_product(data, current_user.id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.update")),
):
    return ProductService(db).update_product(product_id, data, current_user.id)


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.delete")),
):
    ProductService(db).delete_product(product_id, current_user.id)
    return MessageResponse(message="Producto eliminado correctamente")


@router.patch("/{product_id}/activate", response_model=ProductResponse)
def activate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.activate")),
):
    return ProductService(db).activate_product(product_id, current_user.id)


@router.patch("/{product_id}/deactivate", response_model=ProductResponse)
def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.deactivate")),
):
    return ProductService(db).deactivate_product(product_id, current_user.id)


@router.post("/{product_id}/imagen", response_model=ProductResponse)
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.update")),
):
    return ProductService(db).upload_image(product_id, file, current_user.id)
