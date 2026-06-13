def test_list_public_products(client):
    response = client.get("/api/v1/products/public")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1
    assert all(p["estado"] is True for p in products)


def test_create_product_as_admin(client, admin_token):
    categories = client.get(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    category_id = categories[0]["id"]

    response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nombre": "Nuevo Producto Test",
            "descripcion": "Descripción test",
            "precio": "12.50",
            "stock": 20,
            "stock_minimo": 5,
            "category_id": category_id,
            "estado": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Nuevo Producto Test"
    assert float(data["precio"]) == 12.50


def test_activate_deactivate_product(client, admin_token):
    products = client.get(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    product_id = products[0]["id"]

    deactivate = client.patch(
        f"/api/v1/products/{product_id}/deactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert deactivate.status_code == 200
    assert deactivate.json()["estado"] is False

    activate = client.patch(
        f"/api/v1/products/{product_id}/activate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert activate.status_code == 200
    assert activate.json()["estado"] is True


def test_inventory_entry_movement(client, admin_token):
    products = client.get(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    product = products[0]
    stock_before = product["stock"]

    response = client.post(
        "/api/v1/inventory/movements",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "product_id": product["id"],
            "tipo": "entrada",
            "cantidad": 10,
            "motivo": "Reposición de stock",
        },
    )
    assert response.status_code == 201
    movement = response.json()
    assert movement["stock_anterior"] == stock_before
    assert movement["stock_nuevo"] == stock_before + 10

    updated = client.get(
        f"/api/v1/products/{product['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert updated["stock"] == stock_before + 10


def test_inventory_exit_insufficient_stock(client, admin_token):
    response = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "nombre": "Producto Stock Bajo",
            "precio": "5.00",
            "stock": 2,
            "stock_minimo": 5,
            "estado": True,
        },
    )
    product_id = response.json()["id"]

    exit_response = client.post(
        "/api/v1/inventory/movements",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "product_id": product_id,
            "tipo": "salida",
            "cantidad": 10,
            "motivo": "Venta",
        },
    )
    assert exit_response.status_code == 400


def test_list_low_stock_products(client, admin_token):
    response = client.get(
        "/api/v1/products/low-stock",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    products = response.json()
    assert all(p["stock"] <= p["stock_minimo"] for p in products)


def test_list_inventory_movements(client, admin_token):
    response = client.get(
        "/api/v1/inventory/movements",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
