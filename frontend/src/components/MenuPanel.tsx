import ProductCard from './ProductCard'
import type { Product } from '../types'

interface Props {
  title: string
  subtitle?: string
  products: Product[]
  badge?: string
  emptyMessage?: string
}

export default function MenuPanel({ title, subtitle, products, badge, emptyMessage }: Props) {
  return (
    <section className="mt-6 mb-10">
      <div className="mb-6">
        <h2 className="text-2xl font-extrabold text-gray-900 dark:text-white">{title}</h2>
        {subtitle && <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">{subtitle}</p>}
      </div>

      {products.length === 0 ? (
        <div className="card p-10 text-center text-gray-500">
          {emptyMessage ?? 'No hay productos en esta sección.'}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} badge={badge} />
          ))}
        </div>
      )}
    </section>
  )
}
