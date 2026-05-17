import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { ordersApi } from '../api/client'
import { useCart } from '../contexts/CartContext'
import { useAuth } from '../contexts/AuthContext'

export default function Checkout() {
  const { items, clearCart, total } = useCart()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [address, setAddress] = useState('')
  const [notes, setNotes] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (!user) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold mb-4">Zaloguj się, aby złożyć zamówienie</h1>
        <Link to="/login" className="text-brand-600 hover:underline">Zaloguj</Link>
      </div>
    )
  }

  if (items.length === 0) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold mb-4">Koszyk jest pusty</h1>
        <Link to="/products" className="text-brand-600 hover:underline">Przejdź do produktów</Link>
      </div>
    )
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    try {
      const { data } = await ordersApi.create({
        items: items.map((i) => ({
          product_id: i.product_id,
          variant_id: i.variant_id,
          product_name: i.product_name,
          variant_label: i.variant_label,
          quantity: i.quantity,
          unit_price: i.unit_price,
        })),
        shipping_address: address || 'Odbiór osobisty',
        shipping_method: address ? 'courier' : 'pickup',
        notes,
      })
      clearCart()
      navigate(`/account`)
    } catch {
      alert('Błąd składania zamówienia')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-secondary-800 mb-6">Składanie zamówienia</h1>
      <div className="bg-white rounded-lg border border-secondary-200 p-4 mb-6">
        <h2 className="font-semibold mb-3">Podsumowanie koszyka</h2>
        {items.map((item) => (
          <div key={`${item.product_id}-${item.variant_id}`} className="flex justify-between text-sm py-1">
            <span>{item.product_name} {item.variant_label && `(${item.variant_label})`} x{item.quantity}</span>
            <span>{(item.unit_price * item.quantity).toFixed(2)} zł</span>
          </div>
        ))}
        <div className="border-t pt-2 mt-2 flex justify-between font-bold">
          <span>Razem</span>
          <span>{total.toFixed(2)} zł</span>
        </div>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-secondary-700 mb-1">Adres dostawy (opcjonalnie — pozostaw puste dla odbioru osobistego)</label>
          <textarea value={address} onChange={(e) => setAddress(e.target.value)} rows={3}
            className="w-full border border-secondary-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-secondary-700 mb-1">Uwagi</label>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={2}
            className="w-full border border-secondary-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500" />
        </div>
        <p className="text-sm text-secondary-500">Płatność przy odbiorze (pobranie)</p>
        <button type="submit" disabled={submitting}
          className="w-full bg-brand-600 text-white font-semibold py-3 rounded-lg hover:bg-brand-700 transition disabled:opacity-50">
          {submitting ? 'Składanie...' : 'Złóż zamówienie'}
        </button>
      </form>
    </div>
  )
}
