import { useTheme } from '../context/ThemeContext'

export default function ThemeToggle() {
  const { isDark, toggleTheme } = useTheme()

  return (
    <button
      type="button"
      onClick={() => toggleTheme()}
      aria-label={isDark ? 'Activar modo claro' : 'Activar modo noche'}
      aria-pressed={isDark}
      title={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo noche'}
      className={[
        'relative z-10 flex items-center gap-1.5 shrink-0',
        'px-2.5 py-2 sm:px-3 rounded-full text-sm font-semibold',
        'transition-all duration-200 active:scale-95 cursor-pointer',
        isDark
          ? 'bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 ring-2 ring-amber-400/60'
          : 'bg-slate-800/10 text-slate-700 hover:bg-slate-800/20 ring-1 ring-slate-300',
      ].join(' ')}
    >
      {isDark ? (
        <>
          <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden>
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
          <span className="hidden sm:inline">Modo claro</span>
        </>
      ) : (
        <>
          <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden>
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
            />
          </svg>
          <span className="hidden sm:inline">Modo noche</span>
        </>
      )}
    </button>
  )
}
