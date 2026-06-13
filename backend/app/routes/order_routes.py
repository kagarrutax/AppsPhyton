from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.auth import MessageResponse
from app.schemas.commerce import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.commerce_service import OrderService

router = APIRouter(prefix="/orders", tags=["Pedidos"])


@router.get("", response_model=List[OrderResponse])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    estado: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders.read")),
):
    return OrderService(db).list_orders(current_user, skip, limit, estado, user_id)


@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders.create")),
):
    return OrderService(db).checkout(current_user, data)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders.read")),
):
    return OrderService(db).get_order(order_id, current_user)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders.update")),
):
    return OrderService(db).update_status(order_id, data, current_user)


@router.delete("/{order_id}", response_model=MessageResponse)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("orders.delete")),
):
    OrderService(db).delete_order(order_id, current_user)
    return MessageResponse(message="Pedido eliminado correctamente")
