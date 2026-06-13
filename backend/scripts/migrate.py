"""CLI unificado: migraciones Alembic + seeders."""

import argparse
import subprocess
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> int:
    print(f">>> {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=BACKEND_ROOT)


def cmd_upgrade(_: argparse.Namespace) -> int:
    return _run([sys.executable, "-m", "alembic", "upgrade", "head"])


def cmd_downgrade(args: argparse.Namespace) -> int:
    target = args.target or "-1"
    return _run([sys.executable, "-m", "alembic", "downgrade", target])


def cmd_current(_: argparse.Namespace) -> int:
    return _run([sys.executable, "-m", "alembic", "current"])


def cmd_history(_: argparse.Namespace) -> int:
    return _run([sys.executable, "-m", "alembic", "history", "--verbose"])


def cmd_seed(_: argparse.Namespace) -> int:
    return _run([sys.executable, "-m", "app.seeders.run_seeders"])


def cmd_setup(_: argparse.Namespace) -> int:
    steps = [
        cmd_upgrade(_),
        cmd_seed(_),
        cmd_current(_),
    ]
    return max(steps)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gestión de migraciones FastFood Platform")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("upgrade", help="Aplicar migraciones (alembic upgrade head)").set_defaults(
        func=cmd_upgrade
    )
    sub.add_parser("current", help="Ver revisión actual").set_defaults(func=cmd_current)
    sub.add_parser("history", help="Ver historial de migraciones").set_defaults(func=cmd_history)
    sub.add_parser("seed", help="Ejecutar seeders iniciales").set_defaults(func=cmd_seed)
    sub.add_parser("setup", help="Migrar + seeders (instalación completa)").set_defaults(func=cmd_setup)

    down = sub.add_parser("downgrade", help="Revertir migraciones")
    down.add_argument("target", nargs="?", default="-1", help="Revisión destino (default: -1)")
    down.set_defaults(func=cmd_downgrade)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
