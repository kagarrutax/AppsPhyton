import { FormEvent, useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { useModal } from '../../context/ModalContext'
import type { Category } from '../../types'

const emptyForm = { nombre: '', descripcion: '', estado: true }

export default function AdminCategoriesPage() {
  const { showConfirm, showError, showSuccess } = useModal()
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState<Category | null>(null)
  const [form, setForm] = useState(emptyForm)
  const [showForm, setShowForm] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await adminApi.categories.list()
      setCategories(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const openCreate = () => {
    setEditing(null)
    setForm(emptyForm)
    setShowForm(true)
  }

  const openEdit = (c: Category) => {
    setEditing(c)
    setForm({ nombre: c.nombre, descripcion: c.descripcion || '', estado: c.estado })
    setShowForm(true)
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    try {
      if (editing) {
        await adminApi.categories.update(editing.id, form)
        showSuccess('Categoría actualizada')
      } else {
        await adminApi.categories.create(form)
        showSuccess('Categoría creada')
      }
      setShowForm(false)
      load()
    } catch {
      showError('No se pudo guardar la categoría')
    }
  }

  const handleDelete = async (c: Category) => {
    const ok = await showConfirm(`¿Eliminar "${c.nombre}"?`, 'Eliminar categoría')
    if (!ok) return
    try {
      await adminApi.categories.remove(c.id)
      showSuccess('Categoría eliminada')
      load()
    } catch {
      showError('No se pudo eliminar. Puede tener productos asociados.')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold">Categorías</h1>
          <p className="text-gray-500 text-sm">Organiza el menú por secciones</p>
        </div>
        <button type="button" onClick={openCreate} className="btn-primary">+ Nueva categoría</button>
      </div>

      {loading ? (
        <p className="text-gray-500">Cargando...</p>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-800/50 text-left">
              <tr>
                <th className="p-4 font-semibold">Nombre</th>
                <th className="p-4 font-semibold">Descripción</th>
                <th className="p-4 font-semibold">Estado</th>
                <th className="p-4 font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((c) => (
                <tr key={c.id} className="border-t border-gray-100 dark:border-gray-700">
                  <td className="p-4 font-medium">{c.nombre}</td>
                  <td className="p-4 text-gray-500">{c.descripcion || '—'}</td>
                  <td className="p-4">
                    <span className={`text-xs px-2 py-1 rounded-full ${c.estado ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-600'}`}>
                      {c.estado ? 'Activa' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="p-4">
                    <div className="flex gap-3">
                      <button type="button" onClick={() => openEdit(c)} className="text-brand text-xs font-semibold">Editar</button>
                      <button type="button" onClick={() => handleDelete(c)} className="text-red-500 text-xs font-semibold">Eliminar</button>
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
          <form onSubmit={handleSubmit} className="card w-full max-w-md p-6 space-y-4">
            <h2 className="text-xl font-bold">{editing ? 'Editar categoría' : 'Nueva categoría'}</h2>
            <input className="input-field" placeholder="Nombre" required value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
            <textarea className="input-field" placeholder="Descripción" rows={2} value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.checked })} />
              Categoría activa
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
