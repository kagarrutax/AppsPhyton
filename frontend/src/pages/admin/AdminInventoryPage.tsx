import { FormEvent, useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { useModal } from '../../context/ModalContext'
import { formatDate } from '../../lib/format'
import type { InventoryMovement, Product } from '../../types'

export default function AdminInventoryPage() {
  const { showError, showSuccess } = useModal()
  const [movements, setMovements] = useState<InventoryMovement[]>([])
  const [lowStock, setLowStock] = useState<Product[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({
    product_id: '',
    tipo: 'entrada' as 'entrada' | 'salida',
    cantidad: '1',
    motivo: '',
  })

  const load = async () => {
    setLoading(true)
    try {
      const [movRes, stockRes, prodRes] = await Promise.all([
        adminApi.inventory.movements(),
        adminApi.products.lowStock(),
        adminApi.products.list(),
      ])
      setMovements(movRes.data)
      setLowStock(stockRes.data)
      setProducts(prodRes.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!form.product_id) return
    try {
      await adminApi.inventory.createMovement({
        product_id: Number(form.product_id),
        tipo: form.tipo,
        cantidad: Number(form.cantidad),
        motivo: form.motivo || undefined,
      })
      showSuccess('Movimiento registrado')
      setForm({ product_id: '', tipo: 'entrada', cantidad: '1', motivo: '' })
      load()
    } catch {
      showError('No se pudo registrar el movimiento (verifica stock)')
    }
  }

  const productName = (id: number) => products.find((p) => p.id === id)?.nombre || `#${id}`

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold">Inventario</h1>
        <p className="text-gray-500 text-sm">Movimientos de stock y alertas</p>
      </div>

      {lowStock.length > 0 && (
        <section className="card p-5 border-orange-200 dark:border-orange-900">
          <h2 className="font-bold text-orange-600 mb-3">⚠ Stock bajo ({lowStock.length})</h2>
          <ul className="space-y-2 text-sm">
            {lowStock.map((p) => (
              <li key={p.id} className="flex justify-between">
                <span>{p.nombre}</span>
                <span className="font-semibold text-orange-600">{p.stock} / mín {p.stock_minimo}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="card p-5">
        <h2 className="font-bold mb-4">Registrar movimiento</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <select
            className="input-field"
            required
            value={form.product_id}
            onChange={(e) => setForm({ ...form, product_id: e.target.value })}
          >
            <option value="">Producto</option>
            {products.map((p) => (
              <option key={p.id} value={p.id}>{p.nombre} (stock: {p.stock})</option>
            ))}
          </select>
          <select className="input-field" value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value as 'entrada' | 'salida' })}>
            <option value="entrada">Entrada</option>
            <option value="salida">Salida</option>
          </select>
          <input className="input-field" type="number" min="1" required value={form.cantidad} onChange={(e) => setForm({ ...form, cantidad: e.target.value })} placeholder="Cantidad" />
          <input className="input-field" value={form.motivo} onChange={(e) => setForm({ ...form, motivo: e.target.value })} placeholder="Motivo (opcional)" />
          <button type="submit" className="btn-primary sm:col-span-2 lg:col-span-4 max-w-xs">Registrar</button>
        </form>
      </section>

      <section className="card overflow-x-auto">
        <h2 className="font-bold p-5 pb-0">Historial de movimientos</h2>
        {loading ? (
          <p className="p-5 text-gray-500">Cargando...</p>
        ) : movements.length === 0 ? (
          <p className="p-5 text-gray-500">Sin movimientos registrados.</p>
        ) : (
          <table className="w-full text-sm mt-4">
            <thead className="bg-surface-muted/50 dark:bg-gray-800/50 text-left">
              <tr>
                <th className="p-4 font-semibold">Fecha</th>
                <th className="p-4 font-semibold">Producto</th>
                <th className="p-4 font-semibold">Tipo</th>
                <th className="p-4 font-semibold">Cantidad</th>
                <th className="p-4 font-semibold">Stock</th>
                <th className="p-4 font-semibold">Motivo</th>
              </tr>
            </thead>
            <tbody>
              {movements.map((m) => (
                <tr key={m.id} className="border-t border-gray-100 dark:border-gray-700">
                  <td className="p-4 text-gray-500">{formatDate(m.fecha)}</td>
                  <td className="p-4 font-medium">{productName(m.product_id)}</td>
                  <td className="p-4">
                    <span className={`text-xs px-2 py-1 rounded-full ${m.tipo === 'entrada' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {m.tipo}
                    </span>
                  </td>
                  <td className="p-4">{m.cantidad}</td>
                  <td className="p-4">{m.stock_anterior} → {m.stock_nuevo}</td>
                  <td className="p-4 text-gray-500">{m.motivo || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  )
}
