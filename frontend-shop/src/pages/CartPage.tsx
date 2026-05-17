import { Link } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'

export default function CartPage() {
  const { items, removeItem, updateQuantity, total } = useCart()

  if (items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold text-secondary-800 mb-4">Koszyk jest pusty</h1>
        <Link to="/products" className="text-brand-600 hover:underline">Przejdź do produktów</Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-secondary-800 mb-6">Koszyk</h1>
      <div className="space-y-4">
        {items.map((item, idx) => (
          <div key={`${item.product_id}-${item.variant_id}`} className="flex items-center justify-between bg-white p-4 rounded-lg border border-secondary-200">
            <div>
              <h3 className="font-semibold text-secondary-800">{item.product_name}</h3>
              {item.variant_label && <p className="text-sm text-secondary-500">{item.variant_label}</p>}
              <p className="text-brand-700 font-medium">{item.unit_price.toFixed(2)} zł</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center border border-secondary-300 rounded">
                <button onClick={() => updateQuantity(item.product_id, Math.max(1, item.quantity - 1), item.variant_id)} className="px-2 py-1 hover:bg-secondary-100">-</button>
                <span className="px-3 py-1">{item.quantity}</span>
                <button onClick={() => updateQuantity(item.product_id, item.quantity + 1, item.variant_id)} className="px-2 py-1 hover:bg-secondary-100">+</button>
              </div>
              <button onClick={() => removeItem(item.product_id, item.variant_id)} className="text-red-500 hover:text-red-700 text-sm">Usuń</button>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 text-right">
        <p className="text-xl font-bold text-secondary-800">Razem: {total.toFixed(2)} zł</p>
        <Link to="/checkout" className="mt-4 inline-block bg-brand-600 text-white font-semibold px-8 py-3 rounded-lg hover:bg-brand-700 transition">
          Przejdź do zamówienia
        </Link>
      </div>
    </div>
  )
}
