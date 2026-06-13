import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import UserFilter from '../../components/admin/UserFilter'
import { useModal } from '../../context/ModalContext'
import { formatDate, formatMoney } from '../../lib/format'
import type { Invoice, Ticket } from '../../types'

export default function AdminDocumentsPage() {
  const { showError } = useModal()
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [userFilter, setUserFilter] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const params = userFilter ? { user_id: Number(userFilter) } : undefined
      const [invRes, tickRes] = await Promise.all([
        adminApi.invoices.list(params),
        adminApi.tickets.list(params),
      ])
      setInvoices(invRes.data)
      setTickets(tickRes.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [userFilter])

  const downloadInvoice = async (id: number) => {
    try {
      await adminApi.invoices.downloadPdf(id)
    } catch {
      showError('No se pudo descargar la factura')
    }
  }

  const downloadTicket = async (id: number) => {
    try {
      await adminApi.tickets.downloadPdf(id)
    } catch {
      showError('No se pudo descargar el ticket')
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold">Facturas y tickets</h1>
          <p className="text-gray-500 text-sm">Documentos PDF generados tras aprobar pagos</p>
        </div>
        <UserFilter value={userFilter} onChange={setUserFilter} />
      </div>

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <section className="card p-5">
            <h2 className="font-bold mb-4">Facturas ({invoices.length})</h2>
            {invoices.length === 0 ? (
              <p className="text-gray-500 text-sm">No hay facturas.</p>
            ) : (
              <ul className="space-y-3">
                {invoices.map((inv) => (
                  <li key={inv.id} className="flex items-center justify-between gap-3 py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
                    <div>
                      <p className="font-medium">{inv.numero}</p>
                      <p className="text-xs text-gray-500">
                        Pedido #{inv.order_id} · Usuario #{inv.user_id} · {formatDate(inv.fecha)}
                      </p>
                      <p className="text-brand font-bold text-sm">{formatMoney(inv.total)}</p>
                    </div>
                    <button type="button" onClick={() => downloadInvoice(inv.id)} className="btn-outline !py-1.5 !px-3 text-xs shrink-0">
                      PDF
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="card p-5">
            <h2 className="font-bold mb-4">Tickets ({tickets.length})</h2>
            {tickets.length === 0 ? (
              <p className="text-gray-500 text-sm">No hay tickets.</p>
            ) : (
              <ul className="space-y-3">
                {tickets.map((tick) => (
                  <li key={tick.id} className="flex items-center justify-between gap-3 py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
                    <div>
                      <p className="font-medium">{tick.numero}</p>
                      <p className="text-xs text-gray-500">
                        Pedido #{tick.order_id} · Usuario #{tick.user_id} · {formatDate(tick.fecha)}
                      </p>
                      <p className="text-brand font-bold text-sm">{formatMoney(tick.total)}</p>
                    </div>
                    <button type="button" onClick={() => downloadTicket(tick.id)} className="btn-outline !py-1.5 !px-3 text-xs shrink-0">
                      PDF
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}
    </div>
  )
}
