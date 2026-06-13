from app.security.password import hash_password, verify_password
from app.security.sanitizer import validate_password_strength


def test_hash_and_verify_password():
    hashed = hash_password("Admin123*")
    assert verify_password("Admin123*", hashed)
    assert not verify_password("wrong", hashed)


def test_password_strength_validation():
    valid, _ = validate_password_strength("Admin123*")
    assert valid is True

    valid, msg = validate_password_strength("weak")
    assert valid is False
    assert "8 caracteres" in msg
