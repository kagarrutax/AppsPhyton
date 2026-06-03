## Propósito
Implementar tienda según `spec/002-tienda-php-mvc-tailwind.md` por etapas con gates.

## Reglas
- MVC monolítico PHP; Tailwind 3 CDN con colores de palette.css.
- No avanzar si falla `php tests/smoke.php`.
- WhatsApp solo vía enlace externo (wa.me), sin SDK.

## Tareas
### A — Core + config
- Router, Database, Controller base, Auth, config.
**Done**: front controller enruta rutas.

### B — DB + modelos
- schema.sql, User, Product.
**Done**: seed admin y productos demo.

### C — Controladores
- Home, Auth, Dashboard, Product.
**Done**: CRUD y sesiones.

### D — Vistas Tailwind
- Layouts, catálogo, auth, admin, formularios producto.
**Done**: responsive + paleta.

### E — Seguridad + tests
- CSRF, escape, validación uploads.
**Done**: smoke tests pasan.

### F — Cierre
- README con instrucciones `php -S`.
**Done**: criterios spec cumplidos.

## Comandos
```powershell
cd app/tienda
php database/init.php
php -S localhost:8080 -t public
php tests/smoke.php
```
