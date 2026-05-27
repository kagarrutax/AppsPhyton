## Propósito de la skill
Implementar la calculadora según `spec/001-calculadora-html-css-js.md` con gates de testing y seguridad.

## Reglas de operación (no negociables)
- Spec como fuente de verdad.
- Sin `eval` ni `Function`.
- Lógica en `calculator.js`, UI en `main.js`.
- No avanzar si fallan los tests.

## Tareas
### Etapa A — Inspección
- Confirmar rutas `app/calculadora/`.
**Done cuando**: estructura definida.

### Etapa B — Implementación
- Crear HTML, CSS, JS.
**Done cuando**: UI responde a clics.

### Etapa C — Unit tests
- `tests/calculator.test.mjs` + `node --test`.
**Done cuando**: todos pasan.

### Etapa D — Funcionales
- Probar flujos en navegador.
**Done cuando**: checklist del spec cumplido.

### Etapa E — Seguridad
- Revisar checklist del spec.
**Done cuando**: sin hallazgos abiertos.

### Etapa F — Cierre
- Actualizar `app/README.md`.
**Done cuando**: usuario puede abrir la app.

## Comandos de verificación
- Unit: `node --test app/calculadora/tests/calculator.test.mjs`
- Funcional: abrir `index.html` o `python -m http.server 8765` en `app/calculadora/`
