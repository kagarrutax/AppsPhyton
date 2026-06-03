## Objetivo
Entregar una tienda web en `app/tienda/` con arquitectura monolítica MVC (PHP + Tailwind CSS 3): catálogo visual, gestión de productos, login/registro, dashboard admin y compra vía enlace a WhatsApp del vendedor.

## Alcance
- **Incluye**:
  - Front controller PHP con rutas MVC.
  - Página principal dinámica con catálogo de productos.
  - Login y registro de usuarios (sesiones PHP).
  - Dashboard administrativo (solo rol admin).
  - CRUD básico de productos (crear, listar, editar, eliminar).
  - Botón comprar → redirección WhatsApp con mensaje prellenado.
  - Tailwind CSS 3 + paleta `palette.css` del usuario.
  - Diseño responsive.
  - SQLite como base de datos (sin dependencias externas).
- **No incluye**:
  - Pasarela de pago, carrito persistente ni API REST separada.
  - Subida a producción ni Docker.

## Contexto / Norte del proyecto
- **Problema**: catálogo con contacto directo al vendedor por WhatsApp.
- **Actores**: visitante, usuario registrado, administrador.
- **Restricciones**: solo PHP; Tailwind 3; MVC monolítico; desacoplado de `spec/`/`skill/`.

## Diseño (alto nivel)
```
app/tienda/
  public/index.php          → Front controller
  config/                   → app.php, database.php
  database/schema.sql       → SQLite schema + seed
  src/Core/                 → Router, Database, Controller, Auth
  src/Controllers/          → Home, Auth, Dashboard, Product
  src/Models/               → User, Product
  src/Views/                → layouts, home, auth, dashboard, products
  tests/                    → smoke tests PHP
```

- **Flujo compra**: catálogo → botón "Comprar" → `https://wa.me/{telefono}?text=...`
- **Flujo admin**: login admin → dashboard → gestionar productos.

## Pasos de implementación
1. Spec + skill.
2. Core (Router, DB, Auth) + config.
3. Schema SQLite + seed admin y productos demo.
4. Controladores y modelos.
5. Vistas Tailwind con paleta.
6. Tests smoke + checklist seguridad.

## Testing
### Unitarias / smoke
- `php tests/smoke.php` — conexión DB, rutas clave, helpers WhatsApp.

### Funcionales (manual)
1. `/` muestra catálogo.
2. Registro + login funcionan.
3. Admin accede dashboard y CRUD productos.
4. Botón comprar abre WhatsApp con mensaje del producto.

## Seguridad
- [x] `password_hash` / `password_verify`
- [x] Prepared statements (PDO)
- [x] CSRF en formularios POST
- [x] Escape HTML en vistas (`htmlspecialchars`)
- [x] Validación de entradas y roles (admin)
- [x] Sin secretos hardcodeados críticos (WhatsApp en config)

## Riesgos y supuestos
- **Riesgo**: imágenes sin validar → mitigar MIME/size en upload.
- **Supuesto**: PHP 8.1+ y extensión PDO SQLite disponibles.
- **Supuesto**: número WhatsApp configurable en `config/app.php`.

## Criterios de aceptación
- [x] Catálogo visual en página principal.
- [x] Login y registro operativos.
- [x] Dashboard admin con CRUD productos.
- [x] Compra redirige a WhatsApp del vendedor.
- [x] Tailwind 3 + paleta del usuario aplicada.
- [x] Responsive en móvil.
- [x] Estructura MVC clara.
