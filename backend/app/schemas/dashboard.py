from decimal import Decimal
from typing import Dict, List

from pydantic import BaseModel, ConfigDict

from app.schemas.billing import PaymentResponse
from app.schemas.catalog import ProductResponse
from app.schemas.commerce import OrderResponse


class DashboardStatsResponse(BaseModel):
    total_usuarios: int
    total_productos: int
    total_pedidos: int
    pagos_pendientes: int
    productos_stock_bajo: int
    ventas_totales: Decimal
    pedidos_por_estado: Dict[str, int]
    pagos_pendientes_recientes: List[PaymentResponse] = []
    productos_stock_bajo_lista: List[ProductResponse] = []
    pedidos_recientes: List[OrderResponse] = []
