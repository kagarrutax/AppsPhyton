import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import ThemeToggle from '../ThemeToggle'

const NAV = [
  { to: '/admin', label: 'Dashboard', end: true },
  { to: '/admin/pagos', label: 'Pagos' },
  { to: '/admin/pedidos', label: 'Pedidos' },
  { to: '/admin/inventario', label: 'Inventario' },
  { to: '/admin/documentos', label: 'Facturas' },
  { to: '/admin/productos', label: 'Productos' },
  { to: '/admin/categorias', label: 'Categorías' },
  { to: '/admin/usuarios', label: 'Usuarios' },
  { to: '/admin/roles', label: 'Roles' },
  { to: '/admin/auditoria', label: 'Auditoría' },
]

export default function AdminLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-surface-page dark:bg-gray-950 flex">
      <aside className="w-64 shrink-0 bg-gray-900 text-white flex flex-col">
        <div className="p-5 border-b border-gray-800">
          <p className="text-xs uppercase tracking-wider text-gray-400 mb-1">Panel</p>
          <h1 className="font-extrabold text-lg">
            Fast<span className="text-brand">Food</span>
          </h1>
          <p className="text-xs text-gray-400 mt-1">Administración</p>
        </div>

        <nav className="flex-1 p-3 space-y-1">
          {NAV.map(({ to, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `block px-4 py-2.5 rounded-xl text-sm font-medium transition ${
                  isActive
                    ? 'bg-brand text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-800 space-y-2">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:text-white rounded-xl hover:bg-gray-800 transition"
          >
            ← Volver a la tienda
          </button>
          <button
            type="button"
            onClick={() => { logout(); navigate('/') }}
            className="w-full text-left px-4 py-2 text-sm text-red-400 hover:text-red-300 rounded-xl hover:bg-gray-800 transition"
          >
            Cerrar sesión
          </button>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 bg-surface-elevated dark:bg-gray-900 border-b border-gray-200/80 dark:border-gray-800 flex items-center justify-between px-6 shrink-0">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Hola, <span className="font-semibold text-gray-900 dark:text-white">{user?.nombres}</span>
          </p>
          <ThemeToggle />
        </header>

        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
