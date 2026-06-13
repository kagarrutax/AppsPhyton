from typing import List, Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.catalog import Category, InventoryMovement, MovementType, Product
from app.repositories.audit_repository import AuditLogRepository
from app.repositories.catalog_repository import CategoryRepository, InventoryRepository, ProductRepository
from app.schemas.catalog import (
    CategoryCreate,
    CategoryUpdate,
    InventoryMovementCreate,
    ProductCreate,
    ProductUpdate,
)
from app.security.sanitizer import sanitize_string
from app.services.upload_service import delete_product_image, save_product_image


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CategoryRepository(db)
        self.audit = AuditLogRepository(db)

    def list_categories(self, skip: int = 0, limit: int = 100, only_active: bool = False) -> List[Category]:
        return self.repo.get_all(skip, limit, only_active)

    def get_category(self, category_id: int) -> Category:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        return category

    def create_category(self, data: CategoryCreate, actor_id: Optional[int] = None) -> Category:
        if self.repo.get_by_name(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La categoría ya existe")

        category = Category(
            nombre=sanitize_string(data.nombre),
            descripcion=data.descripcion,
            estado=data.estado,
        )
        created = self.repo.create(category)
        self.audit.create("create", "categories", f"Categoría: {created.nombre}", actor_id)
        return created

    def update_category(self, category_id: int, data: CategoryUpdate, actor_id: Optional[int] = None) -> Category:
        category = self.get_category(category_id)
        if data.nombre is not None:
            category.nombre = sanitize_string(data.nombre)
        if data.descripcion is not None:
            category.descripcion = data.descripcion
        if data.estado is not None:
            category.estado = data.estado
        updated = self.repo.update(category)
        self.audit.create("update", "categories", f"Categoría: {updated.nombre}", actor_id)
        return updated

    def delete_category(self, category_id: int, actor_id: Optional[int] = None) -> None:
        category = self.get_category(category_id)
        nombre = category.nombre
        self.repo.delete(category)
        self.audit.create("delete", "categories", f"Categoría: {nombre}", actor_id)


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)
        self.audit = AuditLogRepository(db)

    def list_products(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        only_active: bool = False,
    ) -> List[Product]:
        return self.repo.get_all(skip, limit, search, category_id, only_active)

    def get_product(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return product

    def create_product(self, data: ProductCreate, actor_id: Optional[int] = None) -> Product:
        self._validate_category(data.category_id)
        product = Product(
            nombre=sanitize_string(data.nombre),
            descripcion=data.descripcion,
            precio=data.precio,
            stock=data.stock,
            stock_minimo=data.stock_minimo,
            category_id=data.category_id,
            estado=data.estado,
        )
        created = self.repo.create(product)
        self.audit.create("create", "products", f"Producto: {created.nombre}", actor_id)
        return created

    def update_product(self, product_id: int, data: ProductUpdate, actor_id: Optional[int] = None) -> Product:
        product = self.get_product(product_id)
        if data.category_id is not None:
            self._validate_category(data.category_id)
            product.category_id = data.category_id
        if data.nombre is not None:
            product.nombre = sanitize_string(data.nombre)
        if data.descripcion is not None:
            product.descripcion = data.descripcion
        if data.precio is not None:
            product.precio = data.precio
        if data.stock is not None:
            product.stock = data.stock
        if data.stock_minimo is not None:
            product.stock_minimo = data.stock_minimo
        if data.estado is not None:
            product.estado = data.estado

        updated = self.repo.update(product)
        self.audit.create("update", "products", f"Producto: {updated.nombre}", actor_id)
        return updated

    def delete_product(self, product_id: int, actor_id: Optional[int] = None) -> None:
        product = self.get_product(product_id)
        nombre = product.nombre
        delete_product_image(product.imagen)
        self.repo.delete(product)
        self.audit.create("delete", "products", f"Producto: {nombre}", actor_id)

    def activate_product(self, product_id: int, actor_id: Optional[int] = None) -> Product:
        product = self.get_product(product_id)
        product.estado = True
        updated = self.repo.update(product)
        self.audit.create("activate", "products", f"Producto activado: {updated.nombre}", actor_id)
        return updated

    def deactivate_product(self, product_id: int, actor_id: Optional[int] = None) -> Product:
        product = self.get_product(product_id)
        product.estado = False
        updated = self.repo.update(product)
        self.audit.create("deactivate", "products", f"Producto desactivado: {updated.nombre}", actor_id)
        return updated

    def upload_image(self, product_id: int, file: UploadFile, actor_id: Optional[int] = None) -> Product:
        product = self.get_product(product_id)
        delete_product_image(product.imagen)
        product.imagen = save_product_image(file)
        updated = self.repo.update(product)
        self.audit.create("upload_image", "products", f"Imagen: {updated.nombre}", actor_id)
        return updated

    def get_low_stock(self) -> List[Product]:
        return self.repo.get_low_stock()

    def _validate_category(self, category_id: Optional[int]) -> None:
        if category_id is None:
            return
        if not self.category_repo.get_by_id(category_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = InventoryRepository(db)
        self.product_repo = ProductRepository(db)
        self.audit = AuditLogRepository(db)

    def list_movements(
        self,
        skip: int = 0,
        limit: int = 100,
        product_id: Optional[int] = None,
        tipo: Optional[str] = None,
    ) -> List[InventoryMovement]:
        return self.repo.get_all(skip, limit, product_id, tipo)

    def get_movement(self, movement_id: int) -> InventoryMovement:
        movement = self.repo.get_by_id(movement_id)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movimiento no encontrado")
        return movement

    def create_movement(self, data: InventoryMovementCreate, actor_id: Optional[int] = None) -> InventoryMovement:
        product = self.product_repo.get_by_id(data.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        stock_anterior = product.stock
        if data.tipo == MovementType.ENTRADA.value:
            stock_nuevo = stock_anterior + data.cantidad
        elif data.tipo == MovementType.SALIDA.value:
            if stock_anterior < data.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente. Disponible: {stock_anterior}",
                )
            stock_nuevo = stock_anterior - data.cantidad
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de movimiento inválido")

        product.stock = stock_nuevo
        self.product_repo.update(product)

        movement = InventoryMovement(
            product_id=data.product_id,
            user_id=actor_id,
            tipo=data.tipo,
            cantidad=data.cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=data.motivo,
        )
        created = self.repo.create(movement)
        self.audit.create(
            "create",
            "inventory",
            f"{data.tipo} x{data.cantidad} - Producto #{data.product_id}",
            actor_id,
        )
        return created

    def delete_movement(self, movement_id: int, actor_id: Optional[int] = None) -> None:
        movement = self.get_movement(movement_id)
        product = self.product_repo.get_by_id(movement.product_id)
        if product:
            if movement.tipo == MovementType.ENTRADA.value:
                product.stock = max(0, product.stock - movement.cantidad)
            else:
                product.stock += movement.cantidad
            self.product_repo.update(product)

        self.repo.delete(movement)
        self.audit.create("delete", "inventory", f"Movimiento #{movement_id} revertido", actor_id)
