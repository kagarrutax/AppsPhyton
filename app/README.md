## app/
Esta carpeta contiene la **aplicación final** (código ejecutable) del proyecto.

La orquestación basada en IA vive en:
- `spec/` (planes y especificaciones)
- `skill/` (skills de ejecución del agente)

Regla clave: `spec/` y `skill/` **no deben acoplarse** a la tecnología/framework dentro de `app/`.

## Aplicaciones

### calculadora/
Calculadora web (HTML, CSS, JS).

**Abrir en navegador:**
```powershell
cd app/calculadora
python -m http.server 8765
```
Luego visita: http://localhost:8765

**Tests:**
```powershell
node --test app/calculadora/tests/calculator.test.mjs
```
