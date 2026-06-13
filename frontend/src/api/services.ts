import { api } from './client'
import type {
  Cart,
  Category,
  DashboardStats,
  AuditLog,
  InventoryMovement,
  Invoice,
  Order,
  Payment,
  Permission,
  Product,
  Role,
  Ticket,
  TokenResponse,
  User,
} from '../types'

export const authApi = {
  login: (email: string, password: string) =>
    api.post<TokenResponse>('/auth/login', { email, password }),
  register: (data: {
    nombres: string
    apellidos: string
    email: string
    telefono?: string
    password: string
  }) => api.post<User>('/auth/register', data),
  me: () => api.get<User>('/auth/me'),
  changePassword: (current_password: string, new_password: string) =>
    api.post('/auth/change-password', { current_password, new_password }),
}

export const catalogApi = {
  publicProducts: (params?: { search?: string; category_id?: number; limit?: number }) =>
    api.get<Product[]>('/products/public', { params }),
  categories: () => api.get<Category[]>('/categories', { params: { only_active: true } }),
}

export const cartApi = {
  get: () => api.get<Cart>('/cart'),
  add: (product_id: number, cantidad = 1) =>
    api.post<Cart>('/cart/items', { product_id, cantidad }),
  update: (product_id: number, cantidad: number) =>
    api.put<Cart>(`/cart/items/${product_id}`, { cantidad }),
  remove: (product_id: number) => api.delete<Cart>(`/cart/items/${product_id}`),
  clear: () => api.delete<Cart>('/cart/clear'),
}

export const orderApi = {
  list: () => api.get<Order[]>('/orders'),
  checkout: (notas?: string) => api.post<Order>('/orders/checkout', { notas }),
  get: (id: number) => api.get<Order>(`/orders/${id}`),
}

export const paymentApi = {
  submit: (orderId: number, file: File) => {
    const form = new FormData()
    form.append('file', file)
    return api.post<Payment>(`/payments/orders/${orderId}`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  list: (params?: { estado?: string; user_id?: number }) =>
    api.get<Payment[]>('/payments', { params }),
  pending: () => api.get<Payment[]>('/payments/pending'),
  approve: (id: number) => api.post<Payment>(`/payments/${id}/approve`),
  reject: (id: number, notas_rechazo: string) =>
    api.post<Payment>(`/payments/${id}/reject`, { notas_rechazo }),
}

export const adminApi = {
  dashboard: () => api.get<DashboardStats>('/dashboard'),
  products: {
    list: (params?: { search?: string; category_id?: number; only_active?: boolean }) =>
      api.get<Product[]>('/products', { params }),
    lowStock: () => api.get<Product[]>('/products/low-stock'),
    create: (data: Partial<Product>) => api.post<Product>('/products', data),
    update: (id: number, data: Partial<Product>) => api.put<Product>(`/products/${id}`, data),
    activate: (id: number) => api.patch<Product>(`/products/${id}/activate`),
    deactivate: (id: number) => api.patch<Product>(`/products/${id}/deactivate`),
    uploadImage: (id: number, file: File) => {
      const form = new FormData()
      form.append('file', file)
      return api.post<Product>(`/products/${id}/imagen`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    },
    remove: (id: number) => api.delete(`/products/${id}`),
  },
  categories: {
    list: () => api.get<Category[]>('/categories'),
    create: (data: Partial<Category>) => api.post<Category>('/categories', data),
    update: (id: number, data: Partial<Category>) => api.put<Category>(`/categories/${id}`, data),
    remove: (id: number) => api.delete(`/categories/${id}`),
  },
  orders: {
    list: (params?: { estado?: string; user_id?: number }) =>
      api.get<Order[]>('/orders', { params }),
    updateStatus: (id: number, estado: string) =>
      api.patch<Order>(`/orders/${id}/status`, { estado }),
    remove: (id: number) => api.delete(`/orders/${id}`),
  },
  users: {
    list: (params?: { search?: string }) => api.get<User[]>('/users', { params }),
    update: (id: number, data: Partial<User>) => api.put<User>(`/users/${id}`, data),
  },
  inventory: {
    movements: (params?: { product_id?: number; tipo?: string }) =>
      api.get<InventoryMovement[]>('/inventory/movements', { params }),
    createMovement: (data: {
      product_id: number
      tipo: 'entrada' | 'salida'
      cantidad: number
      motivo?: string
    }) => api.post<InventoryMovement>('/inventory/movements', data),
  },
  invoices: {
    list: (params?: { user_id?: number }) => api.get<Invoice[]>('/invoices', { params }),
    downloadPdf: (id: number) => downloadPdf(`/invoices/${id}/pdf`, `factura-${id}.pdf`),
  },
  tickets: {
    list: (params?: { user_id?: number }) => api.get<Ticket[]>('/tickets', { params }),
    downloadPdf: (id: number) => downloadPdf(`/tickets/${id}/pdf`, `ticket-${id}.pdf`),
  },
  roles: {
    list: () => api.get<Role[]>('/roles'),
  },
  permissions: {
    list: () => api.get<Permission[]>('/permissions'),
  },
  audit: {
    list: (params?: { modulo?: string; accion?: string }) =>
      api.get<AuditLog[]>('/audit-logs', { params }),
  },
  payments: {
    list: (params?: { estado?: string; user_id?: number }) =>
      api.get<Payment[]>('/payments', { params }),
  },
}

async function downloadPdf(path: string, filename: string) {
  const { data } = await api.get(path, { responseType: 'blob' })
  const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
