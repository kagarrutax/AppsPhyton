import { describe, expect, it } from 'vitest'
import { formatDate, formatMoney } from './format'

describe('formatMoney', () => {
  it('formatea números con dos decimales', () => {
    expect(formatMoney(12.5)).toBe('$12.50')
    expect(formatMoney('99.9')).toBe('$99.90')
  })

  it('maneja cero', () => {
    expect(formatMoney(0)).toBe('$0.00')
  })
})

describe('formatDate', () => {
  it('no lanza error con dateStyle y timeStyle', () => {
    const result = formatDate('2026-06-12T15:30:00Z')
    expect(typeof result).toBe('string')
    expect(result.length).toBeGreaterThan(0)
  })

  it('formatea fechas ISO válidas', () => {
    expect(() => formatDate('2026-01-01T10:00:00.000Z')).not.toThrow()
  })
})
