from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.auth import User
from app.permissions.rbac import require_permission
from app.schemas.auth import MessageResponse, PermissionCreate, PermissionResponse, PermissionUpdate
from app.services.auth_service import PermissionService

router = APIRouter(prefix="/permissions", tags=["Permisos"])


@router.get("", response_model=List[PermissionResponse])
def list_permissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
    modulo: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("permissions.read")),
):
    return PermissionService(db).list_permissions(skip, limit, modulo)


@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("permissions.read")),
):
    return PermissionService(db).get_permission(permission_id)


@router.post("", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(
    data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("permissions.create")),
):
    return PermissionService(db).create_permission(data, current_user.id)


@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: int,
    data: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("permissions.update")),
):
    return PermissionService(db).update_permission(permission_id, data, current_user.id)


@router.delete("/{permission_id}", response_model=MessageResponse)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("permissions.delete")),
):
    PermissionService(db).delete_permission(permission_id, current_user.id)
    return MessageResponse(message="Permiso eliminado correctamente")
