"""Tests del panel administrativo: categorías, usuarios, dashboard y pedidos globales."""


def test_category_crud_as_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    create = client.post(
        "/api/v1/categories",
        headers=headers,
        json={"nombre": "Categoría Test", "descripcion": "Para pruebas", "estado": True},
    )
    assert create.status_code == 201
    category_id = create.json()["id"]

    update = client.put(
        f"/api/v1/categories/{category_id}",
        headers=headers,
        json={"nombre": "Categoría Actualizada", "estado": False},
    )
    assert update.status_code == 200
    assert update.json()["nombre"] == "Categoría Actualizada"
    assert update.json()["estado"] is False

    listed = client.get("/api/v1/categories", headers=headers)
    assert listed.status_code == 200
    assert any(c["id"] == category_id for c in listed.json())

    delete = client.delete(f"/api/v1/categories/{category_id}", headers=headers)
    assert delete.status_code == 200


def test_category_crud_forbidden_for_client(client, client_token):
    response = client.post(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"nombre": "Sin permiso", "estado": True},
    )
    assert response.status_code == 403


def test_admin_lists_all_orders(client, admin_token, client_token):
    products = client.get("/api/v1/products/public").json()
    product_id = products[0]["id"]

    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": product_id, "cantidad": 1},
    )
    client.post(
        "/api/v1/orders/checkout",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"notas": "Pedido admin test"},
    )

    response = client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) >= 1
    assert any(o.get("notas") == "Pedido admin test" for o in orders)


def test_admin_deactivate_user(client, admin_token, client_token):
    users = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    client_user = next(u for u in users if u["email"] == "maria@test.com")

    response = client.put(
        f"/api/v1/users/{client_user['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": False},
    )
    assert response.status_code == 200
    assert response.json()["estado"] is False


def test_dashboard_full_schema(client, admin_token):
    response = client.get(
        "/api/v1/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()

    required = [
        "total_usuarios",
        "total_productos",
        "total_pedidos",
        "pagos_pendientes",
        "productos_stock_bajo",
        "ventas_totales",
        "pedidos_por_estado",
        "pagos_pendientes_recientes",
        "productos_stock_bajo_lista",
        "pedidos_recientes",
    ]
    for key in required:
        assert key in data, f"Falta campo {key} en dashboard"

    assert isinstance(data["pedidos_por_estado"], dict)
    assert isinstance(data["pagos_pendientes_recientes"], list)
    assert isinstance(data["pedidos_recientes"], list)
