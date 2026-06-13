import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { formatDate } from '../../lib/format'
import type { AuditLog } from '../../types'

const MODULOS = ['auth', 'users', 'products', 'orders', 'payments', 'cart', 'inventory', 'categories']

export default function AdminAuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([])
  const [loading, setLoading] = useState(true)
  const [modulo, setModulo] = useState('')

  useEffect(() => {
    setLoading(true)
    adminApi.audit
      .list({ modulo: modulo || undefined })
      .then(({ data }) => setLogs(data))
      .finally(() => setLoading(false))
  }, [modulo])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold">Auditoría</h1>
        <p className="text-gray-500 text-sm">Registro de acciones del sistema</p>
      </div>

      <select className="input-field max-w-xs" value={modulo} onChange={(e) => setModulo(e.target.value)}>
        <option value="">Todos los módulos</option>
        {MODULOS.map((m) => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : logs.length === 0 ? (
        <p className="text-gray-500">No hay registros.</p>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-surface-muted/50 dark:bg-gray-800/50 text-left">
              <tr>
                <th className="p-4 font-semibold">Fecha</th>
                <th className="p-4 font-semibold">Módulo</th>
                <th className="p-4 font-semibold">Acción</th>
                <th className="p-4 font-semibold">Detalle</th>
                <th className="p-4 font-semibold">Usuario</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="border-t border-gray-100 dark:border-gray-700">
                  <td className="p-4 text-gray-500 whitespace-nowrap">{formatDate(log.fecha)}</td>
                  <td className="p-4">
                    <span className="text-xs bg-surface-muted dark:bg-gray-700 px-2 py-1 rounded-full">{log.modulo}</span>
                  </td>
                  <td className="p-4 font-medium">{log.accion}</td>
                  <td className="p-4 text-gray-600 dark:text-gray-300 max-w-md truncate">{log.detalle || '—'}</td>
                  <td className="p-4 text-gray-500">{log.user_id ? `#${log.user_id}` : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
