## Propósito de la skill
Ejecutar cualquier solicitud siguiendo **spec-as-source** con control por etapas, incorporando **testing** y **seguridad** como “gates” obligatorios, sin acoplar la orquestación (`spec/`, `skill/`) al contenido tecnológico de `app/`.

## Reglas de operación (no negociables)
- Antes de tocar `app/`, debe existir un spec en `spec/` para la solicitud actual.
- Antes de implementar, debe existir una skill en `skill/` para la solicitud actual.
- Ejecutar por etapas; si una etapa falla, **no avanzar**: corregir y revalidar.
- No introducir dependencias nuevas sin registrarlas en el spec (riesgo/impacto).
- No copiar secretos/credenciales en archivos del repo.

## Entrada requerida (del spec)
- Objetivo y alcance claros.
- Criterios de aceptación verificables.
- Plan por etapas con comandos o pasos de verificación.

## Tareas pequeñas y controladas (secuencia estándar)
### Etapa A — Inspección (read-only)
- Identificar estructura actual del repo y tecnologías en `app/` (si existe).
- Identificar comandos de test/lint disponibles (si existen).
- Registrar supuestos y riesgos si falta información.
- Resultado: “Mapa de ejecución” (qué se cambiará, dónde, cómo se probará).

### Etapa B — Implementación mínima (cambio pequeño)
- Implementar el mínimo que desbloquea valor y permite probar.
- Mantener cambios localizados; evitar refactors grandes sin necesidad.
- Resultado: build/ejecución local posible (si aplica).

### Etapa C — Gate de unit tests
- Añadir/actualizar pruebas unitarias según spec.
- Ejecutar pruebas unitarias.
- Resultado: pruebas unitarias pasan.

### Etapa D — Gate de pruebas funcionales
- Añadir/ejecutar pruebas funcionales (o pasos reproducibles) según spec.
- Resultado: flujos clave pasan.

### Etapa E — Gate de seguridad
- Ejecutar checklist de seguridad del spec:
  - Validación de entradas
  - Manejo de errores sin filtrar datos sensibles
  - Dependencias (si se agregaron)
  - Archivos/paths (si aplica)
  - Red/HTTP (si aplica)
- Resultado: no quedan hallazgos obvios sin mitigar.

### Etapa F — Cierre
- Ejecutar lint/format si existe.
- Verificar que criterios de aceptación están cumplidos.
- Documentar cambios (breve) en el spec de la solicitud.

## Evidencia mínima por etapa
- A: lista de archivos/áreas a tocar y comandos a correr.
- B: diff funcional.
- C/D: salida de comandos o confirmación verificable.
- E: checklist marcado con mitigaciones.
- F: resumen final + próximos pasos.
