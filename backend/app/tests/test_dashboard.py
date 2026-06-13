def test_dashboard_stats_as_admin(client, admin_token):
    response = client.get(
        "/api/v1/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_usuarios" in data
    assert "ventas_totales" in data
    assert "pedidos_por_estado" in data


def test_dashboard_forbidden_for_client(client, client_token):
    response = client.get(
        "/api/v1/dashboard",
        headers={"Authorization": f"Bearer {client_token}"},
    )
    assert response.status_code == 403
