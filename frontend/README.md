# FastFood Platform — Frontend

React + TypeScript + Tailwind CSS + Vite

## Stack

- React 18
- TypeScript
- Tailwind CSS 3
- Axios
- React Router 7
- Context API (autenticación JWT)

## Requisitos

- Node.js 18+
- Backend corriendo en http://localhost:8000

## Instalación

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Abre http://localhost:5173

## Páginas

| Ruta | Descripción |
|------|-------------|
| `/` | Inicio estilo Rappi (banner, categorías, productos) |
| `/login` | Inicio de sesión |
| `/register` | Registro de cliente |
| `/cart` | Carrito de compras |
| `/orders` | Historial de pedidos |
| `/orders/:id` | Detalle + subir comprobante de pago |
| `/profile` | Perfil y cambio de contraseña |

## Build producción

```powershell
npm run build
npm run preview
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `VITE_API_URL` | URL base API (default: http://localhost:8000/api/v1) |

El proxy de Vite redirige `/api` y `/uploads` al backend en desarrollo.
