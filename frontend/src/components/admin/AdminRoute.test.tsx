import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import AdminRoute from './AdminRoute'

const useAuthMock = vi.fn()

vi.mock('../../context/AuthContext', () => ({
  useAuth: () => useAuthMock(),
}))

function renderAdminRoute(initialPath = '/admin') {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route path="/login" element={<div>Página login</div>} />
        <Route path="/" element={<div>Tienda</div>} />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <div>Panel admin</div>
            </AdminRoute>
          }
        />
      </Routes>
    </MemoryRouter>
  )
}

describe('AdminRoute', () => {
  beforeEach(() => {
    useAuthMock.mockReset()
  })

  it('muestra cargando mientras auth está pendiente', () => {
    useAuthMock.mockReturnValue({ user: null, loading: true, isAdmin: false })
    renderAdminRoute()
    expect(screen.getByText('Cargando...')).toBeInTheDocument()
  })

  it('redirige a login si no hay usuario', () => {
    useAuthMock.mockReturnValue({ user: null, loading: false, isAdmin: false })
    renderAdminRoute()
    expect(screen.getByText('Página login')).toBeInTheDocument()
  })

  it('redirige a tienda si el usuario no es admin', () => {
    useAuthMock.mockReturnValue({
      user: { id: 1, nombres: 'María', roles: [{ id: 2, nombre: 'Cliente' }] },
      loading: false,
      isAdmin: false,
    })
    renderAdminRoute()
    expect(screen.getByText('Tienda')).toBeInTheDocument()
  })

  it('renderiza hijos si el usuario es admin', () => {
    useAuthMock.mockReturnValue({
      user: { id: 1, nombres: 'Admin', roles: [{ id: 1, nombre: 'Administrador' }] },
      loading: false,
      isAdmin: true,
    })
    renderAdminRoute()
    expect(screen.getByText('Panel admin')).toBeInTheDocument()
  })
})
