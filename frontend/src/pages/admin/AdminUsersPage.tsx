import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import { useModal } from '../../context/ModalContext'
import type { User } from '../../types'

export default function AdminUsersPage() {
  const { showError, showSuccess } = useModal()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await adminApi.users.list({ search: search || undefined })
      setUsers(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [search])

  const toggleStatus = async (u: User) => {
    try {
      await adminApi.users.update(u.id, { estado: !u.estado })
      showSuccess(`Usuario ${u.estado ? 'desactivado' : 'activado'}`)
      load()
    } catch {
      showError('No se pudo actualizar el usuario')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold">Usuarios</h1>
        <p className="text-gray-500 text-sm">Administra cuentas registradas</p>
      </div>

      <input
        type="search"
        placeholder="Buscar por nombre o email..."
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
                <th className="p-4 font-semibold">Usuario</th>
                <th className="p-4 font-semibold">Email</th>
                <th className="p-4 font-semibold">Roles</th>
                <th className="p-4 font-semibold">Estado</th>
                <th className="p-4 font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-t border-gray-100 dark:border-gray-700">
                  <td className="p-4 font-medium">{u.nombres} {u.apellidos}</td>
                  <td className="p-4 text-gray-500">{u.email}</td>
                  <td className="p-4">
                    <div className="flex flex-wrap gap-1">
                      {u.roles.map((r) => (
                        <span key={r.id} className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">
                          {r.nombre}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="p-4">
                    <span className={`text-xs px-2 py-1 rounded-full ${u.estado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {u.estado ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="p-4">
                    <button type="button" onClick={() => toggleStatus(u)} className="text-xs font-semibold text-brand">
                      {u.estado ? 'Desactivar' : 'Activar'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
