# AppsPhyton

Proyecto con enfoque **spec-as-source**: planificación y ejecución controlada por IA.

## Estructura

| Carpeta | Contenido |
|---------|-----------|
| `spec/` | Planes detallados por solicitud |
| `skill/` | Skills de ejecución para el agente |
| `app/` | Aplicaciones finales (código ejecutable) |

## Aplicación actual

- **Calculadora** → `app/calculadora/`
  - Spec: `spec/001-calculadora-html-css-js.md`
  - Skill: `skill/001-calculadora-html-css-js.md`

## Inicio rápido (calculadora)

```powershell
cd app/calculadora
python -m http.server 8765
```

Abre http://localhost:8765 en el navegador.
