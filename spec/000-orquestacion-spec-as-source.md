## Objetivo
Establecer una capa de orquestación basada en IA con enfoque **spec-as-source** que:
- Mantenga el contexto del proyecto (norte) y reduzca desviaciones.
- Obligue a planificar antes de implementar.
- Ejecute cambios de forma progresiva, con validaciones de **testing** y **seguridad**.

## Alcance
- **Incluye**:
  - Estructura fija de carpetas:
    - `spec/`: planes detallados por solicitud (fuente de verdad).
    - `skill/`: skills de ejecución para el agente (pasos pequeños y controlados).
    - `app/`: aplicación final (cualquier tecnología), **sin acoplarse** a `spec/`/`skill/`.
  - Plantillas y convenciones para specs/skills.
  - Checklist mínimo de testing y seguridad por solicitud.
- **No incluye**:
  - Implementación de funcionalidades dentro de `app/` (solo se hará cuando una solicitud concreta lo requiera y esté especificada).
  - Dependencia de framework/librería concreta para la capa de orquestación.

## Convenciones (spec-as-source)
- Cada solicitud debe generar:
  - Un spec en `spec/` con: **Objetivo, Alcance, Pasos, Riesgos y supuestos, Testing, Seguridad, Criterios de aceptación**.
  - Una skill en `skill/` con: **tareas pequeñas**, “gates” de validación y orden de ejecución.
- El agente **no programa de inmediato**: primero crea/actualiza el spec, después crea la skill, luego ejecuta por etapas.
- `spec/` y `skill/` son **orquestación IA** y no deben importar/depender de código de `app/`.

## Pasos de implementación (para futuras solicitudes)
1. Crear `spec/<id>-<tema>.md` usando la plantilla base.
2. Crear `skill/<id>-<tema>.md` usando la plantilla base.
3. Ejecutar por etapas:
   - Etapa A: inspección (estado repo, estructura, dependencias).
   - Etapa B: cambios mínimos viables en `app/` (si aplica).
   - Etapa C: pruebas unitarias.
   - Etapa D: pruebas funcionales.
   - Etapa E: checklist de seguridad.
   - Etapa F: verificación final (lint/format si aplica) y resumen.

## Riesgos y supuestos
- **Riesgo**: specs demasiado genéricos → mitigación: criterios de aceptación verificables.
- **Riesgo**: sobrecarga de proceso para cambios pequeños → mitigación: specs cortos pero completos; ejecutar en incremental.
- **Supuesto**: el repo puede ser multi-tecnología; `app/` puede contener Python/Node/etc.
- **Supuesto**: el entorno de ejecución y pruebas depende de `app/` y se definirá por solicitud.

## Capa de testing (obligatoria por solicitud)
- **Unitarias**:
  - Definir qué unidades se validan (funciones/clases/módulos).
  - Definir entradas/salidas y casos borde (null/empty/errores).
  - Criterio: pruebas pasan en local antes de avanzar de etapa.
- **Funcionales**:
  - Definir flujos “happy path” y fallos esperables.
  - Criterio: evidencia ejecutable (comando/resultado) o reproducción clara.

## Capa de seguridad (obligatoria por solicitud)
Checklist mínimo:
- **Entrada/validación**: sanitización, tipos, límites, manejo de errores seguro.
- **Secretos**: no commitear tokens/keys; evitar logs con datos sensibles.
- **Dependencias**: revisar riesgos obvios (paquetes abandonados, uso inseguro).
- **Archivos/paths**: evitar path traversal, permisos excesivos.
- **Red/HTTP**: timeouts, TLS, validación de certificados (según aplique).

## Criterios de aceptación (meta)
- Existe estructura `spec/`, `skill/`, `app/`.
- Existe este documento como “contrato” del proceso.
- Existen plantillas en `spec/` y `skill/` que guían futuras solicitudes.
