from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    user_id: int
    metodo: str
    monto: Decimal
    comprobante: str
    estado: str
    notas_rechazo: Optional[str] = None
    revisado_por: Optional[int] = None
    fecha_envio: datetime
    fecha_revision: Optional[datetime] = None


class PaymentRejectRequest(BaseModel):
    notas_rechazo: str = Field(..., min_length=5, max_length=500)


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    user_id: int
    numero: str
    total: Decimal
    pdf_path: str
    fecha: datetime


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    user_id: int
    numero: str
    total: Decimal
    pdf_path: str
    fecha: datetime
