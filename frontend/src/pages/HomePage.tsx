import Layout from '../components/Layout'
import HeroBanner from '../components/HeroBanner'
import MenuTabBar from '../components/MenuTabBar'
import MenuPanel from '../components/MenuPanel'
import MenuSection from '../components/MenuSection'
import { catalogApi } from '../api/services'
import { useMenuNav } from '../context/MenuNavContext'
import { useEffect, useMemo, useState } from 'react'
import type { Product } from '../types'

const BEST_SELLER_NAMES = [
  'Hamburguesa Clásica',
  'Combo Familiar',
  'Papas Fritas',
  'Malteada de Vainilla',
  'Alitas BBQ x6',
  'Combo Ejecutivo',
]

export default function HomePage() {
  const { tab, setTab, registerMenuContent } = useMenuNav()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  useEffect(() => {
    catalogApi
      .publicProducts({ limit: 100 })
      .then(({ data }) => setProducts(Array.isArray(data) ? data : []))
      .catch(() => setError('No se pudo cargar el menú. Verificá que el backend esté activo.'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    setSearch('')
  }, [tab])

  const categories = useMemo(() => {
    const map = new Map<number, string>()
    products.forEach((p) => {
      if (p.category) map.set(p.category.id, p.category.nombre)
    })
    return Array.from(map.entries()).map(([id, nombre]) => ({ id, nombre }))
  }, [products])

  const bestSellers = useMemo(
    () => products.filter((p) => BEST_SELLER_NAMES.includes(p.nombre)),
    [products]
  )

  const combos = useMemo(
    () => products.filter((p) => p.category?.nombre === 'Combos'),
    [products]
  )

  const byCategory = useMemo(() => {
    const groups: Record<string, Product[]> = {}
    products.forEach((p) => {
      const name = p.category?.nombre ?? 'Otros'
      if (!groups[name]) groups[name] = []
      groups[name].push(p)
    })
    return groups
  }, [products])

  const categoryIdFromTab = tab.startsWith('cat-') ? Number(tab.slice(4)) : null

  const searchResults = useMemo(() => {
    if (!search.trim()) return []
    const q = search.toLowerCase()
    return products.filter(
      (p) =>
        p.nombre.toLowerCase().includes(q) ||
        (p.descripcion?.toLowerCase().includes(q) ?? false)
    )
  }, [products, search])

  const categoryProducts = useMemo(() => {
    if (!categoryIdFromTab || Number.isNaN(categoryIdFromTab)) return []
    return products.filter((p) => p.category_id === categoryIdFromTab)
  }, [products, categoryIdFromTab])

  const activeCategoryName = categoryIdFromTab
    ? categories.find((c) => c.id === categoryIdFromTab)?.nombre
    : null

  const handleTabSelect = (next: typeof tab) => {
    setTab(next, { scroll: true })
  }

  const renderContent = () => {
    if (loading) {
      return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="card h-72 animate-pulse bg-gray-200" />
          ))}
        </div>
      )
    }

    if (error) {
      return <div className="card p-10 text-center text-red-600">{error}</div>
    }

    if (search.trim()) {
      return (
        <MenuPanel
          title={`Resultados: "${search}"`}
          products={searchResults}
          emptyMessage="No encontramos productos con ese nombre."
        />
      )
    }

    if (tab === 'destacados') {
      return (
        <MenuPanel
          title="Destacados"
          subtitle="Los favoritos de nuestros clientes"
          products={bestSellers}
          badge="Top"
          emptyMessage="Aún no hay productos destacados."
        />
      )
    }

    if (tab === 'combos') {
      return (
        <MenuPanel
          title="Combos"
          subtitle="Paquetes listos para compartir"
          products={combos}
          badge="Combo"
          emptyMessage="No hay combos disponibles por ahora."
        />
      )
    }

    if (categoryIdFromTab && !Number.isNaN(categoryIdFromTab)) {
      return (
        <MenuPanel
          title={activeCategoryName ?? 'Categoría'}
          products={categoryProducts}
          emptyMessage="Esta categoría no tiene productos."
        />
      )
    }

    if (products.length === 0) {
      return (
        <div className="card p-10 text-center text-gray-500">
          Menú no disponible. Verificá que el backend esté activo.
        </div>
      )
    }

    return (
      <>
        {Object.entries(byCategory).map(([catName, items]) => (
          <MenuSection key={catName} title={catName} products={items} />
        ))}
      </>
    )
  }

  return (
    <Layout>
      <HeroBanner onVerMenu={() => setTab('todo', { scroll: true })} />

      <section className="max-w-7xl mx-auto px-4 sm:px-6 mt-8">
        <div className="relative">
          <input
            type="search"
            placeholder="Buscar hamburguesas, combos, bebidas..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field pl-12 py-4 text-lg shadow-sm"
          />
          <svg className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </section>

      {!search.trim() && (loading || categories.length > 0) && (
        <MenuTabBar tab={tab} categories={categories} onSelect={handleTabSelect} />
      )}

      <div
        id="menu-content"
        ref={registerMenuContent}
        className="scroll-mt-40 max-w-7xl mx-auto px-4 sm:px-6 mt-2"
      >
        {renderContent()}
      </div>
    </Layout>
  )
}
