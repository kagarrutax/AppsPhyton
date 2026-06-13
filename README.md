# AppsPhyton

Proyecto con enfoque **spec-as-source**: planificación y ejecución controlada por IA.

## Estructura

| Carpeta | Contenido |
|---------|-----------|
| `spec/` | Planes detallados por solicitud |
| `skill/` | Skills de ejecución para el agente |
| `app/` | Aplicaciones legacy (calculadora, tienda PHP) |
| `backend/` | **FastFood Platform** — API FastAPI + MySQL |
| `frontend/` | **FastFood Platform** — React + TypeScript + Tailwind |
| `spec/003-fastfood-platform.md` | Spec FastFood (spec-as-source) |
| `skill/003-fastfood-platform.md` | Skill de ejecución FastFood |

## FastFood Platform (inicio rápido)

**Requisitos:** XAMPP MySQL activo, Python 3.11+, Node.js 18+

```powershell
# 1. Crear base de datos (solo la primera vez)
C:\xampp\mysql\bin\mysql.exe -u root -e "CREATE DATABASE IF NOT EXISTS fastfood_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Migraciones (solo la primera vez o tras cambios de esquema)
cd backend
.\scripts\migrate.ps1

# 3. Levantar backend + frontend (desde la raíz)
cd ..
npm install          # instala concurrently (solo la primera vez)
npm run dev
```

También puedes usar dos terminales:

```powershell
# Terminal 1 — Backend
cd backend
.\scripts\start.ps1

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

> **Importante:** Si agregas rutas nuevas al backend, reinicia la API (`Ctrl+C` y vuelve a ejecutar `npm run dev` o `.\scripts\start.ps1`). Si no, el frontend puede recibir errores 404.

### Tests

```powershell
npm run test              # backend (41) + frontend (15)
npm run backend:test
npm run frontend:test
npm run e2e:install       # Playwright (solo la primera vez)
> **E2E:** primero `npm run dev` (en otra terminal), luego `npm run e2e`.
```

### CI (GitHub Actions)

El workflow `.github/workflows/ci.yml` ejecuta en cada push/PR:

- **backend** — pytest (41 tests, SQLite en memoria)
- **frontend** — vitest + build
- **e2e** — Playwright con MySQL 8 (smoke: tienda, login admin, registro cliente)

- Frontend: http://localhost:5173
- API / Swagger: http://localhost:8000/docs
- Panel admin: http://localhost:5173/admin
- Admin: `admin@admin.com` / `Admin123*`

### Docker (opcional)

```powershell
docker compose up --build
```

- API: http://localhost:8000
- Web: http://localhost:5173

## Aplicaciones legacy

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
