export interface User {
  id: number
  nombres: string
  apellidos: string
  email: string
  telefono?: string
  estado: boolean
  roles: { id: number; nombre: string }[]
}

export interface Category {
  id: number
  nombre: string
  descripcion?: string
  estado: boolean
}

export interface Product {
  id: number
  nombre: string
  descripcion?: string
  precio: number
  stock: number
  stock_minimo: number
  category_id?: number
  imagen?: string
  estado: boolean
  category?: Category
}

export interface CartItem {
  id: number
  product_id: number
  cantidad: number
  precio_unitario: number
  subtotal: number
  product?: Product
}

export interface Cart {
  id: number
  user_id: number
  items: CartItem[]
  total: number
  cantidad_items: number
}

export interface OrderItem {
  id: number
  product_id?: number
  product_nombre: string
  cantidad: number
  precio_unitario: number
  subtotal: number
}

export interface Order {
  id: number
  user_id: number
  estado: string
  total: number
  notas?: string
  fecha_creacion: string
  items: OrderItem[]
}

export interface Payment {
  id: number
  order_id: number
  user_id: number
  monto: number
  comprobante: string
  estado: string
  notas_rechazo?: string
  fecha_envio: string
  fecha_revision?: string
}

export interface DashboardStats {
  total_usuarios: number
  total_productos: number
  total_pedidos: number
  pagos_pendientes: number
  productos_stock_bajo: number
  ventas_totales: number
  pedidos_por_estado: Record<string, number>
  pagos_pendientes_recientes: Payment[]
  productos_stock_bajo_lista: Product[]
  pedidos_recientes: Order[]
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface InventoryMovement {
  id: number
  product_id: number
  user_id?: number
  tipo: 'entrada' | 'salida'
  cantidad: number
  stock_anterior: number
  stock_nuevo: number
  motivo?: string
  fecha: string
}

export interface Invoice {
  id: number
  order_id: number
  user_id: number
  numero: string
  total: number
  pdf_path: string
  fecha: string
}

export interface Ticket {
  id: number
  order_id: number
  user_id: number
  numero: string
  total: number
  pdf_path: string
  fecha: string
}

export interface Permission {
  id: number
  nombre: string
  modulo: string
  descripcion?: string
}

export interface Role {
  id: number
  nombre: string
  descripcion?: string
  permissions: Permission[]
}

export interface AuditLog {
  id: number
  user_id?: number
  accion: string
  modulo: string
  detalle?: string
  ip_address?: string
  fecha: string
}
