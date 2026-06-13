from app.routes.audit_routes import router as audit_router
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.cart_routes import router as cart_router
from app.routes.category_routes import router as category_router
from app.routes.inventory_routes import router as inventory_router
from app.routes.invoice_routes import router as invoice_router
from app.routes.order_routes import router as order_router
from app.routes.payment_routes import router as payment_router
from app.routes.permission_routes import router as permission_router
from app.routes.product_routes import router as product_router
from app.routes.purchase_routes import router as purchase_router
from app.routes.role_routes import router as role_router
from app.routes.ticket_routes import router as ticket_router
from app.routes.user_routes import router as user_router

__all__ = [
    "audit_router",
    "auth_router",
    "dashboard_router",
    "user_router",
    "role_router",
    "permission_router",
    "category_router",
    "product_router",
    "inventory_router",
    "cart_router",
    "order_router",
    "purchase_router",
    "payment_router",
    "invoice_router",
    "ticket_router",
]
