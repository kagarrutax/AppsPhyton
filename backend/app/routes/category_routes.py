from typing import List, Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.auth import MessageResponse
from app.schemas.catalog import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    InventoryMovementCreate,
    InventoryMovementResponse,
    LowStockProductResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.catalog_service import CategoryService, InventoryService, ProductService

router = APIRouter(prefix="/categories", tags=["Categorías"])


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    only_active: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("products.read")),
):
    return CategoryService(db).list_categories(skip, limit, only_active)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("products.read")),
):
    return CategoryService(db).get_category(category_id)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.create")),
):
    return CategoryService(db).create_category(data, current_user.id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.update")),
):
    return CategoryService(db).update_category(category_id, data, current_user.id)


@router.delete("/{category_id}", response_model=MessageResponse)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("products.delete")),
):
    CategoryService(db).delete_category(category_id, current_user.id)
    return MessageResponse(message="Categoría eliminada correctamente")
