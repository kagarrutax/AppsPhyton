import io

import pytest


def _fake_jpeg():
    return io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01" + b"\x00" * 200)


def _checkout_order(client, client_token):
    products = client.get("/api/v1/products/public").json()
    client.post(
        "/api/v1/cart/items",
        headers={"Authorization": f"Bearer {client_token}"},
        json={"product_id": products[0]["id"], "cantidad": 1},
    )
    return client.post(
        "/api/v1/orders/checkout",
        headers={"Authorization": f"Bearer {client_token}"},
        json={},
    ).json()


def test_submit_payment_proof(client, client_token):
    order = _checkout_order(client, client_token)

    response = client.post(
        f"/api/v1/payments/orders/{order['id']}",
        headers={"Authorization": f"Bearer {client_token}"},
        files={"file": ("comprobante.jpg", _fake_jpeg(), "image/jpeg")},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "pendiente"
    assert data["order_id"] == order["id"]
    assert "/uploads/payments/" in data["comprobante"]


def test_approve_payment_generates_invoice_and_ticket(client, client_token, admin_token):
    order = _checkout_order(client, client_token)

    payment = client.post(
        f"/api/v1/payments/orders/{order['id']}",
        headers={"Authorization": f"Bearer {client_token}"},
        files={"file": ("comprobante.jpg", _fake_jpeg(), "image/jpeg")},
    ).json()

    approve = client.post(
        f"/api/v1/payments/{payment['id']}/approve",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert approve.status_code == 200
    assert approve.json()["estado"] == "aprobado"

    updated_order = client.get(
        f"/api/v1/orders/{order['id']}",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    assert updated_order["estado"] == "pagado"

    invoices = client.get(
        "/api/v1/invoices",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    assert len(invoices) >= 1
    assert invoices[0]["numero"].startswith("FAC-")

    tickets = client.get(
        "/api/v1/tickets",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    assert len(tickets) >= 1

    pdf = client.get(
        f"/api/v1/invoices/{invoices[0]['id']}/pdf",
        headers={"Authorization": f"Bearer {client_token}"},
    )
    assert pdf.status_code == 200
    assert pdf.headers["content-type"] == "application/pdf"


def test_reject_payment_keeps_order_pending(client, client_token, admin_token):
    order = _checkout_order(client, client_token)

    payment = client.post(
        f"/api/v1/payments/orders/{order['id']}",
        headers={"Authorization": f"Bearer {client_token}"},
        files={"file": ("comprobante.jpg", _fake_jpeg(), "image/jpeg")},
    ).json()

    reject = client.post(
        f"/api/v1/payments/{payment['id']}/reject",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"notas_rechazo": "Comprobante ilegible, envíe uno nuevo"},
    )
    assert reject.status_code == 200
    assert reject.json()["estado"] == "rechazado"

    updated_order = client.get(
        f"/api/v1/orders/{order['id']}",
        headers={"Authorization": f"Bearer {client_token}"},
    ).json()
    assert updated_order["estado"] == "pendiente"


def test_admin_lists_pending_payments(client, client_token, admin_token):
    order = _checkout_order(client, client_token)
    client.post(
        f"/api/v1/payments/orders/{order['id']}",
        headers={"Authorization": f"Bearer {client_token}"},
        files={"file": ("comprobante.jpg", _fake_jpeg(), "image/jpeg")},
    )

    pending = client.get(
        "/api/v1/payments/pending",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert pending.status_code == 200
    assert len(pending.json()) >= 1
