from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.auth import MessageResponse
from app.schemas.catalog import InventoryMovementCreate, InventoryMovementResponse
from app.services.catalog_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventario"])


@router.get("/movements", response_model=List[InventoryMovementResponse])
def list_movements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    product_id: Optional[int] = None,
    tipo: Optional[str] = Query(None, pattern="^(entrada|salida)$"),
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("inventory.read")),
):
    return InventoryService(db).list_movements(skip, limit, product_id, tipo)


@router.get("/movements/{movement_id}", response_model=InventoryMovementResponse)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("inventory.read")),
):
    return InventoryService(db).get_movement(movement_id)


@router.post("/movements", response_model=InventoryMovementResponse, status_code=status.HTTP_201_CREATED)
def create_movement(
    data: InventoryMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("inventory.create")),
):
    return InventoryService(db).create_movement(data, current_user.id)


@router.delete("/movements/{movement_id}", response_model=MessageResponse)
def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("inventory.delete")),
):
    InventoryService(db).delete_movement(movement_id, current_user.id)
    return MessageResponse(message="Movimiento eliminado y stock revertido")
