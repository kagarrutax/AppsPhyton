from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    accion: str
    modulo: str
    detalle: Optional[str] = None
    ip_address: Optional[str] = None
    fecha: datetime
