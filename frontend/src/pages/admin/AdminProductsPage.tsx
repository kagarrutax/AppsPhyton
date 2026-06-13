import { FormEvent, useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { mediaUrl } from '../../api/client'
import { useModal } from '../../context/ModalContext'
import { formatMoney } from '../../lib/format'
import type { Category, Product } from '../../types'

const emptyForm = {
  nombre: '',
  descripcion: '',
  precio: '',
  stock: '0',
  stock_minimo: '5',
  category_id: '',
  estado: true,
}

export default function AdminProductsPage() {
  const { showConfirm, showError, showSuccess } = useModal()
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [editing, setEditing] = useState<Product | null>(null)
  const [form, setForm] = useState(emptyForm)
  const [showForm, setShowForm] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const [prodRes, catRes] = await Promise.all([
        adminApi.products.list({ search: search || undefined }),
        adminApi.categories.list(),
      ])
      setProducts(prodRes.data)
      setCategories(catRes.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [search])

  const openCreate = () => {
    setEditing(null)
    setForm(emptyForm)
    setShowForm(true)
  }

  const openEdit = (p: Product) => {
    setEditing(p)
    setForm({
      nombre: p.nombre,
      descripcion: p.descripcion || '',
      precio: String(p.precio),
      stock: String(p.stock),
      stock_minimo: String(p.stock_minimo),
      category_id: p.category_id ? String(p.category_id) : '',
      estado: p.estado,
    })
    setShowForm(true)
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const payload = {
      nombre: form.nombre,
      descripcion: form.descripcion || undefined,
      precio: Number(form.precio),
      stock: Number(form.stock),
      stock_minimo: Number(form.stock_minimo),
      category_id: form.category_id ? Number(form.category_id) : undefined,
      estado: form.estado,
    }
    try {
      if (editing) {
        await adminApi.products.update(editing.id, payload)
        showSuccess('Producto actualizado')
      } else {
        await adminApi.products.create(payload)
        showSuccess('Producto creado')
      }
      setShowForm(false)
      load()
    } catch {
      showError('No se pudo guardar el producto')
    }
  }

  const toggleActive = async (p: Product) => {
    try {
      if (p.estado) await adminApi.products.deactivate(p.id)
      else await adminApi.products.activate(p.id)
      load()
    } catch {
      showError('No se pudo cambiar el estado')
    }
  }

  const handleDelete = async (p: Product) => {
    const ok = await showConfirm(`¿Eliminar "${p.nombre}"?`, 'Eliminar producto')
    if (!ok) return
    try {
      await adminApi.products.remove(p.id)
      showSuccess('Producto eliminado')
      load()
    } catch {
      showError('No se pudo eliminar el producto')
    }
  }

  const handleImage = async (p: Product, file: File) => {
    try {
      await adminApi.products.uploadImage(p.id, file)
      showSuccess('Imagen actualizada')
      load()
    } catch {
      showError('No se pudo subir la imagen')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold">Productos</h1>
          <p className="text-gray-500 text-sm">Gestiona el catálogo</p>
        </div>
        <button type="button" onClick={openCreate} className="btn-primary">+ Nuevo producto</button>
      </div>

      <input
        type="search"
        placeholder="Buscar producto..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="input-field max-w-md"
      />

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-800/50 text-left">
              <tr>
                <th className="p-4 font-semibold">Producto</th>
                <th className="p-4 font-semibold">Precio</th>
                <th className="p-4 font-semibold">Stock</th>
                <th className="p-4 font-semibold">Estado</th>
                <th className="p-4 font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id} className="border-t border-gray-100 dark:border-gray-700">
                  <td className="p-4">
                    <div className="flex items-center gap-3">
                      {p.imagen ? (
                        <img src={mediaUrl(p.imagen)} alt="" className="w-10 h-10 rounded-lg object-cover" />
                      ) : (
                        <span className="w-10 h-10 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center">🍔</span>
                      )}
                      <div>
                        <p className="font-medium">{p.nombre}</p>
                        <p className="text-xs text-gray-500">{p.category?.nombre || 'Sin categoría'}</p>
                      </div>
                    </div>
                  </td>
                  <td className="p-4 font-semibold text-brand">{formatMoney(p.precio)}</td>
                  <td className="p-4">
                    <span className={p.stock <= p.stock_minimo ? 'text-orange-600 font-semibold' : ''}>
                      {p.stock}
                    </span>
                  </td>
                  <td className="p-4">
                    <span className={`text-xs px-2 py-1 rounded-full ${p.estado ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-600'}`}>
                      {p.estado ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="p-4">
                    <div className="flex flex-wrap gap-2">
                      <button type="button" onClick={() => openEdit(p)} className="text-brand text-xs font-semibold">Editar</button>
                      <button type="button" onClick={() => toggleActive(p)} className="text-xs font-semibold text-gray-600 dark:text-gray-300">
                        {p.estado ? 'Desactivar' : 'Activar'}
                      </button>
                      <label className="text-xs font-semibold text-indigo-600 cursor-pointer">
                        Imagen
                        <input type="file" accept="image/*" className="hidden" onChange={(e) => e.target.files?.[0] && handleImage(p, e.target.files[0])} />
                      </label>
                      <button type="button" onClick={() => handleDelete(p)} className="text-xs font-semibold text-red-500">Eliminar</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showForm && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <form onSubmit={handleSubmit} className="card w-full max-w-lg p-6 space-y-4 max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold">{editing ? 'Editar producto' : 'Nuevo producto'}</h2>
            <input className="input-field" placeholder="Nombre" required value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
            <textarea className="input-field" placeholder="Descripción" rows={2} value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
            <div className="grid grid-cols-2 gap-3">
              <input className="input-field" type="number" step="0.01" min="0" placeholder="Precio" required value={form.precio} onChange={(e) => setForm({ ...form, precio: e.target.value })} />
              <select className="input-field" value={form.category_id} onChange={(e) => setForm({ ...form, category_id: e.target.value })}>
                <option value="">Sin categoría</option>
                {categories.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
              </select>
              <input className="input-field" type="number" min="0" placeholder="Stock" value={form.stock} onChange={(e) => setForm({ ...form, stock: e.target.value })} />
              <input className="input-field" type="number" min="0" placeholder="Stock mínimo" value={form.stock_minimo} onChange={(e) => setForm({ ...form, stock_minimo: e.target.value })} />
            </div>
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.checked })} />
              Producto activo
            </label>
            <div className="flex gap-3 justify-end">
              <button type="button" onClick={() => setShowForm(false)} className="btn-outline">Cancelar</button>
              <button type="submit" className="btn-primary">Guardar</button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
