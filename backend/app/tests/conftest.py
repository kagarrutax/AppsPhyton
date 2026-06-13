import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-min-32-chars!!")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import clear_settings_cache
from app.core.database import Base, get_db
from app.seeders.initial_seeder import run_seeders

clear_settings_cache()

from main import app  # noqa: E402

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        run_seeders(db)
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@admin.com", "password": "Admin123*"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def client_token(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "nombres": "María",
            "apellidos": "Cliente",
            "email": "maria@test.com",
            "telefono": "5559999",
            "password": "Cliente123*",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "maria@test.com", "password": "Cliente123*"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
