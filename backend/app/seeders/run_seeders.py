import argparse

from app.core.database import SessionLocal
from app.seeders.initial_seeder import run_seeders


def main():
    parser = argparse.ArgumentParser(description="Ejecutar seeders iniciales")
    parser.parse_args()

    db = SessionLocal()
    try:
        run_seeders(db)
        print("Seeders ejecutados correctamente.")
        print("Admin: admin@admin.com / Admin123*")
    finally:
        db.close()


if __name__ == "__main__":
    main()
