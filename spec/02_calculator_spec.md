# Spec: Calculadora Web

## Objetivo
Desarrollar una calculadora web funcional, estéticamente atractiva (WOW factor) y accesible, siguiendo los mejores estándares de desarrollo.

## Alcance
- **Funcionalidades Básicas**: Suma, resta, multiplicación, división, borrado y manejo de decimales.
- **Interfaz**: Diseño moderno con CSS Vanilla, responsive y con micro-animaciones.
- **Accesibilidad**: Uso de ARIA labels y soporte para navegación por teclado.
- **Testing**: Suite de pruebas unitarias para la lógica de cálculo.

## Pasos de Implementación
1. **Refactorización de Lógica**: Asegurar que `calculator.js` maneje correctamente todos los casos de borde (división por cero, precisión decimal).
2. **Mejora de UI**: Aplicar un diseño premium con gradientes y efectos de hover.
3. **Capa de Pruebas**: Expandir `tests/` para cubrir todos los operadores.
4. **Validación de Seguridad**: Revisar el manejo de entradas para prevenir inyecciones o errores inesperados.

## Riesgos y Supuestos
- **Riesgo**: Inconsistencias en el renderizado entre navegadores.
- **Supuesto**: Se utiliza ES Modules para la organización del código.
