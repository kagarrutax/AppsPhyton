from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.commerce import Cart, CartItem, Order, OrderStatus, Purchase, PurchaseItem


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        return self.db.query(Cart).filter(Cart.user_id == user_id).first()

    def get_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        return (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
            .first()
        )

    def create_cart(self, cart: Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def save(self) -> None:
        self.db.commit()

    def refresh(self, obj) -> None:
        self.db.refresh(obj)

    def delete_item(self, item: CartItem) -> None:
        self.db.delete(item)
        self.db.commit()


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Order]:
        query = self.db.query(Order)
        if user_id:
            query = query.filter(Order.user_id == user_id)
        if estado:
            query = query.filter(Order.estado == estado)
        return query.order_by(Order.fecha_creacion.desc()).offset(skip).limit(limit).all()

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()


class PurchaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, purchase_id: int) -> Optional[Purchase]:
        return self.db.query(Purchase).filter(Purchase.id == purchase_id).first()

    def get_by_order_id(self, order_id: int) -> Optional[Purchase]:
        return self.db.query(Purchase).filter(Purchase.order_id == order_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
    ) -> List[Purchase]:
        query = self.db.query(Purchase)
        if user_id:
            query = query.filter(Purchase.user_id == user_id)
        return query.order_by(Purchase.fecha.desc()).offset(skip).limit(limit).all()

    def create(self, purchase: Purchase) -> Purchase:
        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)
        return purchase

    def delete(self, purchase: Purchase) -> None:
        self.db.delete(purchase)
        self.db.commit()
