import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import UserFilter from '../../components/admin/UserFilter'
import { StatusBadge } from '../../components/admin/StatusBadge'
import { ORDER_STATUSES } from '../../constants/orderStatus'
import { useModal } from '../../context/ModalContext'
import { formatDate, formatMoney } from '../../lib/format'
import type { Order } from '../../types'

export default function AdminOrdersPage() {
  const { showConfirm, showError, showSuccess } = useModal()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')
  const [userFilter, setUserFilter] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await adminApi.orders.list({
        estado: filter || undefined,
        user_id: userFilter ? Number(userFilter) : undefined,
      })
      setOrders(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [filter, userFilter])

  const changeStatus = async (order: Order, estado: string) => {
    if (order.estado === estado) return
    try {
      await adminApi.orders.updateStatus(order.id, estado)
      showSuccess(`Pedido #${order.id} → ${estado}`)
      load()
    } catch {
      showError('Transición de estado no permitida')
    }
  }

  const handleDelete = async (order: Order) => {
    const ok = await showConfirm(`¿Eliminar pedido #${order.id}?`, 'Eliminar pedido')
    if (!ok) return
    try {
      await adminApi.orders.remove(order.id)
      showSuccess('Pedido eliminado')
      load()
    } catch {
      showError('Solo se pueden eliminar pedidos pendientes o cancelados')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold">Pedidos</h1>
        <p className="text-gray-500 text-sm">Gestiona todos los pedidos del sistema</p>
      </div>

      <div className="flex flex-wrap gap-3">
        <select className="input-field max-w-xs" value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="">Todos los estados</option>
          {ORDER_STATUSES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <UserFilter value={userFilter} onChange={setUserFilter} />
      </div>

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : orders.length === 0 ? (
        <p className="text-gray-500">No hay pedidos.</p>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div key={order.id} className="card p-5">
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-3 flex-wrap">
                    <h2 className="font-bold text-lg">Pedido #{order.id}</h2>
                    <StatusBadge status={order.estado} />
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    Usuario #{order.user_id} · {formatDate(order.fecha_creacion)}
                  </p>
                  {order.notas && <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">Notas: {order.notas}</p>}
                </div>
                <p className="text-xl font-extrabold text-brand">{formatMoney(order.total)}</p>
              </div>

              <ul className="mt-4 text-sm space-y-1 border-t border-gray-100 dark:border-gray-700 pt-3">
                {order.items.map((item) => (
                  <li key={item.id} className="flex justify-between">
                    <span>{item.cantidad}x {item.product_nombre}</span>
                    <span>{formatMoney(item.subtotal)}</span>
                  </li>
                ))}
              </ul>

              <div className="mt-4 flex flex-wrap items-center gap-3">
                <select
                  className="input-field !py-2 !px-3 text-sm max-w-[180px]"
                  value={order.estado}
                  onChange={(e) => changeStatus(order, e.target.value)}
                >
                  {ORDER_STATUSES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
                <button type="button" onClick={() => handleDelete(order)} className="text-sm text-red-500 font-semibold">
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
