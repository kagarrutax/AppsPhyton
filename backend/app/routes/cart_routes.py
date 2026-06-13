from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.auth import MessageResponse
from app.schemas.commerce import CartItemAdd, CartItemUpdate, CartResponse
from app.services.commerce_service import CartService

router = APIRouter(prefix="/cart", tags=["Carrito"])


@router.get("", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("cart.read")),
):
    return CartService(db).get_cart(current_user)


@router.post("/items", response_model=CartResponse)
def add_to_cart(
    data: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("cart.create")),
):
    return CartService(db).add_item(current_user, data)


@router.put("/items/{product_id}", response_model=CartResponse)
def update_cart_item(
    product_id: int,
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("cart.update")),
):
    return CartService(db).update_item(current_user, product_id, data)


@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("cart.delete")),
):
    return CartService(db).remove_item(current_user, product_id)


@router.delete("/clear", response_model=CartResponse)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("cart.delete")),
):
    return CartService(db).clear_cart(current_user)
