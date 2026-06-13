from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.billing import Invoice, Payment, PaymentStatus, Ticket


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_pending_by_order(self, order_id: int) -> Optional[Payment]:
        return (
            self.db.query(Payment)
            .filter(Payment.order_id == order_id, Payment.estado == PaymentStatus.PENDIENTE.value)
            .first()
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Payment]:
        query = self.db.query(Payment)
        if user_id:
            query = query.filter(Payment.user_id == user_id)
        if estado:
            query = query.filter(Payment.estado == estado)
        return query.order_by(Payment.fecha_envio.desc()).offset(skip).limit(limit).all()

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update(self, payment: Payment) -> Payment:
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def count(self) -> int:
        return self.db.query(Payment).count()


class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()

    def get_by_order_id(self, order_id: int) -> Optional[Invoice]:
        return self.db.query(Invoice).filter(Invoice.order_id == order_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[Invoice]:
        query = self.db.query(Invoice)
        if user_id:
            query = query.filter(Invoice.user_id == user_id)
        return query.order_by(Invoice.fecha.desc()).offset(skip).limit(limit).all()

    def create(self, invoice: Invoice) -> Invoice:
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def count(self) -> int:
        return self.db.query(Invoice).count()


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def get_by_order_id(self, order_id: int) -> Optional[Ticket]:
        return self.db.query(Ticket).filter(Ticket.order_id == order_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[Ticket]:
        query = self.db.query(Ticket)
        if user_id:
            query = query.filter(Ticket.user_id == user_id)
        return query.order_by(Ticket.fecha.desc()).offset(skip).limit(limit).all()

    def create(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def count(self) -> int:
        return self.db.query(Ticket).count()
