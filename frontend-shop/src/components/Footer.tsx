import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-secondary-900 text-white mt-16">
      <div className="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 className="text-xl font-bold text-brand-400 mb-3">StitchCore</h3>
          <p className="text-secondary-300 text-sm">
            Nowoczesna odzież i obuwie dla każdego. Jakość, styl i wygoda.
          </p>
        </div>
        <div>
          <h4 className="font-semibold mb-3">Sklep</h4>
          <ul className="space-y-2 text-sm text-secondary-300">
            <li><Link to="/products" className="hover:text-white transition">Produkty</Link></li>
            <li><Link to="/cart" className="hover:text-white transition">Koszyk</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="font-semibold mb-3">Konto</h4>
          <ul className="space-y-2 text-sm text-secondary-300">
            <li><Link to="/account" className="hover:text-white transition">Moje konto</Link></li>
            <li><Link to="/login" className="hover:text-white transition">Zaloguj</Link></li>
          </ul>
        </div>
      </div>
      <div className="border-t border-secondary-700 py-4 text-center text-secondary-400 text-sm">
        &copy; {new Date().getFullYear()} StitchCore. Wszelkie prawa zastrzeżone.
      </div>
    </footer>
  )
}
