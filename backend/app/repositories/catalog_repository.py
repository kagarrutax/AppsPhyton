from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.catalog import Category, InventoryMovement, Product


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.nombre == name).first()

    def get_all(self, skip: int = 0, limit: int = 100, only_active: bool = False) -> List[Category]:
        query = self.db.query(Category)
        if only_active:
            query = query.filter(Category.estado.is_(True))
        return query.offset(skip).limit(limit).all()

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.nombre == name).first()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        only_active: bool = False,
    ) -> List[Product]:
        query = self.db.query(Product)
        if only_active:
            query = query.filter(Product.estado.is_(True))
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if search:
            term = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Product.nombre).like(term),
                    func.lower(Product.descripcion).like(term),
                )
            )
        return query.order_by(Product.nombre).offset(skip).limit(limit).all()

    def get_low_stock(self) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(Product.estado.is_(True))
            .filter(Product.stock <= Product.stock_minimo)
            .order_by(Product.stock)
            .all()
        )

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movement_id: int) -> Optional[InventoryMovement]:
        return self.db.query(InventoryMovement).filter(InventoryMovement.id == movement_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        product_id: Optional[int] = None,
        tipo: Optional[str] = None,
    ) -> List[InventoryMovement]:
        query = self.db.query(InventoryMovement)
        if product_id:
            query = query.filter(InventoryMovement.product_id == product_id)
        if tipo:
            query = query.filter(InventoryMovement.tipo == tipo)
        return query.order_by(InventoryMovement.fecha.desc()).offset(skip).limit(limit).all()

    def create(self, movement: InventoryMovement) -> InventoryMovement:
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)
        return movement

    def delete(self, movement: InventoryMovement) -> None:
        self.db.delete(movement)
        self.db.commit()
