import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="md:col-span-2">
          <div className="flex items-center gap-2 mb-4">
            <span className="w-8 h-8 bg-brand rounded-lg flex items-center justify-center text-white font-bold">F</span>
            <span className="font-bold text-white text-lg">FastFood</span>
          </div>
          <p className="text-sm text-gray-400 max-w-md">
            Tu comida favorita, en minutos. Hamburguesas, combos, bebidas y más — pedí online y recibí en la puerta de tu casa.
          </p>
        </div>
        <div>
          <h4 className="font-semibold text-white mb-3">Enlaces</h4>
          <ul className="space-y-2 text-sm">
            <li><Link to="/" className="hover:text-brand">Menú</Link></li>
            <li><Link to="/register" className="hover:text-brand">Registrarse</Link></li>
            <li><Link to="/login" className="hover:text-brand">Iniciar sesión</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="font-semibold text-white mb-3">Contacto</h4>
          <ul className="space-y-2 text-sm text-gray-400">
            <li>📍 Ciudad, País</li>
            <li>📞 +57 300 000 0000</li>
            <li>✉️ soporte@fastfood.com</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-gray-800 py-4 text-center text-xs text-gray-500">
        © {new Date().getFullYear()} FastFood Platform. Todos los derechos reservados.
      </div>
    </footer>
  )
}
