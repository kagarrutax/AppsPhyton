## Objetivo
Entregar una calculadora web funcional en `app/calculadora/` usando HTML, CSS y JavaScript, ejecutable en el navegador sin dependencias externas.

## Alcance
- **Incluye**:
  - Operaciones básicas: suma, resta, multiplicación, división.
  - Entrada por botones: dígitos, punto decimal, igual, limpiar (C), borrar último dígito (⌫).
  - Pantalla con valor actual y expresión secundaria.
  - Lógica en módulo JS separado y testeable (sin `eval`).
  - Pruebas unitarias con Node (`node --test`).
  - Estilos responsivos y foco visible.
- **No incluye**:
  - Historial persistente, modo científico ni backend.

## Contexto / Norte del proyecto
- **Problema a resolver**: aplicación de referencia en `app/` bajo spec-as-source.
- **Usuarios / actores**: usuario en navegador.
- **Restricciones**: HTML/CSS/JS estático; sin acoplar `app/` a `spec/`/`skill/`.

## Diseño (alto nivel)
- **Componentes**: `index.html`, `css/styles.css`, `js/calculator.js`, `js/main.js`, `tests/calculator.test.mjs`.
- **Flujo principal**: dígitos → operador → dígitos → `=` → resultado.
- **Decisiones**: no usar `eval`; lógica pura exportada para tests.

## Pasos de implementación (por etapas)
- **Etapa A**: inspección del repo.
- **Etapa B**: HTML + CSS + JS mínimo.
- **Etapa C**: pruebas unitarias.
- **Etapa D**: verificación manual en navegador.
- **Etapa E**: checklist de seguridad.
- **Etapa F**: cierre y documentación.

## Testing (obligatorio)
### Pruebas unitarias
- **Qué se prueba**: `compute`, división por cero, `formatDisplay`, `appendDigit`, `backspace`.
- **Comando**: `node --test app/calculadora/tests/calculator.test.mjs`

### Pruebas funcionales
- `2 + 3 =` → `5`; `10 / 2 =` → `5`; `1 / 0 =` → Error; `C` reinicia; `⌫` borra dígito.
- Abrir `app/calculadora/index.html` o `http://localhost:8765` con servidor local.

## Seguridad (obligatorio)
### Checklist
- [x] Sin `eval` / `Function`
- [x] Errores controlados (división por cero)
- [x] Sin secretos en repo
- [x] Límite de longitud en pantalla

### Amenazas y mitigaciones
- **Inyección vía eval** → operaciones explícitas en `compute()`.
- **División por cero** → retorno `null` y mensaje "Error".
- **Overflow visual** → `MAX_DISPLAY_LENGTH`.

## Riesgos y supuestos
- **Riesgos**: imprecisión de flotantes; mitigado con redondeo en display.
- **Supuestos**: Node disponible solo para tests locales.

## Criterios de aceptación
- [x] `app/calculadora/index.html` abrible en navegador.
- [x] Cuatro operaciones básicas funcionan.
- [x] División por cero muestra error.
- [x] `node --test` pasa.
- [x] Sin `eval`.
