from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.billing import TicketResponse
from app.services.billing_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("", response_model=List[TicketResponse])
def list_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("tickets.read")),
):
    return TicketService(db).list_tickets(current_user, skip, limit, user_id)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("tickets.read")),
):
    return TicketService(db).get_ticket(ticket_id, current_user)


@router.get("/{ticket_id}/pdf")
def download_ticket_pdf(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("tickets.read")),
):
    path = TicketService(db).get_pdf_path(ticket_id, current_user)
    return FileResponse(path, media_type="application/pdf", filename=path.name)
