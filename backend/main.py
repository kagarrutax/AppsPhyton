from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.config import get_settings
from app.core.database import SessionLocal
from sqlalchemy import text

from app.core.database import engine
from app.core.migration import get_current_revision, get_head_revision, verify_database_migrated
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routes import (
    audit_router,
    auth_router,
    dashboard_router,
    cart_router,
    category_router,
    inventory_router,
    invoice_router,
    order_router,
    payment_router,
    permission_router,
    product_router,
    purchase_router,
    role_router,
    ticket_router,
    user_router,
)
from app.seeders.initial_seeder import run_seeders

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.app_env != "test":
        verify_database_migrated()
        Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
        db = SessionLocal()
        try:
            run_seeders(db)
        finally:
            db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Plataforma de gestión y venta de comida rápida - API REST",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(role_router, prefix="/api/v1")
app.include_router(permission_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(cart_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(purchase_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")
app.include_router(ticket_router, prefix="/api/v1")

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


@app.get("/api/v1/health", tags=["Sistema"])
@limiter.limit(settings.rate_limit)
def health_check(request: Request):
    db_connected = False
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            db_connected = True
    except Exception:
        db_connected = False

    current_rev = None
    head_rev = None
    migration_up_to_date = False
    try:
        current_rev = get_current_revision()
        head_rev = get_head_revision()
        migration_up_to_date = current_rev is not None and current_rev == head_rev
    except Exception:
        pass

    if not db_connected:
        status = "error"
    elif not migration_up_to_date:
        status = "degraded"
    else:
        status = "ok"

    return {
        "status": status,
        "app": settings.app_name,
        "env": settings.app_env,
        "database": {"connected": db_connected},
        "migration": {
            "current": current_rev,
            "head": head_rev,
            "up_to_date": migration_up_to_date,
        },
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if settings.debug:
        raise exc
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
