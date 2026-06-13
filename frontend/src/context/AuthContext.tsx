import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'
import { authApi, cartApi } from '../api/services'
import type { Cart, User } from '../types'

interface AuthContextType {
  user: User | null
  loading: boolean
  isAdmin: boolean
  cartCount: number
  login: (email: string, password: string) => Promise<User>
  register: (data: {
    nombres: string
    apellidos: string
    email: string
    telefono?: string
    password: string
  }) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
  refreshCart: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [cartCount, setCartCount] = useState(0)

  const refreshCart = useCallback(async () => {
    if (!localStorage.getItem('access_token')) {
      setCartCount(0)
      return
    }
    try {
      const { data } = await cartApi.get()
      setCartCount(data.cantidad_items)
    } catch {
      setCartCount(0)
    }
  }, [])

  const refreshUser = useCallback(async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const { data } = await authApi.me()
      setUser(data)
      await refreshCart()
    } catch {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [refreshCart])

  useEffect(() => {
    refreshUser()
  }, [refreshUser])

  const login = async (email: string, password: string) => {
    const { data } = await authApi.login(email, password)
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    const { data: profile } = await authApi.me()
    setUser(profile)
    await refreshCart()
    return profile
  }

  const register = async (data: {
    nombres: string
    apellidos: string
    email: string
    telefono?: string
    password: string
  }) => {
    await authApi.register(data)
    await login(data.email, data.password)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    setCartCount(0)
  }

  const isAdmin = user?.roles.some((r) => r.nombre === 'Administrador') ?? false

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAdmin,
        cartCount,
        login,
        register,
        logout,
        refreshUser,
        refreshCart,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return ctx
}

export type { Cart }
