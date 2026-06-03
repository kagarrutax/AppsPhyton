# Tienda Catálogo — PHP MVC + Tailwind CSS 3

Aplicación monolítica MVC con catálogo visual, gestión de productos, autenticación y compra vía WhatsApp.

## Requisitos

- PHP 8.1+
- Extensiones: `pdo_sqlite`, `fileinfo`

## Instalación

```powershell
cd app/tienda
php database/init.php
php -S localhost:8080 -t public public/index.php
```

Abre: **http://localhost:8080**

## Credenciales demo

| Rol  | Email              | Contraseña |
|------|--------------------|------------|
| Admin | admin@tienda.com  | admin123   |

## Configurar WhatsApp

Edita `config/app.php`:

```php
'whatsapp' => [
    'country_code' => '51',      // Perú
    'phone' => '999888777',      // Tu número sin +
    'seller_name' => 'Vendedor',
],
```

## Estructura MVC

```
app/tienda/
├── config/           # Configuración app y DB
├── database/         # Schema SQLite + init
├── public/           # Front controller (index.php)
├── src/
│   ├── Core/         # Router, Database, Auth, Controller
│   ├── Controllers/  # Home, Auth, Dashboard, Product
│   ├── Models/       # User, Product
│   └── Views/        # Vistas Tailwind
└── tests/            # Smoke tests
```

## Rutas principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Catálogo público |
| GET/POST | `/login` | Iniciar sesión |
| GET/POST | `/register` | Registro |
| GET | `/dashboard` | Panel admin |
| GET | `/admin/products` | Listar productos |
| GET/POST | `/admin/products/create` | Crear producto |

## Tests

```powershell
php tests/smoke.php
```

## Paleta de colores

Definida en `public/css/palette.css` (proyecto del usuario).

## Spec / Skill

- `spec/002-tienda-php-mvc-tailwind.md`
- `skill/002-tienda-php-mvc-tailwind.md`
