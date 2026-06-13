from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.auth import AuditLog


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        accion: str,
        modulo: str,
        detalle: Optional[str] = None,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            accion=accion,
            modulo=modulo,
            detalle=detalle,
            ip_address=ip_address,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        modulo: Optional[str] = None,
        accion: Optional[str] = None,
    ) -> List[AuditLog]:
        query = self.db.query(AuditLog).order_by(AuditLog.fecha.desc())
        if modulo:
            query = query.filter(AuditLog.modulo == modulo)
        if accion:
            query = query.filter(AuditLog.accion == accion)
        return query.offset(skip).limit(limit).all()
