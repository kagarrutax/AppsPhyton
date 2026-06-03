# AppsPhyton

Proyecto con enfoque **spec-as-source**: planificación y ejecución controlada por IA.

## Estructura

| Carpeta | Contenido |
|---------|-----------|
| `spec/` | Planes detallados por solicitud |
| `skill/` | Skills de ejecución para el agente |
| `app/` | Aplicaciones finales (código ejecutable) |

## Aplicaciones

| App | Ruta | Stack |
|-----|------|-------|
| Calculadora | `app/calculadora/` | HTML, CSS, JS |
| Tienda catálogo | `app/tienda/` | PHP MVC, Tailwind 3, SQLite |

## Inicio rápido (tienda)

```powershell
cd app/tienda
php database/init.php
php -S localhost:8080 -t public public/index.php
```

Abre http://localhost:8080 — Admin: `admin@tienda.com` / `admin123`

## Inicio rápido (calculadora)

```powershell
cd app/calculadora
python -m http.server 8765
```

Abre http://localhost:8765 en el navegador.
