import { CATEGORY_META } from '../constants/menuCategories'
import type { MenuTab } from '../context/MenuNavContext'

interface CategoryItem {
  id: number
  nombre: string
}

interface Props {
  tab: MenuTab
  categories: CategoryItem[]
  onSelect: (tab: MenuTab) => void
}

const MAIN_TABS: { key: MenuTab; label: string; emoji: string }[] = [
  { key: 'todo', label: 'Todo el menú', emoji: '🍽️' },
  { key: 'destacados', label: 'Destacados', emoji: '🔥' },
  { key: 'combos', label: 'Combos', emoji: '🎉' },
]

export default function MenuTabBar({ tab, categories, onSelect }: Props) {
  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 mt-6">
      <div className="sticky top-16 z-40 -mx-4 px-4 sm:-mx-6 sm:px-6 py-3 bg-surface-page/95 dark:bg-gray-900/95 backdrop-blur border-y border-gray-200/80 dark:border-gray-800">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-400 dark:text-gray-500 mb-2">Secciones</p>
        <div className="flex flex-wrap gap-2">
          {MAIN_TABS.map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => onSelect(t.key)}
              className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition ${
                tab === t.key
                  ? 'bg-brand text-white shadow-sm'
                  : 'bg-surface-card dark:bg-gray-800 text-gray-700 dark:text-gray-200 border border-gray-300/70 dark:border-gray-600 hover:border-brand hover:text-brand'
              }`}
            >
              <span>{t.emoji}</span>
              {t.label}
            </button>
          ))}
          {categories.map((c) => {
            const catTab = `cat-${c.id}` as MenuTab
            const meta = CATEGORY_META[c.nombre]
            return (
              <button
                key={c.id}
                type="button"
                onClick={() => onSelect(catTab)}
                className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition ${
                  tab === catTab
                    ? 'bg-brand text-white shadow-sm'
                    : 'bg-surface-card dark:bg-gray-800 text-gray-700 dark:text-gray-200 border border-gray-300/70 dark:border-gray-600 hover:border-brand hover:text-brand'
                }`}
              >
                {meta && <span>{meta.emoji}</span>}
                {c.nombre}
              </button>
            )
          })}
        </div>
      </div>
    </section>
  )
}
