## Propósito de la skill

Configurar CI/CD y tests E2E para FastFood Platform (Fase 4).

## Tareas completadas

### GitHub Actions (`.github/workflows/ci.yml`)
- Job `backend`: pytest con APP_ENV=test
- Job `frontend`: vitest + build
- Job `e2e`: MySQL 8 + migraciones + uvicorn + vite preview + Playwright

### Playwright (`e2e/`)
- Smoke: home, login, admin dashboard, registro cliente + carrito
- Comando local: `npm run e2e` (con backend y frontend activos)

### Warnings pytest
- Filtros en `backend/pytest.ini` para httpx, asyncio 3.16, alembic

## Comandos

```powershell
npm run test
npm run e2e:install
npm run e2e
```

## Pendiente opcional

- E2E flujo completo: checkout + upload comprobante + admin aprueba
- Migrar a httpx2 cuando Starlette lo requiera de forma estable
