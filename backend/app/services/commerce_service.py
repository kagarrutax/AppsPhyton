from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.auth import User
from app.models.catalog import InventoryMovement, MovementType, Product
from app.models.commerce import (
    VALID_TRANSITIONS,
    Cart,
    CartItem,
    Order,
    OrderItem,
    OrderStatus,
    Purchase,
    PurchaseItem,
)
from app.repositories.audit_repository import AuditLogRepository
from app.repositories.catalog_repository import ProductRepository
from app.repositories.commerce_repository import CartRepository, OrderRepository, PurchaseRepository
from app.schemas.commerce import CartItemAdd, CartItemResponse, CartItemUpdate, CartResponse, OrderCreate, OrderStatusUpdate


def _is_admin(user: User) -> bool:
    return user.has_role("Administrador")


def _build_cart_response(cart: Cart) -> CartResponse:
    total = Decimal("0")
    items_response = []
    for item in cart.items:
        subtotal = Decimal(str(item.precio_unitario)) * item.cantidad
        total += subtotal
        items_response.append(
            CartItemResponse(
                id=item.id,
                product_id=item.product_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=subtotal,
                product=item.product,
            )
        )
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=items_response,
        total=total,
        cantidad_items=sum(i.cantidad for i in cart.items),
        fecha_actualizacion=cart.fecha_actualizacion,
    )


class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
        self.audit = AuditLogRepository(db)

    def _get_or_create_cart(self, user_id: int) -> Cart:
        cart = self.cart_repo.get_by_user_id(user_id)
        if not cart:
            cart = self.cart_repo.create_cart(Cart(user_id=user_id))
        return cart

    def _validate_product(self, product_id: int, cantidad: int) -> Product:
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.estado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no disponible")
        if product.stock < cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {product.nombre}. Disponible: {product.stock}",
            )
        return product

    def get_cart(self, user: User) -> CartResponse:
        cart = self._get_or_create_cart(user.id)
        return _build_cart_response(cart)

    def add_item(self, user: User, data: CartItemAdd) -> CartResponse:
        product = self._validate_product(data.product_id, data.cantidad)
        cart = self._get_or_create_cart(user.id)
        existing = self.cart_repo.get_item(cart.id, data.product_id)

        if existing:
            new_qty = existing.cantidad + data.cantidad
            self._validate_product(data.product_id, new_qty)
            existing.cantidad = new_qty
        else:
            cart.items.append(
                CartItem(
                    product_id=data.product_id,
                    cantidad=data.cantidad,
                    precio_unitario=product.precio,
                )
            )

        self.cart_repo.save()
        self.cart_repo.refresh(cart)
        self.audit.create("add_item", "cart", f"Producto #{data.product_id} x{data.cantidad}", user.id)
        return _build_cart_response(cart)

    def update_item(self, user: User, product_id: int, data: CartItemUpdate) -> CartResponse:
        self._validate_product(product_id, data.cantidad)
        cart = self._get_or_create_cart(user.id)
        item = self.cart_repo.get_item(cart.id, product_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no está en el carrito")

        item.cantidad = data.cantidad
        self.cart_repo.save()
        self.cart_repo.refresh(cart)
        self.audit.create("update_item", "cart", f"Producto #{product_id} cantidad={data.cantidad}", user.id)
        return _build_cart_response(cart)

    def remove_item(self, user: User, product_id: int) -> CartResponse:
        cart = self._get_or_create_cart(user.id)
        item = self.cart_repo.get_item(cart.id, product_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no está en el carrito")

        self.cart_repo.delete_item(item)
        self.cart_repo.refresh(cart)
        self.audit.create("remove_item", "cart", f"Producto #{product_id} eliminado", user.id)
        return _build_cart_response(cart)

    def clear_cart(self, user: User) -> CartResponse:
        cart = self._get_or_create_cart(user.id)
        cart.items.clear()
        self.cart_repo.save()
        self.cart_repo.refresh(cart)
        self.audit.create("clear", "cart", "Carrito vaciado", user.id)
        return _build_cart_response(cart)


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.cart_repo = CartRepository(db)
        self.purchase_repo = PurchaseRepository(db)
        self.product_repo = ProductRepository(db)
        self.audit = AuditLogRepository(db)

    def list_orders(
        self,
        user: User,
        skip: int = 0,
        limit: int = 100,
        estado: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> List[Order]:
        filter_user = None if _is_admin(user) else user.id
        if _is_admin(user) and user_id:
            filter_user = user_id
        return self.order_repo.get_all(skip, limit, filter_user, estado)

    def get_order(self, order_id: int, user: User) -> Order:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
        if not _is_admin(user) and order.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return order

    def checkout(self, user: User, data: OrderCreate) -> Order:
        cart = self.cart_repo.get_by_user_id(user.id)
        if not cart or not cart.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El carrito está vacío")

        order_items = []
        total = Decimal("0")

        for cart_item in cart.items:
            product = self.product_repo.get_by_id(cart_item.product_id)
            if not product or not product.estado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Producto {cart_item.product_id} no disponible",
                )
            if product.stock < cart_item.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para {product.nombre}",
                )
            subtotal = Decimal(str(cart_item.precio_unitario)) * cart_item.cantidad
            total += subtotal
            order_items.append(
                OrderItem(
                    product_id=product.id,
                    product_nombre=product.nombre,
                    cantidad=cart_item.cantidad,
                    precio_unitario=cart_item.precio_unitario,
                    subtotal=subtotal,
                )
            )

        order = Order(
            user_id=user.id,
            estado=OrderStatus.PENDIENTE.value,
            total=total,
            notas=data.notas,
            items=order_items,
        )
        created = self.order_repo.create(order)

        cart.items.clear()
        self.cart_repo.save()

        self.audit.create("checkout", "orders", f"Pedido #{created.id} - Total {total}", user.id)
        return created

    def update_status(self, order_id: int, data: OrderStatusUpdate, user: User) -> Order:
        order = self.get_order(order_id, user)
        if not _is_admin(user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")

        new_status = OrderStatus(data.estado)
        current = OrderStatus(order.estado)

        if new_status == current:
            return order

        allowed = VALID_TRANSITIONS.get(current, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cambiar de '{current.value}' a '{new_status.value}'",
            )

        if new_status == OrderStatus.PAGADO:
            self._process_payment(order, user.id)
        elif new_status == OrderStatus.CANCELADO and current in (
            OrderStatus.PAGADO,
            OrderStatus.VERIFICADO,
            OrderStatus.PREPARANDO,
            OrderStatus.LISTO,
        ):
            self._reverse_payment(order, user.id)

        order.estado = new_status.value
        updated = self.order_repo.update(order)
        self.audit.create("update_status", "orders", f"Pedido #{order_id} -> {new_status.value}", user.id)
        return updated

    def delete_order(self, order_id: int, user: User) -> None:
        order = self.get_order(order_id, user)
        if not _is_admin(user):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")
        if order.estado not in (OrderStatus.PENDIENTE.value, OrderStatus.CANCELADO.value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar pedidos pendientes o cancelados",
            )
        self.order_repo.delete(order)
        self.audit.create("delete", "orders", f"Pedido #{order_id} eliminado", user.id)

    def _process_payment(self, order: Order, actor_id: int) -> None:
        if self.purchase_repo.get_by_order_id(order.id):
            return

        for item in order.items:
            product = self.product_repo.get_by_id(item.product_id) if item.product_id else None
            if not product:
                continue
            if product.stock < item.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para {item.product_nombre}",
                )
            stock_anterior = product.stock
            product.stock -= item.cantidad
            self.product_repo.update(product)
            movement = InventoryMovement(
                product_id=product.id,
                user_id=actor_id,
                tipo=MovementType.SALIDA.value,
                cantidad=item.cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=product.stock,
                motivo=f"Venta pedido #{order.id}",
            )
            self.db.add(movement)

        purchase_items = [
            PurchaseItem(
                product_id=item.product_id,
                product_nombre=item.product_nombre,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=item.subtotal,
            )
            for item in order.items
        ]
        purchase = Purchase(
            user_id=order.user_id,
            order_id=order.id,
            total=order.total,
            items=purchase_items,
        )
        self.db.add(purchase)
        self.db.commit()

    def _reverse_payment(self, order: Order, actor_id: int) -> None:
        purchase = self.purchase_repo.get_by_order_id(order.id)
        for item in order.items:
            if not item.product_id:
                continue
            product = self.product_repo.get_by_id(item.product_id)
            if not product:
                continue
            stock_anterior = product.stock
            product.stock += item.cantidad
            self.product_repo.update(product)
            movement = InventoryMovement(
                product_id=product.id,
                user_id=actor_id,
                tipo=MovementType.ENTRADA.value,
                cantidad=item.cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=product.stock,
                motivo=f"Cancelación pedido #{order.id}",
            )
            self.db.add(movement)

        if purchase:
            self.purchase_repo.delete(purchase)
        self.db.commit()


class PurchaseService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PurchaseRepository(db)
        self.audit = AuditLogRepository(db)

    def list_purchases(
        self, user: User, skip: int = 0, limit: int = 100, user_id: Optional[int] = None
    ) -> List[Purchase]:
        filter_user = None if _is_admin(user) else user.id
        if _is_admin(user) and user_id:
            filter_user = user_id
        return self.repo.get_all(skip, limit, filter_user)

    def get_purchase(self, purchase_id: int, user: User) -> Purchase:
        purchase = self.repo.get_by_id(purchase_id)
        if not purchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra no encontrada")
        if not _is_admin(user) and purchase.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return purchase
