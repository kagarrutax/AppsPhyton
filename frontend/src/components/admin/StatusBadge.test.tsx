import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { StatusBadge } from './StatusBadge'

describe('StatusBadge', () => {
  it('muestra etiqueta de pedido pendiente', () => {
    render(<StatusBadge status="pendiente" />)
    expect(screen.getByText('Pendiente')).toBeInTheDocument()
  })

  it('muestra etiqueta de pago aprobado', () => {
    render(<StatusBadge status="aprobado" type="payment" />)
    expect(screen.getByText('Aprobado')).toBeInTheDocument()
  })

  it('usa el status crudo si no está en el mapa', () => {
    render(<StatusBadge status="desconocido" />)
    expect(screen.getByText('desconocido')).toBeInTheDocument()
  })
})
