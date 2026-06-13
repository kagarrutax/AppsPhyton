from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.auth import Permission, Role, User
from app.repositories.auth_repository import PermissionRepository, RoleRepository, UserRepository
from app.repositories.audit_repository import AuditLogRepository
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RoleUpdate,
    TokenResponse,
    UserCreate,
    UserRegister,
    UserUpdate,
)
from app.security.jwt import create_access_token, create_refresh_token, verify_token
from app.security.password import hash_password, verify_password
from app.security.sanitizer import sanitize_string, validate_password_strength


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.audit_repo = AuditLogRepository(db)

    def login(self, data: LoginRequest, ip_address: Optional[str] = None) -> TokenResponse:
        user = self.user_repo.get_by_email(data.email.lower())
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        if not user.estado:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

        token_data = {"sub": str(user.id), "email": user.email}
        self.audit_repo.create("login", "auth", f"Login exitoso: {user.email}", user.id, ip_address)
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = verify_token(refresh_token, "refresh")
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        user = self.user_repo.get_by_id(int(payload["sub"]))
        if not user or not user.estado:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no válido")

        token_data = {"sub": str(user.id), "email": user.email}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )

    def register_client(self, data: UserRegister, ip_address: Optional[str] = None) -> User:
        valid, msg = validate_password_strength(data.password)
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        if self.user_repo.get_by_email(data.email.lower()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")

        cliente_role = self.role_repo.get_by_name("Cliente")
        if not cliente_role:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Rol Cliente no configurado")

        user = User(
            nombres=sanitize_string(data.nombres),
            apellidos=sanitize_string(data.apellidos),
            email=data.email.lower(),
            telefono=data.telefono,
            hashed_password=hash_password(data.password),
            estado=True,
            roles=[cliente_role],
        )
        created = self.user_repo.create(user)
        self.audit_repo.create("register", "auth", f"Registro: {created.email}", created.id, ip_address)
        return created

    def change_password(
        self, user: User, data: ChangePasswordRequest, ip_address: Optional[str] = None
    ) -> None:
        if not verify_password(data.current_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña actual incorrecta")

        valid, msg = validate_password_strength(data.new_password)
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        user.hashed_password = hash_password(data.new_password)
        self.user_repo.update(user)
        self.audit_repo.create("change_password", "auth", "Contraseña actualizada", user.id, ip_address)


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.audit_repo = AuditLogRepository(db)

    def list_users(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[User]:
        return self.user_repo.get_all(skip, limit, search)

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return user

    def create_user(self, data: UserCreate, actor_id: Optional[int] = None) -> User:
        valid, msg = validate_password_strength(data.password)
        if not valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        if self.user_repo.get_by_email(data.email.lower()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya existe")

        roles = self._resolve_roles(data.role_ids)
        user = User(
            nombres=sanitize_string(data.nombres),
            apellidos=sanitize_string(data.apellidos),
            email=data.email.lower(),
            telefono=data.telefono,
            hashed_password=hash_password(data.password),
            estado=data.estado,
            roles=roles,
        )
        created = self.user_repo.create(user)
        self.audit_repo.create("create", "users", f"Usuario creado: {created.email}", actor_id)
        return created

    def update_user(self, user_id: int, data: UserUpdate, actor_id: Optional[int] = None) -> User:
        user = self.get_user(user_id)

        if data.email and data.email.lower() != user.email:
            existing = self.user_repo.get_by_email(data.email.lower())
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya existe")
            user.email = data.email.lower()

        if data.nombres is not None:
            user.nombres = sanitize_string(data.nombres)
        if data.apellidos is not None:
            user.apellidos = sanitize_string(data.apellidos)
        if data.telefono is not None:
            user.telefono = data.telefono
        if data.estado is not None:
            user.estado = data.estado
        if data.role_ids is not None:
            user.roles = self._resolve_roles(data.role_ids)

        updated = self.user_repo.update(user)
        self.audit_repo.create("update", "users", f"Usuario actualizado: {updated.email}", actor_id)
        return updated

    def delete_user(self, user_id: int, actor_id: Optional[int] = None) -> None:
        user = self.get_user(user_id)
        email = user.email
        self.user_repo.delete(user)
        self.audit_repo.create("delete", "users", f"Usuario eliminado: {email}", actor_id)

    def _resolve_roles(self, role_ids: List[int]) -> List[Role]:
        roles = []
        for role_id in role_ids:
            role = self.role_repo.get_by_id(role_id)
            if not role:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rol {role_id} no encontrado")
            roles.append(role)
        return roles


class RoleService:
    def __init__(self, db: Session):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)
        self.audit_repo = AuditLogRepository(db)

    def list_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        return self.role_repo.get_all(skip, limit)

    def get_role(self, role_id: int) -> Role:
        role = self.role_repo.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        return role

    def create_role(self, data: RoleCreate, actor_id: Optional[int] = None) -> Role:
        if self.role_repo.get_by_name(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El rol ya existe")

        permissions = self._resolve_permissions(data.permission_ids)
        role = Role(nombre=data.nombre, descripcion=data.descripcion, permissions=permissions)
        created = self.role_repo.create(role)
        self.audit_repo.create("create", "roles", f"Rol creado: {created.nombre}", actor_id)
        return created

    def update_role(self, role_id: int, data: RoleUpdate, actor_id: Optional[int] = None) -> Role:
        role = self.get_role(role_id)
        if data.nombre is not None:
            role.nombre = data.nombre
        if data.descripcion is not None:
            role.descripcion = data.descripcion
        if data.permission_ids is not None:
            role.permissions = self._resolve_permissions(data.permission_ids)

        updated = self.role_repo.update(role)
        self.audit_repo.create("update", "roles", f"Rol actualizado: {updated.nombre}", actor_id)
        return updated

    def delete_role(self, role_id: int, actor_id: Optional[int] = None) -> None:
        role = self.get_role(role_id)
        if role.nombre in ("Administrador", "Cliente"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar un rol del sistema")
        nombre = role.nombre
        self.role_repo.delete(role)
        self.audit_repo.create("delete", "roles", f"Rol eliminado: {nombre}", actor_id)

    def _resolve_permissions(self, permission_ids: List[int]) -> List[Permission]:
        permissions = []
        for perm_id in permission_ids:
            perm = self.permission_repo.get_by_id(perm_id)
            if not perm:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permiso {perm_id} no encontrado")
            permissions.append(perm)
        return permissions


class PermissionService:
    def __init__(self, db: Session):
        self.db = db
        self.permission_repo = PermissionRepository(db)
        self.audit_repo = AuditLogRepository(db)

    def list_permissions(
        self, skip: int = 0, limit: int = 100, modulo: Optional[str] = None
    ) -> List[Permission]:
        return self.permission_repo.get_all(skip, limit, modulo)

    def get_permission(self, permission_id: int) -> Permission:
        perm = self.permission_repo.get_by_id(permission_id)
        if not perm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permiso no encontrado")
        return perm

    def create_permission(self, data: PermissionCreate, actor_id: Optional[int] = None) -> Permission:
        if self.permission_repo.get_by_name(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El permiso ya existe")

        perm = Permission(nombre=data.nombre, modulo=data.modulo, descripcion=data.descripcion)
        created = self.permission_repo.create(perm)
        self.audit_repo.create("create", "permissions", f"Permiso creado: {created.nombre}", actor_id)
        return created

    def update_permission(
        self, permission_id: int, data: PermissionUpdate, actor_id: Optional[int] = None
    ) -> Permission:
        perm = self.get_permission(permission_id)
        if data.nombre is not None:
            perm.nombre = data.nombre
        if data.modulo is not None:
            perm.modulo = data.modulo
        if data.descripcion is not None:
            perm.descripcion = data.descripcion

        updated = self.permission_repo.update(perm)
        self.audit_repo.create("update", "permissions", f"Permiso actualizado: {updated.nombre}", actor_id)
        return updated

    def delete_permission(self, permission_id: int, actor_id: Optional[int] = None) -> None:
        perm = self.get_permission(permission_id)
        nombre = perm.nombre
        self.permission_repo.delete(perm)
        self.audit_repo.create("delete", "permissions", f"Permiso eliminado: {nombre}", actor_id)
