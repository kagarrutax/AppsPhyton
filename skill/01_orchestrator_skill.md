# Skill: AI Orchestrator

## Propósito
Esta skill guía al agente de IA para ejecutar tareas de forma estructurada, asegurando que se siga el enfoque spec-as-source.

## Tareas

### 1. Fase de Análisis
- [ ] Leer el `spec/` correspondiente a la solicitud.
- [ ] Validar que el alcance y los pasos de implementación estén claros.
- [ ] Identificar posibles conflictos con el sistema actual.

### 2. Fase de Preparación
- [ ] Definir los casos de prueba (testing layer).
- [ ] Revisar el checklist de seguridad (security layer).

### 3. Fase de Ejecución Controlada
- [ ] Ejecutar cambios en la aplicación (`app/`) de forma incremental.
- [ ] Realizar pruebas después de cada cambio significativo.

### 4. Fase de Validación
- [ ] Ejecutar suite completa de tests.
- [ ] Verificar alineación con el `spec/`.
