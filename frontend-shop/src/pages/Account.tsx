import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ordersApi } from '../api/client'
import { useAuth } from '../contexts/AuthContext'

interface Order {
  id: number
  order_number: string
  status: string
  total: number
  created_at: string
  tracking_number: string
}

export default function Account() {
  const { user, logout } = useAuth()
  const [orders, setOrders] = useState<Order[]>([])

  useEffect(() => {
    if (user) {
      ordersApi.list().then(({ data }) => setOrders(data.results || []))
    }
  }, [user])

  if (!user) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold mb-4">Zaloguj się</h1>
        <Link to="/login" className="text-brand-600 hover:underline">Zaloguj</Link>
      </div>
    )
  }

  const statusColors: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    confirmed: 'bg-blue-100 text-blue-800',
    processing: 'bg-purple-100 text-purple-800',
    shipped: 'bg-cyan-100 text-cyan-800',
    delivered: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-secondary-800">Moje konto</h1>
          <p className="text-secondary-500">{user.email}</p>
        </div>
        <button onClick={logout} className="text-sm text-red-600 hover:underline">Wyloguj</button>
      </div>
      <h2 className="text-xl font-semibold mb-4">Zamówienia</h2>
      {orders.length === 0 ? (
        <p className="text-secondary-500">Brak zamówień</p>
      ) : (
        <div className="space-y-3">
          {orders.map((o) => (
            <div key={o.id} className="bg-white border border-secondary-200 rounded-lg p-4 flex items-center justify-between">
              <div>
                <p className="font-semibold text-secondary-800">{o.order_number}</p>
                <p className="text-sm text-secondary-500">{new Date(o.created_at).toLocaleDateString('pl-PL')}</p>
                {o.tracking_number && <p className="text-sm text-secondary-500">Nr przesyłki: {o.tracking_number}</p>}
              </div>
              <div className="text-right">
                <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${statusColors[o.status] || 'bg-secondary-100 text-secondary-800'}`}>
                  {o.status}
                </span>
                <p className="font-bold text-brand-700 mt-1">{Number(o.total).toFixed(2)} zł</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
