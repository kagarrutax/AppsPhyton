## app/
Esta carpeta contiene la **aplicación final** (código ejecutable) del proyecto.

La orquestación basada en IA vive en:
- `spec/` (planes y especificaciones)
- `skill/` (skills de ejecución del agente)

Regla clave: `spec/` y `skill/` **no deben acoplarse** a la tecnología/framework dentro de `app/`.

## Aplicaciones

### calculadora/
Calculadora web (HTML, CSS, JS).

**Abrir en navegador:**
```powershell
cd app/calculadora
python -m http.server 8765
```
Luego visita: http://localhost:8765

### tienda/
Tienda catálogo PHP MVC + Tailwind CSS 3 (WhatsApp).

```powershell
cd app/tienda
php database/init.php
php -S localhost:8080 -t public public/index.php
```

Admin: `admin@tienda.com` / `admin123`

**Tests:** `php app/tienda/tests/smoke.php`

