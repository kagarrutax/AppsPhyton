from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.datetime_utils import utc_now
from app.models.auth import User
from app.models.billing import Invoice, Payment, PaymentMethod, PaymentStatus, Ticket
from app.models.commerce import OrderStatus
from app.repositories.audit_repository import AuditLogRepository
from app.repositories.billing_repository import InvoiceRepository, PaymentRepository, TicketRepository
from app.repositories.commerce_repository import OrderRepository
from app.schemas.billing import PaymentRejectRequest
from app.schemas.commerce import OrderStatusUpdate
from app.services.commerce_service import OrderService, _is_admin
from app.services.pdf_service import generate_invoice_pdf, generate_ticket_pdf
from app.services.upload_service import save_payment_proof


def _resolve_pdf_path(stored_path: str) -> Path:
    settings = get_settings()
    relative = stored_path.lstrip("/")
    if relative.startswith("uploads/"):
        return Path(settings.upload_dir) / relative.removeprefix("uploads/")
    return Path(settings.upload_dir) / Path(relative).name


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PaymentRepository(db)
        self.order_repo = OrderRepository(db)
        self.invoice_repo = InvoiceRepository(db)
        self.ticket_repo = TicketRepository(db)
        self.audit = AuditLogRepository(db)

    def list_payments(
        self,
        user: User,
        skip: int = 0,
        limit: int = 100,
        estado: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> List[Payment]:
        filter_user = None if _is_admin(user) else user.id
        if _is_admin(user) and user_id:
            filter_user = user_id
        return self.repo.get_all(skip, limit, filter_user, estado)

    def list_pending(self, user: User) -> List[Payment]:
        if not _is_admin(user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")
        return self.repo.get_all(estado=PaymentStatus.PENDIENTE.value, limit=200)

    def get_payment(self, payment_id: int, user: User) -> Payment:
        payment = self.repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        if not _is_admin(user) and payment.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return payment

    def submit_payment(self, order_id: int, file: UploadFile, user: User) -> Payment:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
        if order.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        if order.estado != OrderStatus.PENDIENTE.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se puede pagar pedidos pendientes",
            )
        if self.repo.get_pending_by_order(order_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un comprobante pendiente de revisión",
            )

        comprobante = save_payment_proof(file)
        payment = Payment(
            order_id=order_id,
            user_id=user.id,
            metodo=PaymentMethod.TRANSFERENCIA.value,
            monto=order.total,
            comprobante=comprobante,
            estado=PaymentStatus.PENDIENTE.value,
        )
        created = self.repo.create(payment)
        self.audit.create("submit", "payments", f"Comprobante pedido #{order_id}", user.id)
        return created

    def approve(self, payment_id: int, admin: User) -> Payment:
        if not _is_admin(admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")

        payment = self.get_payment(payment_id, admin)
        if payment.estado != PaymentStatus.PENDIENTE.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El pago ya fue procesado")

        order = self.order_repo.get_by_id(payment.order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

        order_service = OrderService(self.db)
        order_service.update_status(
            payment.order_id,
            OrderStatusUpdate(estado=OrderStatus.PAGADO.value),
            admin,
        )

        order = self.order_repo.get_by_id(payment.order_id)
        self._generate_documents(order, admin)

        payment.estado = PaymentStatus.APROBADO.value
        payment.revisado_por = admin.id
        payment.fecha_revision = utc_now()
        updated = self.repo.update(payment)
        self.audit.create("approve", "payments", f"Pago #{payment_id} aprobado", admin.id)
        return updated

    def reject(self, payment_id: int, data: PaymentRejectRequest, admin: User) -> Payment:
        if not _is_admin(admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")

        payment = self.get_payment(payment_id, admin)
        if payment.estado != PaymentStatus.PENDIENTE.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El pago ya fue procesado")

        payment.estado = PaymentStatus.RECHAZADO.value
        payment.notas_rechazo = data.notas_rechazo
        payment.revisado_por = admin.id
        payment.fecha_revision = utc_now()
        updated = self.repo.update(payment)
        self.audit.create("reject", "payments", f"Pago #{payment_id} rechazado", admin.id)
        return updated

    def _generate_documents(self, order, admin: User) -> None:
        if self.invoice_repo.get_by_order_id(order.id):
            return

        year = datetime.now().year
        inv_num = f"FAC-{year}-{self.invoice_repo.count() + 1:06d}"
        tkt_num = f"TKT-{year}-{self.ticket_repo.count() + 1:06d}"

        user = order.user
        inv_pdf = generate_invoice_pdf(order, user, inv_num)
        tkt_pdf = generate_ticket_pdf(order, user, tkt_num)

        self.invoice_repo.create(
            Invoice(
                order_id=order.id,
                user_id=order.user_id,
                numero=inv_num,
                total=order.total,
                pdf_path=inv_pdf,
            )
        )
        self.ticket_repo.create(
            Ticket(
                order_id=order.id,
                user_id=order.user_id,
                numero=tkt_num,
                total=order.total,
                pdf_path=tkt_pdf,
            )
        )


class InvoiceService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = InvoiceRepository(db)

    def list_invoices(
        self, user: User, skip: int = 0, limit: int = 100, user_id: Optional[int] = None
    ) -> List[Invoice]:
        filter_user = None if _is_admin(user) else user.id
        if _is_admin(user) and user_id:
            filter_user = user_id
        return self.repo.get_all(skip, limit, filter_user)

    def get_invoice(self, invoice_id: int, user: User) -> Invoice:
        invoice = self.repo.get_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
        if not _is_admin(user) and invoice.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return invoice

    def get_pdf_path(self, invoice_id: int, user: User) -> Path:
        invoice = self.get_invoice(invoice_id, user)
        path = _resolve_pdf_path(invoice.pdf_path)
        if not path.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF no encontrado")
        return path


class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TicketRepository(db)

    def list_tickets(
        self, user: User, skip: int = 0, limit: int = 100, user_id: Optional[int] = None
    ) -> List[Ticket]:
        filter_user = None if _is_admin(user) else user.id
        if _is_admin(user) and user_id:
            filter_user = user_id
        return self.repo.get_all(skip, limit, filter_user)

    def get_ticket(self, ticket_id: int, user: User) -> Ticket:
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
        if not _is_admin(user) and ticket.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return ticket

    def get_pdf_path(self, ticket_id: int, user: User) -> Path:
        ticket = self.get_ticket(ticket_id, user)
        path = _resolve_pdf_path(ticket.pdf_path)
        if not path.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF no encontrado")
        return path
