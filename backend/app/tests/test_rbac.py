from app.permissions.rbac import CLIENTE_PERMISSIONS, get_all_system_permissions


def test_system_permissions_generated():
    permissions = get_all_system_permissions()
    assert len(permissions) > 0
    names = {p["nombre"] for p in permissions}
    assert "users.create" in names
    assert "orders.approve" in names


def test_cliente_permissions_subset():
    all_names = {p["nombre"] for p in get_all_system_permissions()}
    for perm in CLIENTE_PERMISSIONS:
        assert perm in all_names
