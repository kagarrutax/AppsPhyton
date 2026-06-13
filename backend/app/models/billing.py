from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.datetime_utils import utc_now


class PaymentStatus(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class PaymentMethod(str, Enum):
    TRANSFERENCIA = "transferencia"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    metodo = Column(String(30), nullable=False, default=PaymentMethod.TRANSFERENCIA.value)
    monto = Column(Numeric(10, 2), nullable=False)
    comprobante = Column(String(500), nullable=False)
    estado = Column(String(20), nullable=False, default=PaymentStatus.PENDIENTE.value, index=True)
    notas_rechazo = Column(Text, nullable=True)
    revisado_por = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    fecha_envio = Column(DateTime, default=utc_now, nullable=False)
    fecha_revision = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="payments", lazy="selectin")
    user = relationship("User", foreign_keys=[user_id], lazy="selectin")
    reviewer = relationship("User", foreign_keys=[revisado_por])


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    numero = Column(String(30), unique=True, nullable=False, index=True)
    total = Column(Numeric(10, 2), nullable=False)
    pdf_path = Column(String(500), nullable=False)
    fecha = Column(DateTime, default=utc_now, nullable=False)

    order = relationship("Order", back_populates="invoice", lazy="selectin")
    user = relationship("User", lazy="selectin")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    numero = Column(String(30), unique=True, nullable=False, index=True)
    total = Column(Numeric(10, 2), nullable=False)
    pdf_path = Column(String(500), nullable=False)
    fecha = Column(DateTime, default=utc_now, nullable=False)

    order = relationship("Order", back_populates="ticket", lazy="selectin")
    user = relationship("User", lazy="selectin")
