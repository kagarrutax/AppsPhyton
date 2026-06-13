import { useEffect, useState } from 'react'
import { adminApi } from '../../api/services'
import type { User } from '../../types'

interface Props {
  value: string
  onChange: (userId: string) => void
  className?: string
}

export default function UserFilter({ value, onChange, className = 'input-field max-w-xs' }: Props) {
  const [users, setUsers] = useState<User[]>([])

  useEffect(() => {
    adminApi.users.list().then(({ data }) => setUsers(data)).catch(() => setUsers([]))
  }, [])

  return (
    <select className={className} value={value} onChange={(e) => onChange(e.target.value)}>
      <option value="">Todos los usuarios</option>
      {users.map((u) => (
        <option key={u.id} value={u.id}>
          {u.nombres} {u.apellidos} ({u.email})
        </option>
      ))}
    </select>
  )
}
