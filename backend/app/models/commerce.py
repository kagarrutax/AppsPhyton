from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.datetime_utils import utc_now


class OrderStatus(str, Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    VERIFICADO = "verificado"
    PREPARANDO = "preparando"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


VALID_TRANSITIONS = {
    OrderStatus.PENDIENTE: [OrderStatus.PAGADO, OrderStatus.CANCELADO],
    OrderStatus.PAGADO: [OrderStatus.VERIFICADO, OrderStatus.CANCELADO],
    OrderStatus.VERIFICADO: [OrderStatus.PREPARANDO, OrderStatus.CANCELADO],
    OrderStatus.PREPARANDO: [OrderStatus.LISTO, OrderStatus.CANCELADO],
    OrderStatus.LISTO: [OrderStatus.ENTREGADO, OrderStatus.CANCELADO],
    OrderStatus.ENTREGADO: [],
    OrderStatus.CANCELADO: [],
}


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    fecha_actualizacion = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan", lazy="selectin")


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),)

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", lazy="selectin")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    estado = Column(String(20), nullable=False, default=OrderStatus.PENDIENTE.value, index=True)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=utc_now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User", lazy="selectin")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin")
    purchase = relationship("Purchase", back_populates="order", uselist=False)
    payments = relationship("Payment", back_populates="order", lazy="selectin")
    invoice = relationship("Invoice", back_populates="order", uselist=False)
    ticket = relationship("Ticket", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    product_nombre = Column(String(150), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, unique=True)
    total = Column(Numeric(10, 2), nullable=False)
    fecha = Column(DateTime, default=utc_now, nullable=False)

    user = relationship("User", lazy="selectin")
    order = relationship("Order", back_populates="purchase")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan", lazy="selectin")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    product_nombre = Column(String(150), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product")
