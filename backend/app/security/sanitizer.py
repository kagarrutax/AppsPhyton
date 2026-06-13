import re
from html import escape


def sanitize_string(value: str) -> str:
    cleaned = value.strip()
    return escape(cleaned)


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe incluir al menos una mayúscula"
    if not re.search(r"[a-z]", password):
        return False, "La contraseña debe incluir al menos una minúscula"
    if not re.search(r"\d", password):
        return False, "La contraseña debe incluir al menos un número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "La contraseña debe incluir al menos un carácter especial"
    return True, ""
