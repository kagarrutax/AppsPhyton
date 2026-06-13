from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.catalog import Category, Product
from app.repositories.catalog_repository import CategoryRepository, ProductRepository

DEMO_CATEGORIES = [
    {"nombre": "Hamburguesas", "descripcion": "Hamburguesas artesanales a la parrilla"},
    {"nombre": "Bebidas", "descripcion": "Refrescos, jugos, malteadas y café"},
    {"nombre": "Combos", "descripcion": "Promociones para compartir"},
    {"nombre": "Acompañamientos", "descripcion": "Papas, nuggets, aros de cebolla"},
    {"nombre": "Alitas", "descripcion": "Alitas BBQ, picantes y crujientes"},
    {"nombre": "Postres", "descripcion": "Postres, helados y brownies"},
    {"nombre": "Ensaladas", "descripcion": "Opciones frescas y saludables"},
    {"nombre": "Desayunos", "descripcion": "Para empezar el día con energía"},
]

DEMO_PRODUCTS = [
    # Hamburguesas
    {"nombre": "Hamburguesa Clásica", "descripcion": "Carne 150g, lechuga, tomate, queso cheddar", "precio": Decimal("8.99"), "stock": 50, "stock_minimo": 10, "categoria": "Hamburguesas"},
    {"nombre": "Hamburguesa BBQ", "descripcion": "Carne 150g, salsa BBQ, cebolla caramelizada", "precio": Decimal("10.50"), "stock": 35, "stock_minimo": 10, "categoria": "Hamburguesas"},
    {"nombre": "Hamburguesa Doble Cheese", "descripcion": "Doble carne, doble queso, salsa especial", "precio": Decimal("12.99"), "stock": 30, "stock_minimo": 8, "categoria": "Hamburguesas"},
    {"nombre": "Hamburguesa Pollo Crispy", "descripcion": "Pechuga empanizada, coleslaw, pepinillos", "precio": Decimal("9.99"), "stock": 40, "stock_minimo": 10, "categoria": "Hamburguesas"},
    {"nombre": "Hamburguesa Veggie", "descripcion": "Medallón de garbanzo, aguacate, tomate", "precio": Decimal("9.50"), "stock": 25, "stock_minimo": 8, "categoria": "Hamburguesas"},
    # Bebidas
    {"nombre": "Malteada de Vainilla", "descripcion": "Malteada cremosa 16oz", "precio": Decimal("4.99"), "stock": 40, "stock_minimo": 10, "categoria": "Bebidas"},
    {"nombre": "Malteada de Chocolate", "descripcion": "Con trozos de brownie", "precio": Decimal("5.49"), "stock": 35, "stock_minimo": 10, "categoria": "Bebidas"},
    {"nombre": "Limonada Natural", "descripcion": "Limonada fresca 500ml", "precio": Decimal("3.25"), "stock": 60, "stock_minimo": 15, "categoria": "Bebidas"},
    {"nombre": "Gaseosa 400ml", "descripcion": "Coca-Cola, Sprite o Fanta", "precio": Decimal("2.50"), "stock": 100, "stock_minimo": 25, "categoria": "Bebidas"},
    {"nombre": "Café Americano", "descripcion": "Café recién preparado 12oz", "precio": Decimal("2.99"), "stock": 45, "stock_minimo": 10, "categoria": "Bebidas"},
    # Combos
    {"nombre": "Combo Familiar", "descripcion": "4 hamburguesas clásicas + papas grandes + 4 bebidas", "precio": Decimal("29.99"), "stock": 15, "stock_minimo": 5, "categoria": "Combos"},
    {"nombre": "Combo Pareja", "descripcion": "2 hamburguesas BBQ + papas medianas + 2 bebidas", "precio": Decimal("18.99"), "stock": 20, "stock_minimo": 5, "categoria": "Combos"},
    {"nombre": "Combo Ejecutivo", "descripcion": "Hamburguesa clásica + papas + bebida + postre", "precio": Decimal("13.99"), "stock": 25, "stock_minimo": 8, "categoria": "Combos"},
    {"nombre": "Combo Alitas", "descripcion": "12 alitas + papas + 2 salsas + 2 bebidas", "precio": Decimal("22.99"), "stock": 18, "stock_minimo": 5, "categoria": "Combos"},
    # Acompañamientos
    {"nombre": "Papas Fritas", "descripcion": "Porción grande de papas crujientes", "precio": Decimal("3.50"), "stock": 80, "stock_minimo": 20, "categoria": "Acompañamientos"},
    {"nombre": "Papas con Queso", "descripcion": "Papas fritas con salsa de queso cheddar", "precio": Decimal("4.99"), "stock": 50, "stock_minimo": 15, "categoria": "Acompañamientos"},
    {"nombre": "Nuggets de Pollo", "descripcion": "8 piezas con salsa a elección", "precio": Decimal("5.99"), "stock": 45, "stock_minimo": 12, "categoria": "Acompañamientos"},
    {"nombre": "Aros de Cebolla", "descripcion": "6 aros empanizados crujientes", "precio": Decimal("4.50"), "stock": 40, "stock_minimo": 10, "categoria": "Acompañamientos"},
    # Alitas
    {"nombre": "Alitas BBQ x6", "descripcion": "6 alitas con salsa BBQ ahumada", "precio": Decimal("7.99"), "stock": 35, "stock_minimo": 10, "categoria": "Alitas"},
    {"nombre": "Alitas Picantes x6", "descripcion": "6 alitas con salsa buffalo", "precio": Decimal("7.99"), "stock": 32, "stock_minimo": 10, "categoria": "Alitas"},
    {"nombre": "Alitas Mix x12", "descripcion": "12 alitas mitad BBQ mitad picante", "precio": Decimal("14.99"), "stock": 20, "stock_minimo": 6, "categoria": "Alitas"},
    # Postres
    {"nombre": "Brownie con Helado", "descripcion": "Brownie tibio con bola de vainilla", "precio": Decimal("5.99"), "stock": 30, "stock_minimo": 8, "categoria": "Postres"},
    {"nombre": "Cheesecake", "descripcion": "Porción de cheesecake de frutos rojos", "precio": Decimal("4.99"), "stock": 25, "stock_minimo": 8, "categoria": "Postres"},
    {"nombre": "Sundae de Caramelo", "descripcion": "Helado con salsa de caramelo y nueces", "precio": Decimal("4.50"), "stock": 28, "stock_minimo": 8, "categoria": "Postres"},
    # Ensaladas
    {"nombre": "Ensalada César", "descripcion": "Lechuga, pollo grillado, crutones, parmesano", "precio": Decimal("8.50"), "stock": 22, "stock_minimo": 6, "categoria": "Ensaladas"},
    {"nombre": "Ensalada Mixta", "descripcion": "Mix de verdes, tomate, aguacate, vinagreta", "precio": Decimal("7.99"), "stock": 20, "stock_minimo": 6, "categoria": "Ensaladas"},
    # Desayunos
    {"nombre": "Desayuno Americano", "descripcion": "Huevos, tostadas, jamón y café", "precio": Decimal("6.99"), "stock": 30, "stock_minimo": 8, "categoria": "Desayunos"},
    {"nombre": "Sandwich de Huevo", "descripcion": "Huevo, queso y tocino en pan artesanal", "precio": Decimal("5.50"), "stock": 35, "stock_minimo": 10, "categoria": "Desayunos"},
    {"nombre": "Hot Cakes x3", "descripcion": "Con mantequilla y miel de maple", "precio": Decimal("5.99"), "stock": 28, "stock_minimo": 8, "categoria": "Desayunos"},
]


def seed_catalog(db: Session) -> None:
    category_repo = CategoryRepository(db)
    product_repo = ProductRepository(db)

    category_map: dict[str, Category] = {}
    for cat_data in DEMO_CATEGORIES:
        existing = category_repo.get_by_name(cat_data["nombre"])
        if existing:
            category_map[cat_data["nombre"]] = existing
        else:
            category = Category(**cat_data, estado=True)
            created = category_repo.create(category)
            category_map[cat_data["nombre"]] = created

    for prod_data in DEMO_PRODUCTS:
        prod_copy = prod_data.copy()
        if product_repo.get_by_name(prod_copy["nombre"]):
            continue

        categoria_nombre = prod_copy.pop("categoria")
        category = category_map.get(categoria_nombre)
        product = Product(
            **prod_copy,
            category_id=category.id if category else None,
            estado=True,
        )
        product_repo.create(product)
