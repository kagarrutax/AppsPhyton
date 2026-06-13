import { useEffect, useState } from 'react'

import { Link, useNavigate } from 'react-router-dom'

import Layout from '../components/Layout'

import { cartApi, orderApi } from '../api/services'

import { mediaUrl } from '../api/client'

import { useAuth } from '../context/AuthContext'

import { useModal } from '../context/ModalContext'

import type { Cart } from '../types'



export default function CartPage() {

  const { user, refreshCart } = useAuth()

  const { showConfirm, showError, showSuccess } = useModal()

  const navigate = useNavigate()

  const [cart, setCart] = useState<Cart | null>(null)

  const [loading, setLoading] = useState(true)

  const [checkingOut, setCheckingOut] = useState(false)



  const load = () => {

    cartApi.get().then(({ data }) => setCart(data)).finally(() => setLoading(false))

  }



  useEffect(() => {

    if (!user) {

      navigate('/login')

      return

    }

    load()

  }, [user, navigate])



  const updateQty = async (productId: number, cantidad: number) => {

    const { data } = await cartApi.update(productId, cantidad)

    setCart(data)

    await refreshCart()

  }



  const remove = async (productId: number) => {

    const ok = await showConfirm('¿Querés quitar este producto del carrito?', 'Quitar producto')

    if (!ok) return

    const { data } = await cartApi.remove(productId)

    setCart(data)

    await refreshCart()

  }



  const checkout = async () => {

    if (!cart) return

    const ok = await showConfirm(

      `¿Confirmar pedido por $${Number(cart.total).toFixed(2)}?`,

      'Confirmar pedido'

    )

    if (!ok) return



    setCheckingOut(true)

    try {

      const { data } = await orderApi.checkout()

      await refreshCart()

      showSuccess('Tu pedido fue creado. Podés subir el comprobante de pago.', 'Pedido confirmado')

      navigate(`/orders/${data.id}`)

    } catch (e: unknown) {

      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail

      showError(msg || 'Error en checkout')

    } finally {

      setCheckingOut(false)

    }

  }



  if (loading) {

    return (

      <Layout>

        <div className="max-w-3xl mx-auto px-4 py-12 text-center text-gray-500 dark:text-gray-400">Cargando carrito...</div>

      </Layout>

    )

  }



  return (

    <Layout>

      <div className="max-w-3xl mx-auto px-4 py-8">

        <h1 className="text-2xl font-extrabold mb-6 dark:text-white">Tu carrito</h1>



        {!cart?.items.length ? (

          <div className="card p-12 text-center">

            <p className="text-5xl mb-4">🛒</p>

            <p className="text-gray-500 dark:text-gray-400 mb-6">Tu carrito está vacío</p>

            <Link to="/" className="btn-primary inline-block">Ver menú</Link>

          </div>

        ) : (

          <div className="space-y-4">

            {cart.items.map((item) => (

              <div key={item.id} className="card p-4 flex gap-4 items-center">

                <div className="w-16 h-16 rounded-xl bg-orange-50 dark:bg-gray-800 flex items-center justify-center shrink-0 overflow-hidden">

                  {item.product?.imagen ? (

                    <img src={mediaUrl(item.product.imagen)} alt="" className="w-full h-full object-cover" />

                  ) : (

                    <span className="text-2xl">🍔</span>

                  )}

                </div>

                <div className="flex-1 min-w-0">

                  <h3 className="font-bold truncate dark:text-white">{item.product?.nombre || `Producto #${item.product_id}`}</h3>

                  <p className="text-brand font-semibold">${Number(item.precio_unitario).toFixed(2)}</p>

                </div>

                <div className="flex items-center gap-2">

                  <button onClick={() => updateQty(item.product_id, Math.max(1, item.cantidad - 1))} className="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-700 font-bold dark:text-white">−</button>

                  <span className="w-8 text-center font-semibold dark:text-white">{item.cantidad}</span>

                  <button onClick={() => updateQty(item.product_id, item.cantidad + 1)} className="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-700 font-bold dark:text-white">+</button>

                </div>

                <button onClick={() => remove(item.product_id)} className="text-red-400 hover:text-red-600 text-sm">✕</button>

              </div>

            ))}



            <div className="card p-6">

              <div className="flex justify-between text-lg font-bold mb-4 dark:text-white">

                <span>Total</span>

                <span className="text-brand">${Number(cart.total).toFixed(2)}</span>

              </div>

              <button onClick={checkout} disabled={checkingOut} className="btn-primary w-full text-lg !py-3">

                {checkingOut ? 'Procesando...' : 'Confirmar pedido'}

              </button>

            </div>

          </div>

        )}

      </div>

    </Layout>

  )

}

