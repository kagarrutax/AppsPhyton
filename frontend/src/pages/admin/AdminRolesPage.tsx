import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import type { Permission, Role } from '../../types'

export default function AdminRolesPage() {
  const [roles, setRoles] = useState<Role[]>([])
  const [permissions, setPermissions] = useState<Permission[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedRole, setSelectedRole] = useState<number | null>(null)

  useEffect(() => {
    Promise.all([adminApi.roles.list(), adminApi.permissions.list()])
      .then(([rolesRes, permsRes]) => {
        setRoles(rolesRes.data)
        setPermissions(permsRes.data)
        if (rolesRes.data.length > 0) setSelectedRole(rolesRes.data[0].id)
      })
      .finally(() => setLoading(false))
  }, [])

  const activeRole = roles.find((r) => r.id === selectedRole)

  const groupedPermissions = permissions.reduce<Record<string, Permission[]>>((acc, p) => {
    if (!acc[p.modulo]) acc[p.modulo] = []
    acc[p.modulo].push(p)
    return acc
  }, {})

  if (loading) return <p className="text-gray-500">Cargando...</p>

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold">Roles y permisos</h1>
        <p className="text-gray-500 text-sm">Vista de solo lectura del sistema RBAC</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <section className="card p-5 space-y-2">
          <h2 className="font-bold mb-3">Roles</h2>
          {roles.map((role) => (
            <button
              key={role.id}
              type="button"
              onClick={() => setSelectedRole(role.id)}
              className={`w-full text-left p-3 rounded-xl transition ${
                selectedRole === role.id
                  ? 'bg-brand text-white'
                  : 'hover:bg-surface-muted dark:hover:bg-gray-700'
              }`}
            >
              <p className="font-semibold">{role.nombre}</p>
              {role.descripcion && (
                <p className={`text-xs mt-0.5 ${selectedRole === role.id ? 'text-white/80' : 'text-gray-500'}`}>
                  {role.descripcion}
                </p>
              )}
              <p className={`text-xs mt-1 ${selectedRole === role.id ? 'text-white/70' : 'text-gray-400'}`}>
                {role.permissions.length} permisos
              </p>
            </button>
          ))}
        </section>

        <section className="card p-5 lg:col-span-2">
          <h2 className="font-bold mb-4">
            Permisos de {activeRole?.nombre ?? '—'}
          </h2>
          {activeRole ? (
            activeRole.permissions.length === 0 ? (
              <p className="text-gray-500 text-sm">Sin permisos asignados.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {activeRole.permissions.map((p) => (
                  <span key={p.id} className="text-xs bg-surface-muted dark:bg-gray-700 px-2.5 py-1 rounded-full">
                    {p.nombre}
                  </span>
                ))}
              </div>
            )
          ) : null}

          <h3 className="font-bold mt-8 mb-3">Todos los permisos del sistema</h3>
          <div className="space-y-4">
            {Object.entries(groupedPermissions).map(([modulo, perms]) => (
              <div key={modulo}>
                <p className="text-xs uppercase tracking-wider text-gray-500 mb-2">{modulo}</p>
                <ul className="text-sm space-y-1">
                  {perms.map((p) => (
                    <li key={p.id} className="flex justify-between gap-2 py-1 border-b border-gray-100 dark:border-gray-800 last:border-0">
                      <span className="font-medium">{p.nombre}</span>
                      <span className="text-gray-500 text-xs truncate">{p.descripcion || '—'}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
