import { FormEvent, useEffect, useState } from 'react'
import { adminApi, paymentApi } from '../../api/services'
import { mediaUrl } from '../../api/client'
import UserFilter from '../../components/admin/UserFilter'
import { StatusBadge } from '../../components/admin/StatusBadge'
import { useModal } from '../../context/ModalContext'
import { formatDate, formatMoney } from '../../lib/format'
import type { Payment } from '../../types'

export default function AdminPaymentsPage() {
  const { showConfirm, showError, showSuccess } = useModal()
  const [payments, setPayments] = useState<Payment[]>([])
  const [loading, setLoading] = useState(true)
  const [rejectId, setRejectId] = useState<number | null>(null)
  const [rejectNotes, setRejectNotes] = useState('')
  const [userFilter, setUserFilter] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const params: { estado?: string; user_id?: number } = { estado: 'pendiente' }
      if (userFilter) params.user_id = Number(userFilter)
      const { data } = userFilter
        ? await adminApi.payments.list(params)
        : await paymentApi.pending()
      setPayments(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [userFilter])

  const handleApprove = async (p: Payment) => {
    const ok = await showConfirm(
      `¿Aprobar pago #${p.id} por ${formatMoney(p.monto)}? Se generará factura y ticket.`,
      'Aprobar pago'
    )
    if (!ok) return
    try {
      await paymentApi.approve(p.id)
      showSuccess('Pago aprobado. Factura y ticket generados.')
      load()
    } catch {
      showError('No se pudo aprobar el pago')
    }
  }

  const submitReject = async (e: FormEvent) => {
    e.preventDefault()
    if (!rejectId || rejectNotes.length < 5) return
    try {
      await paymentApi.reject(rejectId, rejectNotes)
      showSuccess('Pago rechazado')
      setRejectId(null)
      setRejectNotes('')
      load()
    } catch {
      showError('No se pudo rechazar el pago')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold">Pagos pendientes</h1>
        <p className="text-gray-500 text-sm">Revisa comprobantes y aprueba o rechaza transferencias</p>
      </div>

      <UserFilter value={userFilter} onChange={setUserFilter} />

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : payments.length === 0 ? (
        <div className="card p-12 text-center">
          <p className="text-4xl mb-3">✅</p>
          <p className="text-gray-500">No hay pagos pendientes de revisión.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {payments.map((p) => (
            <div key={p.id} className="card p-5">
              <div className="flex flex-col lg:flex-row gap-6">
                <div className="flex-1">
                  <div className="flex items-center gap-3 flex-wrap">
                    <h2 className="font-bold text-lg">Pago #{p.id}</h2>
                    <StatusBadge status={p.estado} type="payment" />
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    Pedido #{p.order_id} · Usuario #{p.user_id} · {formatDate(p.fecha_envio)}
                  </p>
                  <p className="text-2xl font-extrabold text-brand mt-3">{formatMoney(p.monto)}</p>
                  <div className="mt-4 flex flex-wrap gap-3">
                    <button type="button" onClick={() => handleApprove(p)} className="btn-primary !py-2 !px-4 text-sm">
                      Aprobar
                    </button>
                    <button
                      type="button"
                      onClick={() => { setRejectId(p.id); setRejectNotes('') }}
                      className="btn-outline !py-2 !px-4 text-sm !border-red-500 !text-red-500 hover:!bg-red-500"
                    >
                      Rechazar
                    </button>
                    <a
                      href={mediaUrl(p.comprobante)}
                      target="_blank"
                      rel="noreferrer"
                      className="text-sm font-semibold text-indigo-600 hover:underline self-center"
                    >
                      Ver comprobante
                    </a>
                  </div>
                </div>
                {p.comprobante && (
                  <a href={mediaUrl(p.comprobante)} target="_blank" rel="noreferrer" className="shrink-0">
                    <img
                      src={mediaUrl(p.comprobante)}
                      alt="Comprobante"
                      className="w-48 h-48 object-cover rounded-xl border border-gray-200 dark:border-gray-700"
                    />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {rejectId && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <form onSubmit={submitReject} className="card w-full max-w-md p-6 space-y-4">
            <h2 className="text-xl font-bold">Rechazar pago #{rejectId}</h2>
            <textarea
              className="input-field"
              rows={4}
              required
              minLength={5}
              placeholder="Motivo del rechazo (mín. 5 caracteres)"
              value={rejectNotes}
              onChange={(e) => setRejectNotes(e.target.value)}
            />
            <div className="flex gap-3 justify-end">
              <button type="button" onClick={() => setRejectId(null)} className="btn-outline">Cancelar</button>
              <button type="submit" className="btn-primary !bg-red-500 hover:!bg-red-600">Rechazar</button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
