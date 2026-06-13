from sqlalchemy.orm import Session

from app.models.auth import Permission, Role, User
from app.permissions.rbac import CLIENTE_PERMISSIONS, get_all_system_permissions
from app.seeders.catalog_seeder import seed_catalog
from app.repositories.auth_repository import PermissionRepository, RoleRepository, UserRepository
from app.security.password import hash_password

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "Admin123*"


def run_seeders(db: Session) -> None:
    _seed_permissions(db)
    _seed_roles(db)
    _seed_admin(db)
    seed_catalog(db)


def _seed_permissions(db: Session) -> None:
    repo = PermissionRepository(db)
    for perm_data in get_all_system_permissions():
        if not repo.get_by_name(perm_data["nombre"]):
            repo.create(Permission(**perm_data))


def _seed_roles(db: Session) -> None:
    perm_repo = PermissionRepository(db)
    role_repo = RoleRepository(db)
    all_permissions = perm_repo.get_all(limit=500)

    admin_role = role_repo.get_by_name("Administrador")
    if not admin_role:
        admin_role = Role(
            nombre="Administrador",
            descripcion="Acceso total al sistema",
            permissions=all_permissions,
        )
        role_repo.create(admin_role)
    else:
        admin_role.permissions = all_permissions
        role_repo.update(admin_role)

    cliente_role = role_repo.get_by_name("Cliente")
    if not cliente_role:
        cliente_perms = [p for p in all_permissions if p.nombre in CLIENTE_PERMISSIONS]
        cliente_role = Role(
            nombre="Cliente",
            descripcion="Usuario final con permisos de compra",
            permissions=cliente_perms,
        )
        role_repo.create(cliente_role)
    else:
        cliente_perms = [p for p in all_permissions if p.nombre in CLIENTE_PERMISSIONS]
        cliente_role.permissions = cliente_perms
        role_repo.update(cliente_role)


def _seed_admin(db: Session) -> None:
    user_repo = UserRepository(db)
    role_repo = RoleRepository(db)

    if user_repo.get_by_email(ADMIN_EMAIL):
        return

    admin_role = role_repo.get_by_name("Administrador")
    if not admin_role:
        raise RuntimeError("Rol Administrador no encontrado. Ejecute seeders de roles primero.")

    admin = User(
        nombres="Administrador",
        apellidos="Sistema",
        email=ADMIN_EMAIL,
        telefono=None,
        hashed_password=hash_password(ADMIN_PASSWORD),
        estado=True,
        roles=[admin_role],
    )
    user_repo.create(admin)
