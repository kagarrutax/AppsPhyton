import { Link } from 'react-router-dom'

interface Props {
  onVerMenu?: () => void
}

export default function HeroBanner({ onVerMenu }: Props) {
  return (
    <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-brand via-brand-light to-orange-400 text-white mx-4 sm:mx-6 max-w-7xl lg:mx-auto mt-6">
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 right-20 text-[120px]">🍔</div>
        <div className="absolute bottom-0 left-10 text-[80px]">🍟</div>
      </div>
      <div className="relative px-8 py-12 sm:py-16 md:px-14 flex flex-col md:flex-row items-center gap-8">
        <div className="flex-1 text-center md:text-left">
          <span className="inline-block bg-white/20 backdrop-blur text-sm font-semibold px-4 py-1 rounded-full mb-4">
            🔥 Promoción del día
          </span>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold leading-tight">
            Comida rápida,<br />entregada en minutos
          </h1>
          <p className="mt-4 text-white/90 text-lg max-w-lg">
            Los mejores combos, hamburguesas artesanales y bebidas frescas. Pedí ahora y disfrutá.
          </p>
          <div className="mt-8 flex flex-wrap gap-3 justify-center md:justify-start">
            <button
              type="button"
              onClick={onVerMenu}
              className="bg-white text-brand font-bold px-8 py-3 rounded-full hover:bg-gray-100 transition shadow-lg"
            >
              Ver menú
            </button>
            <Link to="/register" className="border-2 border-white font-bold px-8 py-3 rounded-full hover:bg-white/10 transition">
              Crear cuenta
            </Link>
          </div>
        </div>
        <div className="hidden md:flex w-64 h-64 bg-white/10 rounded-full items-center justify-center text-[100px] backdrop-blur-sm border border-white/20">
          🛵
        </div>
      </div>
    </section>
  )
}
