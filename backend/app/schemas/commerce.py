from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CartItemAdd(BaseModel):
    product_id: int
    cantidad: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    cantidad: int = Field(..., gt=0)


class ProductSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    precio: Decimal
    imagen: Optional[str] = None
    estado: bool


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    product: Optional[ProductSummary] = None


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    items: List[CartItemResponse] = []
    total: Decimal = Decimal("0")
    cantidad_items: int = 0
    fecha_actualizacion: datetime


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: Optional[int] = None
    product_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal


class OrderCreate(BaseModel):
    notas: Optional[str] = None


class OrderUpdate(BaseModel):
    estado: Optional[str] = None
    notas: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    estado: str = Field(..., pattern="^(pendiente|pagado|verificado|preparando|listo|entregado|cancelado)$")


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    estado: str
    total: Decimal
    notas: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    items: List[OrderItemResponse] = []


class PurchaseItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: Optional[int] = None
    product_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal


class PurchaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    order_id: Optional[int] = None
    total: Decimal
    fecha: datetime
    items: List[PurchaseItemResponse] = []
