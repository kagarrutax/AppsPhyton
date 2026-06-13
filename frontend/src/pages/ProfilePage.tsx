import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import { authApi } from '../api/services'
import { useAuth } from '../context/AuthContext'

export default function ProfilePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [passwords, setPasswords] = useState({ current: '', new: '' })
  const [msg, setMsg] = useState('')
  const [error, setError] = useState('')

  if (!user) {
    navigate('/login')
    return null
  }

  const handlePassword = async (e: FormEvent) => {
    e.preventDefault()
    setMsg('')
    setError('')
    try {
      await authApi.changePassword(passwords.current, passwords.new)
      setMsg('Contraseña actualizada correctamente')
      setPasswords({ current: '', new: '' })
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : 'Error al cambiar contraseña')
    }
  }

  return (
    <Layout>
      <div className="max-w-lg mx-auto px-4 py-8">
        <h1 className="text-2xl font-extrabold mb-6">Mi perfil</h1>

        <div className="card p-6 mb-6">
          <div className="w-16 h-16 bg-brand rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
            {user.nombres[0]}
          </div>
          <h2 className="font-bold text-lg">{user.nombres} {user.apellidos}</h2>
          <p className="text-gray-500">{user.email}</p>
          {user.telefono && <p className="text-gray-500 text-sm mt-1">{user.telefono}</p>}
          <p className="text-xs text-gray-400 mt-2 capitalize">
            Rol: {user.roles.map((r) => r.nombre).join(', ')}
          </p>
        </div>

        <div className="card p-6">
          <h3 className="font-bold mb-4">Cambiar contraseña</h3>
          {msg && <p className="text-green-600 text-sm mb-3">{msg}</p>}
          {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
          <form onSubmit={handlePassword} className="space-y-4">
            <input type="password" placeholder="Contraseña actual" required value={passwords.current} onChange={(e) => setPasswords({ ...passwords, current: e.target.value })} className="input-field" />
            <input type="password" placeholder="Nueva contraseña" required minLength={8} value={passwords.new} onChange={(e) => setPasswords({ ...passwords, new: e.target.value })} className="input-field" />
            <button type="submit" className="btn-primary w-full">Actualizar contraseña</button>
          </form>
        </div>

        <button onClick={() => { logout(); navigate('/') }} className="mt-6 w-full text-red-500 font-medium py-3 hover:bg-red-50 rounded-xl transition">
          Cerrar sesión
        </button>
      </div>
    </Layout>
  )
}
