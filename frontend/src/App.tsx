import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import ErrorBoundary from './components/ErrorBoundary'
import AdminRoute from './components/admin/AdminRoute'
import AdminLayout from './components/admin/AdminLayout'
import { AuthProvider, useAuth } from './context/AuthContext'
import { MenuNavProvider } from './context/MenuNavContext'
import { ModalProvider } from './context/ModalContext'
import { ThemeProvider } from './context/ThemeContext'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import CartPage from './pages/CartPage'
import OrdersPage from './pages/OrdersPage'
import OrderDetailPage from './pages/OrderDetailPage'
import ProfilePage from './pages/ProfilePage'
import AdminDashboardPage from './pages/admin/AdminDashboardPage'
import AdminProductsPage from './pages/admin/AdminProductsPage'
import AdminCategoriesPage from './pages/admin/AdminCategoriesPage'
import AdminOrdersPage from './pages/admin/AdminOrdersPage'
import AdminPaymentsPage from './pages/admin/AdminPaymentsPage'
import AdminUsersPage from './pages/admin/AdminUsersPage'
import AdminInventoryPage from './pages/admin/AdminInventoryPage'
import AdminDocumentsPage from './pages/admin/AdminDocumentsPage'
import AdminRolesPage from './pages/admin/AdminRolesPage'
import AdminAuditPage from './pages/admin/AdminAuditPage'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-page dark:bg-gray-900 text-gray-600 dark:text-gray-300">
        Cargando...
      </div>
    )
  }
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <ThemeProvider>
          <AuthProvider>
            <ModalProvider>
              <MenuNavProvider>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  <Route path="/cart" element={<PrivateRoute><CartPage /></PrivateRoute>} />
                  <Route path="/orders" element={<PrivateRoute><OrdersPage /></PrivateRoute>} />
                  <Route path="/orders/:id" element={<PrivateRoute><OrderDetailPage /></PrivateRoute>} />
                  <Route path="/profile" element={<PrivateRoute><ProfilePage /></PrivateRoute>} />
                  <Route path="/admin" element={<AdminRoute><AdminLayout /></AdminRoute>}>
                    <Route index element={<AdminDashboardPage />} />
                    <Route path="pagos" element={<AdminPaymentsPage />} />
                    <Route path="pedidos" element={<AdminOrdersPage />} />
                    <Route path="productos" element={<AdminProductsPage />} />
                    <Route path="categorias" element={<AdminCategoriesPage />} />
                    <Route path="usuarios" element={<AdminUsersPage />} />
                    <Route path="inventario" element={<AdminInventoryPage />} />
                    <Route path="documentos" element={<AdminDocumentsPage />} />
                    <Route path="roles" element={<AdminRolesPage />} />
                    <Route path="auditoria" element={<AdminAuditPage />} />
                  </Route>
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </MenuNavProvider>
            </ModalProvider>
          </AuthProvider>
        </ThemeProvider>
      </BrowserRouter>
    </ErrorBoundary>
  )
}
