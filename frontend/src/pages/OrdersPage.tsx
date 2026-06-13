import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import { orderApi } from '../api/services'
import { useAuth } from '../context/AuthContext'
import type { Order } from '../types'

const STATUS_LABELS: Record<string, { label: string; color: string }> = {
  pendiente: { label: 'Pendiente', color: 'bg-yellow-100 text-yellow-800' },
  pagado: { label: 'Pagado', color: 'bg-blue-100 text-blue-800' },
  verificado: { label: 'Verificado', color: 'bg-indigo-100 text-indigo-800' },
  preparando: { label: 'Preparando', color: 'bg-orange-100 text-orange-800' },
  listo: { label: 'Listo', color: 'bg-green-100 text-green-800' },
  entregado: { label: 'Entregado', color: 'bg-emerald-100 text-emerald-800' },
  cancelado: { label: 'Cancelado', color: 'bg-red-100 text-red-800' },
}

export default function OrdersPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }
    orderApi.list().then(({ data }) => setOrders(data)).finally(() => setLoading(false))
  }, [user, navigate])

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-extrabold mb-6">Mis pedidos</h1>

        {loading ? (
          <p className="text-gray-500">Cargando...</p>
        ) : orders.length === 0 ? (
          <div className="card p-12 text-center">
            <p className="text-5xl mb-4">📦</p>
            <p className="text-gray-500 mb-6">Aún no tienes pedidos</p>
            <Link to="/" className="btn-primary inline-block">Hacer un pedido</Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => {
              const st = STATUS_LABELS[order.estado] || { label: order.estado, color: 'bg-gray-100 text-gray-800' }
              return (
                <Link key={order.id} to={`/orders/${order.id}`} className="card p-5 block hover:shadow-md transition">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold">Pedido #{order.id}</span>
                    <span className={`text-xs font-semibold px-3 py-1 rounded-full ${st.color}`}>{st.label}</span>
                  </div>
                  <p className="text-sm text-gray-500">
                    {new Date(order.fecha_creacion).toLocaleDateString('es', { dateStyle: 'medium' })}
                    {' · '}{order.items.length} producto(s)
                  </p>
                  <p className="text-brand font-bold mt-2">${Number(order.total).toFixed(2)}</p>
                </Link>
              )
            })}
          </div>
        )}
      </div>
    </Layout>
  )
}
