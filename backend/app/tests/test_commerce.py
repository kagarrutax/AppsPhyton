def test_add_to_cart(client, client_token):
    products = client.get("/api/v1/products/public").json()
    product_id = products[0]["id"]

    response = client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": product_id, "cantidad": 2},
    )
    assert response.status_code == 200
    cart = response.json()
    assert cart["cantidad_items"] == 2
    assert float(cart["total"]) > 0


def test_update_cart_quantity(client, client_token):
    products = client.get("/api/v1/products/public").json()
    product_id = products[0]["id"]

    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": product_id, "cantidad": 1},
    )
    response = client.put(
        f"/api/v1/cart/items/{product_id}",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"cantidad": 3},
    )
    assert response.status_code == 200
    assert response.json()["cantidad_items"] == 3


def test_checkout_creates_order(client, client_token):
    products = client.get("/api/v1/products/public").json()
    product_id = products[0]["id"]

    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": product_id, "cantidad": 1},
    )

    response = client.post(
        "/api/v1/orders/checkout",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"notas": "Sin cebolla"},
    )
    assert response.status_code == 201
    order = response.json()
    assert order["estado"] == "pendiente"
    assert len(order["items"]) == 1
    assert order["notas"] == "Sin cebolla"

    cart = client.get(
        "/api/v1/cart",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    assert cart["cantidad_items"] == 0


def test_order_status_flow(client, client_token, admin_token):
    products = client.get("/api/v1/products/public").json()
    product_id = products[0]["id"]

    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": product_id, "cantidad": 1},
    )
    order = client.post(
        "/api/v1/orders/checkout",
        headers={"Authorization": f"Bearer {client_token}"},
        json={},
    ).json()
    order_id = order["id"]

    product_before = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    stock_before = product_before["stock"]

    pay = client.patch(
        f"/api/v1/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": "pagado"},
    )
    assert pay.status_code == 200
    assert pay.json()["estado"] == "pagado"

    product_after = client.get(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()
    assert product_after["stock"] == stock_before - 1

    purchases = client.get(
        "/api/v1/purchases",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    assert len(purchases) >= 1
    assert float(purchases[0]["total"]) == float(order["total"])


def test_invalid_status_transition(client, client_token, admin_token):
    products = client.get("/api/v1/products/public").json()
    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": products[0]["id"], "cantidad": 1},
    )
    order_id = client.post(
        "/api/v1/orders/checkout",
        headers={"Authorization": f"Bearer {client_token}"},
        json={},
    ).json()["id"]

    response = client.patch(
        f"/api/v1/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"estado": "entregado"},
    )
    assert response.status_code == 400


def test_client_sees_own_orders_only(client, client_token, admin_token):
    products = client.get("/api/v1/products/public").json()
    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": products[0]["id"], "cantidad": 1},
    )
    client.post(
        "/api/v1/orders/checkout",
        headers={"Authorization": f"Bearer {client_token}"},
        json={},
    )

    client_orders = client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    admin_orders = client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()

    assert len(client_orders) >= 1
    assert len(admin_orders) >= len(client_orders)
