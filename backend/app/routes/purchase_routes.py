from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.commerce import PurchaseResponse
from app.services.commerce_service import PurchaseService

router = APIRouter(prefix="/purchases", tags=["Compras"])


@router.get("", response_model=List[PurchaseResponse])
def list_purchases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("purchases.read")),
):
    return PurchaseService(db).list_purchases(current_user, skip, limit, user_id)


@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("purchases.read")),
):
    return PurchaseService(db).get_purchase(purchase_id, current_user)
