import { useEffect, useState } from 'react'

import { useNavigate, useParams } from 'react-router-dom'

import Layout from '../components/Layout'

import { orderApi, paymentApi } from '../api/services'

import { useAuth } from '../context/AuthContext'

import { useModal } from '../context/ModalContext'

import type { Order } from '../types'



export default function OrderDetailPage() {

  const { id } = useParams<{ id: string }>()

  const { user } = useAuth()

  const { showSuccess, showError } = useModal()

  const navigate = useNavigate()

  const [order, setOrder] = useState<Order | null>(null)

  const [file, setFile] = useState<File | null>(null)

  const [uploading, setUploading] = useState(false)



  useEffect(() => {

    if (!user) {

      navigate('/login')

      return

    }

    orderApi.get(Number(id)).then(({ data }) => setOrder(data)).catch(() => navigate('/orders'))

  }, [user, id, navigate])



  const handleUpload = async () => {

    if (!file || !order) return

    setUploading(true)

    try {

      await paymentApi.submit(order.id, file)

      setFile(null)

      showSuccess('Comprobante enviado. El administrador lo revisará pronto.', 'Comprobante recibido')

    } catch (e: unknown) {

      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail

      showError(msg || 'Error al subir comprobante')

    } finally {

      setUploading(false)

    }

  }



  if (!order) {

    return (

      <Layout>

        <div className="max-w-3xl mx-auto px-4 py-12 text-center text-gray-500 dark:text-gray-400">Cargando pedido...</div>

      </Layout>

    )

  }



  return (

    <Layout>

      <div className="max-w-3xl mx-auto px-4 py-8">

        <button onClick={() => navigate('/orders')} className="text-brand text-sm font-medium mb-4 hover:underline">

          ← Volver a pedidos

        </button>



        <div className="card p-6 mb-6">

          <div className="flex justify-between items-start mb-4">

            <div>

              <h1 className="text-2xl font-extrabold dark:text-white">Pedido #{order.id}</h1>

              <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">

                {new Date(order.fecha_creacion).toLocaleString('es')}

              </p>

            </div>

            <span className="bg-yellow-100 dark:bg-yellow-900/40 text-yellow-800 dark:text-yellow-200 text-sm font-semibold px-3 py-1 rounded-full capitalize">

              {order.estado}

            </span>

          </div>



          <div className="divide-y dark:divide-gray-700">

            {order.items.map((item) => (

              <div key={item.id} className="py-3 flex justify-between">

                <div>

                  <p className="font-medium dark:text-white">{item.product_nombre}</p>

                  <p className="text-sm text-gray-500 dark:text-gray-400">x{item.cantidad}</p>

                </div>

                <p className="font-semibold dark:text-white">${Number(item.subtotal).toFixed(2)}</p>

              </div>

            ))}

          </div>



          <div className="flex justify-between text-xl font-bold mt-4 pt-4 border-t dark:border-gray-700 dark:text-white">

            <span>Total</span>

            <span className="text-brand">${Number(order.total).toFixed(2)}</span>

          </div>

        </div>



        {order.estado === 'pendiente' && (

          <div className="card p-6">

            <h2 className="font-bold text-lg mb-2 dark:text-white">💳 Pago por transferencia</h2>

            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">

              Realiza la transferencia bancaria por <strong>${Number(order.total).toFixed(2)}</strong> y sube tu comprobante (JPG, PNG o PDF).

            </p>

            <div className="bg-surface-muted dark:bg-gray-800 rounded-xl p-4 text-sm text-gray-600 dark:text-gray-300 mb-4">

              <p><strong>Banco:</strong> Banco Demo</p>

              <p><strong>Cuenta:</strong> 1234-5678-9012</p>

              <p><strong>Titular:</strong> FastFood Platform S.A.S.</p>

            </div>

            <input

              type="file"

              accept=".jpg,.jpeg,.png,.pdf"

              onChange={(e) => setFile(e.target.files?.[0] || null)}

              className="block w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-brand file:text-white file:font-semibold hover:file:bg-brand-dark mb-4"

            />

            <button onClick={handleUpload} disabled={!file || uploading} className="btn-primary w-full">

              {uploading ? 'Enviando...' : 'Enviar comprobante'}

            </button>

          </div>

        )}

      </div>

    </Layout>

  )

}

