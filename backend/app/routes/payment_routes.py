from typing import List, Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.billing import PaymentRejectRequest, PaymentResponse
from app.services.billing_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Pagos"])


@router.get("", response_model=List[PaymentResponse])
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    estado: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payments.read")),
):
    return PaymentService(db).list_payments(current_user, skip, limit, estado, user_id)


@router.get("/pending", response_model=List[PaymentResponse])
def list_pending_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payments.approve")),
):
    return PaymentService(db).list_pending(current_user)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payments.read")),
):
    return PaymentService(db).get_payment(payment_id, current_user)


@router.post("/orders/{order_id}", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def submit_payment(
    order_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payments.create")),
):
    return PaymentService(db).submit_payment(order_id, file, current_user)


@router.post("/{payment_id}/approve", response_model=PaymentResponse)
def approve_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payments.approve")),
):
    return PaymentService(db).approve(payment_id, current_user)


@router.post("/{payment_id}/reject", response_model=PaymentResponse)
def reject_payment(
    payment_id: int,
    data: PaymentRejectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("payments.reject")),
):
    return PaymentService(db).reject(payment_id, data, current_user)
