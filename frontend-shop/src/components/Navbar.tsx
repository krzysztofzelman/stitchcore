import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useCart } from '../contexts/CartContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const { count } = useCart()

  return (
    <nav className="bg-white shadow-sm border-b border-secondary-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="text-2xl font-bold text-brand-600">
            StitchCore
          </Link>
          <div className="flex items-center gap-4">
            <Link to="/products" className="text-secondary-600 hover:text-brand-600 transition">
              Produkty
            </Link>
            <Link to="/cart" className="text-secondary-600 hover:text-brand-600 transition relative">
              Koszyk
              {count > 0 && (
                <span className="absolute -top-2 -right-3 bg-brand-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {count}
                </span>
              )}
            </Link>
            {user ? (
              <>
                <Link to="/account" className="text-secondary-600 hover:text-brand-600 transition">
                  Konto
                </Link>
                <button onClick={logout} className="text-secondary-500 hover:text-red-600 transition text-sm">
                  Wyloguj
                </button>
              </>
            ) : (
              <Link to="/login" className="text-brand-600 hover:text-brand-700 font-medium">
                Zaloguj
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
