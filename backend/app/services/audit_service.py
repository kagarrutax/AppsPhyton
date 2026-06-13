from typing import List, Optional

from sqlalchemy.orm import Session

from app.repositories.audit_repository import AuditLogRepository


class AuditService:
    def __init__(self, db: Session):
        self.repo = AuditLogRepository(db)

    def list_logs(
        self,
        skip: int = 0,
        limit: int = 100,
        modulo: Optional[str] = None,
        accion: Optional[str] = None,
    ) -> List:
        return self.repo.get_all(skip, limit, modulo, accion)
