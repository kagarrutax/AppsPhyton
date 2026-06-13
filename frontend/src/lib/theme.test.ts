import { describe, it, expect, beforeEach } from 'vitest'
import {
  applyTheme,
  readThemeFromDom,
  toggleThemeValue,
  THEME_CHANGE_EVENT,
} from './theme'

describe('theme', () => {
  beforeEach(() => {
    document.documentElement.classList.remove('light', 'dark')
    delete document.documentElement.dataset.theme
    document.documentElement.style.colorScheme = ''
    if (document.body) {
      document.body.classList.remove('light', 'dark')
    }
  })

  it('alterna entre light y dark', () => {
    expect(toggleThemeValue('light')).toBe('dark')
    expect(toggleThemeValue('dark')).toBe('light')
  })

  it('aplica clase dark en html', () => {
    applyTheme('dark')
    expect(document.documentElement.classList.contains('dark')).toBe(true)
    expect(readThemeFromDom()).toBe('dark')
  })

  it('aplica clase light en html', () => {
    applyTheme('light')
    expect(document.documentElement.classList.contains('light')).toBe(true)
    expect(readThemeFromDom()).toBe('light')
  })

  it('emite evento al cambiar tema', () => {
    let received: string | undefined
    const handler = (e: Event) => {
      received = (e as CustomEvent).detail
    }
    window.addEventListener(THEME_CHANGE_EVENT, handler)
    applyTheme('dark')
    window.removeEventListener(THEME_CHANGE_EVENT, handler)
    expect(received).toBe('dark')
  })
})
