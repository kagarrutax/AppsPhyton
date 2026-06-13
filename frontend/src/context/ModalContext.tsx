import {
  createContext,
  useCallback,
  useContext,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { Link } from 'react-router-dom'
import Modal from '../components/ui/Modal'
import { cartApi } from '../api/services'
import { mediaUrl } from '../api/client'
import { useAuth } from './AuthContext'
import type { Product } from '../types'

export type ModalKind = 'alert' | 'confirm' | 'success' | 'error' | 'info' | 'login' | 'product'

interface ModalState {
  open: boolean
  kind: ModalKind
  title: string
  message?: string
  product?: Product
  confirmText?: string
  cancelText?: string
}

interface ModalContextValue {
  showAlert: (message: string, title?: string) => void
  showSuccess: (message: string, title?: string) => void
  showError: (message: string, title?: string) => void
  showInfo: (message: string, title?: string) => void
  showConfirm: (message: string, title?: string) => Promise<boolean>
  showLoginPrompt: () => void
  showProduct: (product: Product) => void
  closeModal: () => void
}

const ModalContext = createContext<ModalContextValue | null>(null)

const KIND_ICON: Record<ModalKind, string> = {
  alert: 'ℹ️',
  confirm: '❓',
  success: '✅',
  error: '❌',
  info: '💡',
  login: '🔐',
  product: '🍔',
}

const initialState: ModalState = {
  open: false,
  kind: 'info',
  title: '',
}

export function ModalProvider({ children }: { children: ReactNode }) {
  const [modal, setModal] = useState<ModalState>(initialState)
  const confirmResolve = useRef<((value: boolean) => void) | null>(null)
  const { user, refreshCart } = useAuth()
  const [addingToCart, setAddingToCart] = useState(false)

  const closeModal = useCallback(() => {
    setModal((m) => ({ ...m, open: false }))
    confirmResolve.current?.(false)
    confirmResolve.current = null
  }, [])

  const open = useCallback((state: Omit<ModalState, 'open'>) => {
    setModal({ ...state, open: true })
  }, [])

  const showAlert = useCallback(
    (message: string, title = 'Aviso') => open({ kind: 'alert', title, message }),
    [open]
  )

  const showSuccess = useCallback(
    (message: string, title = '¡Listo!') => open({ kind: 'success', title, message }),
    [open]
  )

  const showError = useCallback(
    (message: string, title = 'Error') => open({ kind: 'error', title, message }),
    [open]
  )

  const showInfo = useCallback(
    (message: string, title = 'Información') => open({ kind: 'info', title, message }),
    [open]
  )

  const showConfirm = useCallback(
    (message: string, title = 'Confirmar') =>
      new Promise<boolean>((resolve) => {
        confirmResolve.current = resolve
        open({ kind: 'confirm', title, message, confirmText: 'Confirmar', cancelText: 'Cancelar' })
      }),
    [open]
  )

  const showLoginPrompt = useCallback(
    () =>
      open({
        kind: 'login',
        title: 'Iniciá sesión',
        message: 'Necesitás una cuenta para agregar productos al carrito.',
      }),
    [open]
  )

  const showProduct = useCallback(
    (product: Product) => open({ kind: 'product', title: product.nombre, product }),
    [open]
  )

  const handleConfirm = () => {
    confirmResolve.current?.(true)
    confirmResolve.current = null
    setModal((m) => ({ ...m, open: false }))
  }

  const handleAddToCart = async () => {
    if (!modal.product) return
    if (!user) {
      closeModal()
      showLoginPrompt()
      return
    }
    if (modal.product.stock <= 0) {
      showError('Producto agotado')
      return
    }
    setAddingToCart(true)
    try {
      await cartApi.add(modal.product.id, 1)
      await refreshCart()
      closeModal()
      showSuccess(`${modal.product.nombre} se agregó a tu carrito.`, '¡Agregado!')
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      showError(msg || 'Error al agregar al carrito')
    } finally {
      setAddingToCart(false)
    }
  }

  const icon = KIND_ICON[modal.kind]
  const img = modal.product ? mediaUrl(modal.product.imagen) : undefined
  const showStandardModal = modal.open && modal.kind !== 'product'
  const showProductModal = modal.open && modal.kind === 'product' && !!modal.product

  return (
    <ModalContext.Provider
      value={{
        showAlert,
        showSuccess,
        showError,
        showInfo,
        showConfirm,
        showLoginPrompt,
        showProduct,
        closeModal,
      }}
    >
      {children}

      {showStandardModal && (
        <Modal
          open
          onClose={closeModal}
          title={`${icon} ${modal.title}`}
          size={modal.kind === 'login' ? 'md' : 'sm'}
          closeOnBackdrop={modal.kind !== 'confirm'}
          footer={
            modal.kind === 'confirm' ? (
              <>
                <button type="button" onClick={closeModal} className="btn-outline text-sm !py-2 !px-4">
                  {modal.cancelText ?? 'Cancelar'}
                </button>
                <button type="button" onClick={handleConfirm} className="btn-primary text-sm !py-2 !px-4">
                  {modal.confirmText ?? 'Confirmar'}
                </button>
              </>
            ) : modal.kind === 'login' ? (
              <>
                <button type="button" onClick={closeModal} className="btn-outline text-sm !py-2 !px-4">
                  Ahora no
                </button>
                <Link to="/register" onClick={closeModal} className="btn-outline text-sm !py-2 !px-4 inline-block">
                  Registrarse
                </Link>
                <Link to="/login" onClick={closeModal} className="btn-primary text-sm !py-2 !px-4 inline-block">
                  Ingresar
                </Link>
              </>
            ) : (
              <button type="button" onClick={closeModal} className="btn-primary text-sm !py-2 !px-6 ml-auto">
                Entendido
              </button>
            )
          }
        >
          {modal.message && (
            <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">{modal.message}</p>
          )}
        </Modal>
      )}

      {showProductModal && modal.product && (
        <Modal
          open
          onClose={closeModal}
          title={modal.product.nombre}
          size="lg"
          footer={
            <div className="flex gap-3 ml-auto">
              <button type="button" onClick={closeModal} className="btn-outline text-sm !py-2 !px-4">
                Cerrar
              </button>
              <button
                type="button"
                onClick={handleAddToCart}
                disabled={addingToCart || modal.product.stock <= 0}
                className="btn-primary text-sm !py-2 !px-4"
              >
                {modal.product.stock <= 0 ? 'Agotado' : addingToCart ? 'Agregando...' : '+ Agregar al carrito'}
              </button>
            </div>
          }
        >
          <div className="space-y-4">
            <div className="aspect-video rounded-xl overflow-hidden bg-gradient-to-br from-orange-50 to-red-50 dark:from-gray-800 dark:to-gray-700">
              {img ? (
                <img src={img} alt={modal.product.nombre} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-6xl">🍔</div>
              )}
            </div>
            {modal.product.descripcion && (
              <p className="text-gray-600 dark:text-gray-300 text-sm">{modal.product.descripcion}</p>
            )}
            <div className="flex items-center justify-between">
              <span className="text-2xl font-extrabold text-brand">
                ${Number(modal.product.precio).toFixed(2)}
              </span>
              {modal.product.category && (
                <span className="text-xs font-medium px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                  {modal.product.category.nombre}
                </span>
              )}
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Stock disponible: {modal.product.stock} unidades
            </p>
          </div>
        </Modal>
      )}
    </ModalContext.Provider>
  )
}

export function useModal() {
  const ctx = useContext(ModalContext)
  if (!ctx) throw new Error('useModal debe usarse dentro de ModalProvider')
  return ctx
}
