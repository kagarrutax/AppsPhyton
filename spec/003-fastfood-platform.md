## Objetivo

Plataforma completa de gestión y venta de comida rápida con arquitectura Cliente-Servidor: API REST (FastAPI + MySQL) y frontend web (React + TypeScript), preparada para clientes web, móvil y escritorio vía APIs reutilizables.

## Alcance

- **Incluye**:
  - Backend `backend/`: FastAPI, SQLAlchemy, Alembic, JWT, RBAC, MySQL (XAMPP)
  - Frontend `frontend/`: React, TypeScript, Tailwind, Axios, React Router, Context API
  - Módulos: Usuarios, Roles, Permisos, Productos, Inventario, Carrito, Pedidos, Compras, Pagos, Facturación, Tickets
  - Migraciones Alembic como única fuente de esquema
  - Seeders (admin, roles, permisos, productos demo)
  - Tests backend (30+)
  - Seguridad OWASP básica
- **No incluye** (fase pendiente):
  - Apps Android / Escritorio nativas
  - CI/CD automatizado

## Contexto / Norte del proyecto

- **Problema a resolver**: Venta y gestión de comida rápida con control de inventario, pagos por transferencia y facturación.
- **Usuarios / actores**: Administrador (total), Cliente (compras limitadas).
- **Restricciones**: XAMPP MySQL local, Python 3.11+, Node.js 18+.

## Diseño (alto nivel)

- **Componentes**:
  - `backend/app/`: models → repositories → services → routes
  - `frontend/src/`: api → context → pages → components
- **Flujo principal**: Registro → Catálogo → Carrito → Checkout → Pago (comprobante) → Admin aprueba → Factura/Ticket PDF
- **Datos**: MySQL `fastfood_db`, JWT Bearer, uploads en `backend/uploads/`

## Pasos de implementación (por etapas)

- **Etapa A — Inspección**: Estructura repo, MySQL activo, `.env` configurado
- **Etapa B — Backend auth + RBAC**: Usuarios, roles, permisos, JWT
- **Etapa C — Catálogo e inventario**: Productos, categorías, movimientos
- **Etapa D — Comercio**: Carrito, pedidos, compras
- **Etapa E — Billing**: Pagos transferencia, facturas, tickets PDF
- **Etapa F — Frontend**: Home estilo Rappi, auth, carrito, pedidos
- **Etapa G — Migraciones**: Alembic head + scripts `migrate.ps1`
- **Etapa H — Cierre**: pytest, build frontend, smoke test

## Testing (obligatorio)

### Pruebas unitarias / integración

- **Qué se prueba**: Auth, RBAC, catálogo, comercio, billing, seguridad
- **Comando**: `cd backend && pytest -v`

### Pruebas funcionales

- **Flujos**: Health, productos públicos, login, carrito, checkout, pago
- **Comandos**:
  - Backend: `uvicorn main:app --port 8000`
  - Frontend: `npm run dev`
  - Migración: `.\scripts\migrate.ps1`

## Seguridad (obligatorio)

### Checklist

- [x] Validación Pydantic + sanitización XSS
- [x] JWT + bcrypt, RBAC granular
- [x] Rate limiting, CORS, headers HTTP
- [x] Uploads validados (tipo/tamaño)
- [x] `.env` fuera de git
- [x] SQL Injection mitigado vía ORM

## Criterios de aceptación

- [x] Estructura `backend/` y `frontend/` operativa
- [x] Alembic en `004_billing (head)`
- [x] 37 tests backend pasan
- [x] Frontend build exitoso
- [x] Admin: `admin@admin.com` / `Admin123*`
- [x] Dashboard administrador con KPIs
