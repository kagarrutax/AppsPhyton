def test_list_audit_logs_as_admin(client, admin_token):
    response = client.get(
        "/api/v1/audit-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    logs = response.json()
    assert isinstance(logs, list)
    assert len(logs) >= 1
    assert "accion" in logs[0]
    assert "modulo" in logs[0]


def test_audit_logs_forbidden_for_client(client, client_token):
    response = client.get(
        "/api/v1/audit-logs",
        headers={"Authorization": f"Bearer {client_token}"},
    )
    assert response.status_code == 403


def test_audit_logs_filter_by_modulo(client, admin_token):
    response = client.get(
        "/api/v1/audit-logs",
        headers={"Authorization": f"Bearer {admin_token}"},
        params={"modulo": "auth"},
    )
    assert response.status_code == 200
    logs = response.json()
    assert all(log["modulo"] == "auth" for log in logs)


def test_health_check_extended(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ok", "degraded", "error")
    assert "database" in data
    assert "connected" in data["database"]
    assert "migration" in data
    assert "up_to_date" in data["migration"]
