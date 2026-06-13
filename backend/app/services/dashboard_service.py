from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.auth import User
from app.models.billing import Payment, PaymentStatus
from app.models.catalog import Product
from app.models.commerce import Order
from app.services.billing_service import PaymentService
from app.services.catalog_service import ProductService
from app.services.commerce_service import OrderService


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self, current_user: User) -> dict:
        total_usuarios = self.db.query(func.count(User.id)).scalar() or 0
        total_productos = self.db.query(func.count(Product.id)).scalar() or 0
        total_pedidos = self.db.query(func.count(Order.id)).scalar() or 0
        pagos_pendientes = (
            self.db.query(func.count(Payment.id))
            .filter(Payment.estado == PaymentStatus.PENDIENTE.value)
            .scalar()
            or 0
        )
        ventas_totales = (
            self.db.query(func.coalesce(func.sum(Payment.monto), 0))
            .filter(Payment.estado == PaymentStatus.APROBADO.value)
            .scalar()
            or Decimal("0")
        )

        status_rows = self.db.query(Order.estado, func.count(Order.id)).group_by(Order.estado).all()
        pedidos_por_estado = {estado: count for estado, count in status_rows}

        product_service = ProductService(self.db)
        low_stock = product_service.get_low_stock()

        payment_service = PaymentService(self.db)
        pending_payments = payment_service.list_pending(current_user)[:5]

        order_service = OrderService(self.db)
        recent_orders = order_service.list_orders(current_user, skip=0, limit=5)

        return {
            "total_usuarios": total_usuarios,
            "total_productos": total_productos,
            "total_pedidos": total_pedidos,
            "pagos_pendientes": pagos_pendientes,
            "productos_stock_bajo": len(low_stock),
            "ventas_totales": ventas_totales,
            "pedidos_por_estado": pedidos_por_estado,
            "pagos_pendientes_recientes": pending_payments,
            "productos_stock_bajo_lista": low_stock[:5],
            "pedidos_recientes": recent_orders,
        }
