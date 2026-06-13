from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.billing import InvoiceResponse
from app.services.billing_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["Facturación"])


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("invoices.read")),
):
    return InvoiceService(db).list_invoices(current_user, skip, limit, user_id)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("invoices.read")),
):
    return InvoiceService(db).get_invoice(invoice_id, current_user)


@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("invoices.read")),
):
    path = InvoiceService(db).get_pdf_path(invoice_id, current_user)
    return FileResponse(path, media_type="application/pdf", filename=path.name)
