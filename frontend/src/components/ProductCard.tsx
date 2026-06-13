import { useState } from 'react'

import { cartApi } from '../api/services'

import { mediaUrl } from '../api/client'

import { useAuth } from '../context/AuthContext'

import { useModal } from '../context/ModalContext'

import type { Product } from '../types'



interface Props {

  product: Product

  badge?: string

}



export default function ProductCard({ product, badge }: Props) {

  const { user, refreshCart } = useAuth()

  const { showLoginPrompt, showSuccess, showError, showProduct } = useModal()

  const [loading, setLoading] = useState(false)



  const handleAdd = async () => {

    if (!user) {

      showLoginPrompt()

      return

    }

    setLoading(true)

    try {

      await cartApi.add(product.id, 1)

      await refreshCart()

      showSuccess(`${product.nombre} se agregó a tu carrito.`, '¡Agregado!')

    } catch (e: unknown) {

      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail

      showError(msg || 'Error al agregar al carrito')

    } finally {

      setLoading(false)

    }

  }



  const img = mediaUrl(product.imagen)



  return (

    <article className="card group hover:shadow-lg dark:hover:shadow-black/30 transition-shadow duration-300">

      <button

        type="button"

        onClick={() => showProduct(product)}

        className="relative aspect-[4/3] w-full bg-gradient-to-br from-orange-50 to-red-50 dark:from-gray-800 dark:to-gray-700 overflow-hidden text-left"

      >

        {img ? (

          <img src={img} alt={product.nombre} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />

        ) : (

          <div className="w-full h-full flex items-center justify-center text-5xl">🍔</div>

        )}

        {badge && (

          <span className="absolute top-3 left-3 bg-brand text-white text-xs font-bold px-2.5 py-1 rounded-full">

            {badge}

          </span>

        )}

        {product.category && (

          <span className="absolute top-3 right-3 bg-surface-elevated/95 dark:bg-gray-900/90 text-xs font-medium px-2 py-1 rounded-full text-gray-600 dark:text-gray-300">

            {product.category.nombre}

          </span>

        )}

      </button>

      <div className="p-4">

        <button

          type="button"

          onClick={() => showProduct(product)}

          className="font-bold text-gray-900 dark:text-white line-clamp-1 text-left hover:text-brand transition w-full"

        >

          {product.nombre}

        </button>

        {product.descripcion && (

          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">{product.descripcion}</p>

        )}

        <div className="flex items-center justify-between mt-4 gap-2">

          <span className="text-xl font-extrabold text-brand">

            ${Number(product.precio).toFixed(2)}

          </span>

          <button

            onClick={handleAdd}

            disabled={loading || product.stock <= 0}

            className="btn-primary text-sm !py-2 !px-4 shrink-0"

          >

            {product.stock <= 0 ? 'Agotado' : loading ? '...' : '+ Agregar'}

          </button>

        </div>

      </div>

    </article>

  )

}

