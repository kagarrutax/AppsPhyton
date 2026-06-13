from datetime import datetime, timezone


def utc_now() -> datetime:
    """Datetime UTC naive (compatible con columnas MySQL existentes)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
