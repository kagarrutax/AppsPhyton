"""Utilidades para verificar el estado de migraciones Alembic."""

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from app.core.database import engine


def get_current_revision() -> str | None:
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        return context.get_current_revision()


def get_head_revision() -> str | None:
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    return script.get_current_head()


def is_database_migrated() -> bool:
    return get_current_revision() == get_head_revision()


def verify_database_migrated() -> None:
    current = get_current_revision()
    head = get_head_revision()

    if current is None:
        raise RuntimeError(
            "La base de datos no tiene migraciones aplicadas. "
            "Ejecute: alembic upgrade head"
        )

    if current != head:
        raise RuntimeError(
            f"La base de datos está desactualizada (actual: {current}, head: {head}). "
            "Ejecute: alembic upgrade head"
        )
