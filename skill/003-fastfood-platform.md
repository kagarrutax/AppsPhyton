## Propósito de la skill

Ejecutar y mantener la plataforma FastFood (`backend/` + `frontend/`) siguiendo spec `003-fastfood-platform.md`, con gates de migración, testing y seguridad.

## Reglas de operación (no negociables)

- Migraciones **solo** vía Alembic (`alembic upgrade head` o `scripts/migrate.ps1`).
- No usar `Base.metadata.create_all` en producción.
- No commitear `.env`, `venv/`, `node_modules/`, `uploads/*` (excepto `.gitkeep`).
- Ejecutar `pytest` antes de cerrar cambios en backend.
- Ejecutar `npm run build` antes de cerrar cambios en frontend.

## Tareas (pequeñas, controladas, verificables)

### Etapa A — Inspección

- Verificar MySQL XAMPP activo y BD `fastfood_db`
- Verificar `.env` en `backend/` y `frontend/`
- `alembic current` debe mostrar `004_billing (head)`

**Done cuando**: entorno y revisión Alembic confirmados.

### Etapa B — Migración de BD

```powershell
cd backend
.\scripts\migrate.ps1          # setup completo
# o
.\scripts\migrate.ps1 -Upgrade
.\scripts\migrate.ps1 -Seed
```

**Done cuando**: `004_billing (head)` y seeders aplicados.

### Etapa C — Unit tests (gate)

```powershell
cd backend
.\venv\Scripts\pytest -v
```

**Done cuando**: 30/30 tests pasan.

### Etapa D — Funcionales (gate)

```powershell
# Terminal 1
cd backend && .\venv\Scripts\uvicorn main:app --reload --port 8000

# Terminal 2
cd frontend && npm run dev
```

Verificar:
- http://localhost:8000/api/v1/health → `{"status":"ok"}`
- http://localhost:8000/api/v1/products/public → productos
- http://localhost:5173 → home carga

**Done cuando**: API y frontend responden.

### Etapa E — Seguridad (gate)

- Endpoints protegidos retornan 401 sin token
- Uploads rechazan formatos no permitidos
- Admin requerido para aprobar pagos

**Done cuando**: checklist spec marcado.

### Etapa F — Cierre

```powershell
cd frontend && npm run build
```

**Done cuando**: build sin errores TypeScript.

## Comandos de verificación

| Acción | Comando |
|--------|---------|
| Migrar | `npm run backend:migrate` |
| Tests | `npm run backend:test` |
| API | `npm run backend:dev` |
| UI | `npm run frontend:dev` |
| Build | `npm run frontend:build` |
