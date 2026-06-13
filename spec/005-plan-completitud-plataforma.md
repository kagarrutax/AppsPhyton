## Objetivo

Completar la plataforma FastFood cerrando brechas de tests, UX admin, DevOps y funcionalidades pendientes identificadas tras auditoría.

## Alcance

- **Incluye**:
  - Ampliar tests backend (admin) y frontend (utilidades)
  - Corregir fallas detectadas por tests
  - Roadmap priorizado de lo que falta
- **No incluye**:
  - Apps móvil/escritorio nativas
  - CI/CD completo (solo preparación)

## Estado actual (auditoría)

| Área | Estado | Tests |
|------|--------|-------|
| Auth + RBAC | Completo | 9+ |
| Catálogo + inventario | Completo | 7 |
| Comercio (carrito/pedidos) | Completo | 6 |
| Billing (pagos/facturas) | Completo | 4 |
| Dashboard admin API | Completo | 2 |
| Panel admin React | Implementado | Sin tests E2E |
| Tema claro/oscuro | Implementado | 4 (theme) |
| format.ts (fechas/money) | Corregido | 4 |

## Pasos de implementación (roadmap)

### Fase 1 — Tests y estabilidad (prioridad alta)
- [x] Tests admin: categorías CRUD, usuarios, pedidos globales, schema dashboard
- [x] Tests frontend: `formatMoney`, `formatDate`
- [x] Tests componentes admin (Vitest + RTL): `AdminRoute`, `StatusBadge`
- [x] Script raíz `npm run dev` (backend + frontend concurrente)
- [x] Documentar reinicio backend tras nuevas rutas

### Fase 2 — Panel admin (prioridad media)
- [x] Página inventario (movimientos + stock bajo)
- [x] Descarga facturas/tickets PDF desde admin
- [x] Filtro por usuario en pedidos y pagos
- [x] CRUD roles/permisos (solo lectura mínima)
- [x] Agregar al carrito desde modal de producto (cliente)

### Fase 3 — API pendiente (prioridad media)
- [x] `GET /api/v1/audit-logs` (lectura auditoría)
- [x] Endpoint health extendido (DB, migración head)
- [x] Página admin `/admin/auditoria`

### Fase 4 — DevOps y calidad (prioridad baja)
- [x] GitHub Actions: pytest + frontend build + vitest
- [x] E2E Playwright: smoke (tienda, login admin, registro + carrito)
- [x] Suprimir warnings pytest (httpx testclient, asyncio 3.16, alembic)

## Riesgos y supuestos

- **Riesgo**: Backend en producción local sin reiniciar → 404 en rutas nuevas.
  - **Mitigación**: script `start.ps1` y nota en README.
- **Riesgo**: Tests frontend limitados sin RTL/E2E.
  - **Mitigación**: ampliar Vitest por módulo crítico.
- **Supuesto**: MySQL XAMPP activo para entorno local.

## Testing (obligatorio)

### Comandos
```powershell
cd backend; .\venv\Scripts\pytest -v
cd frontend; npm test -- --run
cd frontend; npm run build
```

### Meta de cobertura
- Backend: ≥ 35 tests (auth, catalog, commerce, billing, admin, dashboard, security)
- Frontend: utilidades + al menos 1 test por módulo admin crítico

## Seguridad (checklist pendiente)

- [ ] Rate limit en login (verificar en prod)
- [ ] Audit logs expuestos solo a admin
- [ ] Validar tamaño/tipo uploads en tests de integración

## Criterios de aceptación

- [x] Nuevos tests admin backend pasan
- [x] Tests format.ts pasan
- [ ] Plan documentado y priorizado
- [x] Fase 1 completada al 100%
