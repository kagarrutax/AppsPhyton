export type Theme = 'light' | 'dark'

export const STORAGE_KEY = 'fastfood-theme'
export const THEME_CHANGE_EVENT = 'fastfood-theme-change'

export function readStoredTheme(): Theme | null {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light' || saved === 'dark') return saved
  } catch {
    /* localStorage bloqueado */
  }
  return null
}

export function getSystemTheme(): Theme {
  try {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  } catch {
    return 'light'
  }
}

export function resolveTheme(): Theme {
  return readStoredTheme() ?? getSystemTheme()
}

export function readThemeFromDom(): Theme {
  const root = document.documentElement
  if (root.dataset.theme === 'dark' || root.classList.contains('dark')) return 'dark'
  return 'light'
}

export function applyTheme(theme: Theme) {
  const root = document.documentElement
  root.classList.remove('light', 'dark')
  root.classList.add(theme)
  root.dataset.theme = theme
  root.style.colorScheme = theme

  if (document.body) {
    document.body.classList.remove('light', 'dark')
    document.body.classList.add(theme)
  }

  window.dispatchEvent(new CustomEvent(THEME_CHANGE_EVENT, { detail: theme }))
}

export function persistTheme(theme: Theme) {
  try {
    localStorage.setItem(STORAGE_KEY, theme)
  } catch {
    /* ignorar */
  }
}

export function initTheme(): Theme {
  const theme = resolveTheme()
  applyTheme(theme)
  return theme
}

export function toggleThemeValue(current: Theme): Theme {
  return current === 'dark' ? 'light' : 'dark'
}

export function subscribeTheme(onChange: () => void): () => void {
  const handler = () => onChange()
  window.addEventListener(THEME_CHANGE_EVENT, handler)
  return () => window.removeEventListener(THEME_CHANGE_EVENT, handler)
}

export function getThemeSnapshot(): Theme {
  return readThemeFromDom()
}

export function getThemeServerSnapshot(): Theme {
  return 'light'
}
