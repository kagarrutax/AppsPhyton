def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ok", "degraded")
    assert data["database"]["connected"] is True


def test_admin_login(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@admin.com", "password": "Admin123*"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@admin.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_register_client(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "nombres": "Juan",
            "apellidos": "Pérez",
            "email": "juan@test.com",
            "telefono": "5551234",
            "password": "Cliente123*",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "juan@test.com"
    assert any(r["nombre"] == "Cliente" for r in data["roles"])


def test_get_me_authenticated(client, admin_token):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "admin@admin.com"


def test_list_users_requires_auth(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 401


def test_list_users_as_admin(client, admin_token):
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1


def test_list_roles_as_admin(client, admin_token):
    response = client.get(
        "/api/v1/roles",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    roles = response.json()
    role_names = [r["nombre"] for r in roles]
    assert "Administrador" in role_names
    assert "Cliente" in role_names


def test_list_permissions_as_admin(client, admin_token):
    response = client.get(
        "/api/v1/permissions",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    permissions = response.json()
    assert len(permissions) > 0
    assert any(p["nombre"] == "users.read" for p in permissions)
