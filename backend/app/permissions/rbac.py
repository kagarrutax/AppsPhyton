from typing import Callable, List

from fastapi import Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.auth import User

SYSTEM_PERMISSIONS = {
    "users": ["create", "read", "update", "delete"],
    "roles": ["create", "read", "update", "delete"],
    "permissions": ["create", "read", "update", "delete"],
    "products": ["create", "read", "update", "delete", "activate", "deactivate"],
    "inventory": ["create", "read", "update", "delete"],
    "orders": ["create", "read", "update", "delete", "approve", "reject"],
    "cart": ["create", "read", "update", "delete"],
    "purchases": ["create", "read", "update", "delete"],
    "invoices": ["create", "read", "update", "delete"],
    "tickets": ["create", "read", "update", "delete"],
    "payments": ["create", "read", "update", "delete", "approve", "reject"],
    "dashboard": ["read"],
    "audit": ["read"],
    "profile": ["read", "update"],
}

CLIENTE_PERMISSIONS = [
    "products.read",
    "cart.create",
    "cart.read",
    "cart.update",
    "cart.delete",
    "orders.create",
    "orders.read",
    "purchases.create",
    "purchases.read",
    "payments.create",
    "payments.read",
    "invoices.read",
    "tickets.read",
    "profile.read",
    "profile.update",
]


def build_permission_name(modulo: str, action: str) -> str:
    return f"{modulo}.{action}"


def get_all_system_permissions() -> List[dict]:
    permissions = []
    for modulo, actions in SYSTEM_PERMISSIONS.items():
        for action in actions:
            permissions.append(
                {
                    "nombre": build_permission_name(modulo, action),
                    "modulo": modulo,
                    "descripcion": f"Permiso para {action} en {modulo}",
                }
            )
    return permissions


def require_permission(permission_name: str) -> Callable:
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.has_role("Administrador"):
            return current_user
        if not current_user.has_permission(permission_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: {permission_name}",
            )
        return current_user

    return permission_checker


def require_role(role_name: str) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.has_role(role_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Rol requerido: {role_name}",
            )
        return current_user

    return role_checker
