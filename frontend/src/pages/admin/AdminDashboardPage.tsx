import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { adminApi } from '../../api/services'
import { formatDate, formatMoney } from '../../lib/format'
import type { DashboardStats } from '../../types'
import { StatusBadge } from '../../components/admin/StatusBadge'

function KpiCard({ label, value, hint, accent }: { label: string; value: string | number; hint?: string; accent?: string }) {
  return (
    <div className="card p-5">
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <p className={`text-3xl font-extrabold mt-1 ${accent || 'text-gray-900 dark:text-white'}`}>{value}</p>
      {hint && <p className="text-xs text-gray-400 mt-2">{hint}</p>}
    </div>
  )
}

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    adminApi.dashboard()
      .then(({ data }) => setStats(data))
      .catch((err) => {
        const status = err?.response?.status
        if (status === 404) {
          setError('El backend no tiene la ruta /dashboard. Reinicia el servidor API (uvicorn).')
        } else if (status === 403) {
          setError('No tienes permiso dashboard.read. Vuelve a iniciar sesión como administrador.')
        } else {
          setError('No se pudo conectar con la API. Verifica que el backend esté en http://127.0.0.1:8000')
        }
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-gray-500">Cargando dashboard...</p>
  if (!stats) {
    return (
      <div className="card p-8 text-center max-w-lg mx-auto">
        <p className="text-red-500 mb-2">No se pudo cargar el dashboard.</p>
        {error && <p className="text-sm text-gray-500 dark:text-gray-400">{error}</p>}
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">Resumen general del negocio</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        <KpiCard label="Ventas totales" value={formatMoney(stats.ventas_totales)} accent="text-brand" />
        <KpiCard label="Pedidos" value={stats.total_pedidos} />
        <KpiCard
          label="Pagos pendientes"
          value={stats.pagos_pendientes}
          accent={stats.pagos_pendientes > 0 ? 'text-yellow-600' : undefined}
          hint={stats.pagos_pendientes > 0 ? 'Requieren revisión' : undefined}
        />
        <KpiCard label="Productos" value={stats.total_productos} />
        <KpiCard
          label="Stock bajo"
          value={stats.productos_stock_bajo}
          accent={stats.productos_stock_bajo > 0 ? 'text-orange-600' : undefined}
        />
        <KpiCard label="Usuarios" value={stats.total_usuarios} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <section className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-lg">Pagos por revisar</h2>
            <Link to="/admin/pagos" className="text-sm text-brand font-semibold hover:underline">
              Ver todos
            </Link>
          </div>
          {stats.pagos_pendientes_recientes.length === 0 ? (
            <p className="text-gray-500 text-sm">No hay pagos pendientes.</p>
          ) : (
            <ul className="space-y-3">
              {stats.pagos_pendientes_recientes.map((p) => (
                <li key={p.id} className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
                  <div>
                    <p className="font-medium">Pago #{p.id} · Pedido #{p.order_id}</p>
                    <p className="text-xs text-gray-500">{formatDate(p.fecha_envio)}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-brand">{formatMoney(p.monto)}</p>
                    <StatusBadge status={p.estado} type="payment" />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-lg">Pedidos recientes</h2>
            <Link to="/admin/pedidos" className="text-sm text-brand font-semibold hover:underline">
              Ver todos
            </Link>
          </div>
          {stats.pedidos_recientes.length === 0 ? (
            <p className="text-gray-500 text-sm">Sin pedidos aún.</p>
          ) : (
            <ul className="space-y-3">
              {stats.pedidos_recientes.map((o) => (
                <li key={o.id} className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
                  <div>
                    <p className="font-medium">Pedido #{o.id}</p>
                    <p className="text-xs text-gray-500">Usuario #{o.user_id} · {formatDate(o.fecha_creacion)}</p>
                  </div>
                  <div className="text-right space-y-1">
                    <p className="font-bold">{formatMoney(o.total)}</p>
                    <StatusBadge status={o.estado} />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      {Object.keys(stats.pedidos_por_estado).length > 0 && (
        <section className="card p-5">
          <h2 className="font-bold text-lg mb-4">Pedidos por estado</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {Object.entries(stats.pedidos_por_estado).map(([estado, count]) => (
              <div key={estado} className="rounded-xl bg-gray-50 dark:bg-gray-800/50 p-4 text-center">
                <StatusBadge status={estado} />
                <p className="text-2xl font-bold mt-2">{count}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {stats.productos_stock_bajo_lista.length > 0 && (
        <section className="card p-5">
          <h2 className="font-bold text-lg mb-4">Productos con stock bajo</h2>
          <ul className="space-y-2">
            {stats.productos_stock_bajo_lista.map((p) => (
              <li key={p.id} className="flex justify-between text-sm">
                <span>{p.nombre}</span>
                <span className="text-orange-600 font-semibold">{p.stock} / mín {p.stock_minimo}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
