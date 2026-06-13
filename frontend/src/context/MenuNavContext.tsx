import {
  createContext,
  useCallback,
  useContext,
  useRef,
  useState,
  type ReactNode,
} from 'react'

export type MenuTab = 'todo' | 'destacados' | 'combos' | `cat-${number}`

interface SetTabOptions {
  scroll?: boolean
}

interface MenuNavContextValue {
  tab: MenuTab
  setTab: (tab: MenuTab, options?: SetTabOptions) => void
  registerMenuContent: (el: HTMLElement | null) => void
}

const MenuNavContext = createContext<MenuNavContextValue | null>(null)

export function MenuNavProvider({ children }: { children: ReactNode }) {
  const [tab, setTabState] = useState<MenuTab>('todo')
  const contentEl = useRef<HTMLElement | null>(null)
  const pendingScroll = useRef(false)

  const scrollToMenu = useCallback(() => {
    contentEl.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, [])

  const registerMenuContent = useCallback(
    (el: HTMLElement | null) => {
      contentEl.current = el
      if (el && pendingScroll.current) {
        pendingScroll.current = false
        requestAnimationFrame(scrollToMenu)
      }
    },
    [scrollToMenu]
  )

  const setTab = useCallback(
    (next: MenuTab, options?: SetTabOptions) => {
      setTabState(next)
      if (options?.scroll) {
        if (contentEl.current) {
          requestAnimationFrame(scrollToMenu)
        } else {
          pendingScroll.current = true
        }
      }
    },
    [scrollToMenu]
  )

  return (
    <MenuNavContext.Provider value={{ tab, setTab, registerMenuContent }}>
      {children}
    </MenuNavContext.Provider>
  )
}

export function useMenuNav() {
  const ctx = useContext(MenuNavContext)
  if (!ctx) throw new Error('useMenuNav debe usarse dentro de MenuNavProvider')
  return ctx
}

export function parseMenuTab(raw: string | null | undefined): MenuTab {
  if (!raw || raw === 'todo') return 'todo'
  if (raw === 'destacados' || raw === 'combos' || raw === 'ofertas') {
    return raw === 'ofertas' ? 'combos' : raw
  }
  if (raw.startsWith('cat-')) return raw as MenuTab
  const n = Number(raw)
  if (!Number.isNaN(n) && n > 0) return `cat-${n}`
  return 'todo'
}
