# Proyecto: AI-Assisted System Design (Spec-as-Source)

## Objetivo
Establecer un framework de trabajo donde la Inteligencia Artificial actúa como un desarrollador senior, siguiendo planes detallados (`spec/`) y utilizando habilidades específicas (`skill/`) antes de realizar cualquier implementación en la aplicación (`app/`).

## Alcance
- **Capa de Orquestación**: Gestión de planes y habilidades de IA.
- **Capa de Aplicación**: Implementación limpia y desacoplada.
- **Testing y Seguridad**: Validación obligatoria en cada etapa.

## Principios
1. **Spec-as-Source**: El plan es la fuente de verdad.
2. **Desacoplamiento**: La lógica de orquestación no interfiere con el framework de la aplicación.
3. **Ejecución Progresiva**: Análisis primero, ejecución por etapas después.
4. **Validación Continua**: Pruebas y checklists de seguridad integrados.

## Riesgos y Supuestos
- **Riesgo**: Desviación del plan original durante la ejecución.
- **Mitigación**: Revisiones constantes del `spec/` antes de cada tarea en `skill/`.
- **Supuesto**: El entorno soporta la ejecución de pruebas unitarias.
