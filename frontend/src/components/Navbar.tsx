import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useMenuNav, type MenuTab } from '../context/MenuNavContext'
import ThemeToggle from './ThemeToggle'

function NavTabButton({ tab, label }: { tab: MenuTab; label: string }) {
  const { tab: activeTab, setTab } = useMenuNav()
  const navigate = useNavigate()
  const location = useLocation()
  const isHome = location.pathname === '/'
  const isActive = isHome && activeTab === tab

  const handleClick = () => {
    if (location.pathname !== '/') {
      navigate('/')
    }
    setTab(tab, { scroll: true })
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-current={isActive ? 'page' : undefined}
      className={`relative text-sm font-semibold px-3 py-2 rounded-full transition ${
        isActive
          ? 'text-brand bg-brand/10 ring-1 ring-brand/30 dark:bg-brand/20'
          : 'text-gray-600 hover:text-brand hover:bg-surface-muted/60 dark:text-gray-300 dark:hover:bg-gray-800'
      }`}
    >
      {label}
    </button>
  )
}

export default function Navbar() {
  const { user, cartCount, logout, isAdmin } = useAuth()
  const { setTab } = useMenuNav()
  const navigate = useNavigate()

  const goHome = () => {
    navigate('/')
    setTab('todo', { scroll: true })
  }

  return (
    <header className="sticky top-0 z-50 bg-surface-elevated/95 dark:bg-gray-900/95 backdrop-blur border-b border-gray-200/80 dark:border-gray-800 shadow-sm transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16 gap-2">
        <button type="button" onClick={goHome} className="flex items-center gap-2 shrink-0">
          <span className="w-9 h-9 bg-brand rounded-xl flex items-center justify-center text-white font-bold text-lg">
            F
          </span>
          <span className="font-extrabold text-xl text-gray-900 dark:text-white hidden sm:block">
            Fast<span className="text-brand">Food</span>
          </span>
        </button>

        <nav className="hidden md:flex items-center gap-2 mr-2">
          <NavTabButton tab="todo" label="Menú" />
          <NavTabButton tab="destacados" label="Destacados" />
          <NavTabButton tab="combos" label="Combos" />
        </nav>

        <nav className="flex items-center gap-1 sm:gap-2 shrink-0">
          <ThemeToggle />

          {user ? (
            <>
              <button
                type="button"
                onClick={() => navigate('/orders')}
                className="text-sm font-medium text-gray-600 hover:text-brand dark:text-gray-300 hidden sm:block"
              >
                Mis pedidos
              </button>
              <button
                type="button"
                onClick={() => navigate('/cart')}
                className="relative p-2 rounded-full hover:bg-surface-muted dark:hover:bg-gray-800 transition"
                aria-label="Carrito"
              >
                <svg className="w-6 h-6 text-gray-700 dark:text-gray-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                {cartCount > 0 && (
                  <span className="absolute -top-0.5 -right-0.5 bg-brand text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
                    {cartCount > 9 ? '9+' : cartCount}
                  </span>
                )}
              </button>
              <button
                type="button"
                onClick={() => navigate('/profile')}
                className="text-sm font-medium text-gray-700 hover:text-brand dark:text-gray-200 hidden sm:block"
              >
                {user.nombres}
              </button>
              {isAdmin && (
                <button
                  type="button"
                  onClick={() => navigate('/admin')}
                  className="text-xs bg-gray-900 dark:bg-brand text-white px-3 py-1.5 rounded-full font-semibold"
                >
                  Admin
                </button>
              )}
              <button
                onClick={() => { logout(); navigate('/') }}
                className="text-sm text-gray-500 hover:text-red-500 dark:text-gray-400"
              >
                Salir
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                onClick={() => navigate('/login')}
                className="text-sm font-semibold text-gray-700 hover:text-brand dark:text-gray-200 px-2 sm:px-3 py-2"
              >
                Ingresar
              </button>
              <button
                type="button"
                onClick={() => navigate('/register')}
                className="btn-primary text-sm !py-2 !px-4"
              >
                Registrarse
              </button>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
