import ProductCard from './ProductCard'
import type { Product } from '../types'

interface Props {
  id?: string
  title: string
  subtitle?: string
  products: Product[]
  badge?: string
}

export default function MenuSection({ id, title, subtitle, products, badge }: Props) {
  if (products.length === 0) return null

  return (
    <section id={id} className="max-w-7xl mx-auto px-4 sm:px-6 mt-10">
      <div className="flex items-end justify-between mb-6 gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-gray-900 dark:text-white">{title}</h2>
          {subtitle && <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">{subtitle}</p>}
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {products.map((p) => (
          <ProductCard key={p.id} product={p} badge={badge} />
        ))}
      </div>
    </section>
  )
}
