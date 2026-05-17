import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { productsApi } from '../api/client'
import { useCart } from '../contexts/CartContext'

interface Variant {
  id: number
  sku: string
  size: string
  color: string
  price_adjustment: number
  is_active: boolean
}

interface Product {
  id: number
  name: string
  description: string
  price: number
  compare_price: number | null
  brand: string
  variants: Variant[]
}

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedVariant, setSelectedVariant] = useState<Variant | null>(null)
  const [qty, setQty] = useState(1)
  const { addItem } = useCart()

  useEffect(() => {
    if (!id) return
    productsApi.get(Number(id)).then(({ data }) => {
      setProduct(data)
      if (data.variants?.length > 0) setSelectedVariant(data.variants[0])
    }).finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="text-center py-16 text-secondary-400">Ładowanie...</div>
  if (!product) return <div className="text-center py-16 text-secondary-500">Produkt nie znaleziony</div>

  const price = product.price + (selectedVariant?.price_adjustment || 0)
  const finalPrice = Math.max(0, price)

  const handleAdd = () => {
    addItem({
      product_id: product.id,
      variant_id: selectedVariant?.id,
      product_name: product.name,
      variant_label: selectedVariant ? `${selectedVariant.size} / ${selectedVariant.color}` : '',
      quantity: qty,
      unit_price: finalPrice,
    })
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <Link to="/products" className="text-sm text-brand-600 hover:underline mb-4 inline-block">&larr; Powrót</Link>
      <div className="grid md:grid-cols-2 gap-8">
        <div className="h-80 bg-gradient-to-br from-brand-100 to-brand-200 rounded-lg flex items-center justify-center">
          <span className="text-6xl">🧵</span>
        </div>
        <div>
          <h1 className="text-3xl font-bold text-secondary-800 mb-2">{product.name}</h1>
          <p className="text-secondary-500 mb-4">{product.brand}</p>
          <p className="text-secondary-600 mb-6">{product.description}</p>
          <div className="text-3xl font-bold text-brand-700 mb-4">{finalPrice.toFixed(2)} zł</div>
          {product.variants.length > 0 && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-secondary-700 mb-2">Wariant:</label>
              <select
                value={selectedVariant?.id || ''}
                onChange={(e) => setSelectedVariant(product.variants.find((v) => v.id === Number(e.target.value)) || null)}
                className="border border-secondary-300 rounded-lg px-3 py-2 w-full max-w-xs"
              >
                {product.variants.filter((v) => v.is_active).map((v) => (
                  <option key={v.id} value={v.id}>{v.size} / {v.color} (SKU: {v.sku})</option>
                ))}
              </select>
            </div>
          )}
          <div className="flex items-center gap-4 mb-6">
            <div className="flex items-center border border-secondary-300 rounded-lg">
              <button onClick={() => setQty(Math.max(1, qty - 1))} className="px-3 py-2 hover:bg-secondary-100">-</button>
              <span className="px-4 py-2">{qty}</span>
              <button onClick={() => setQty(qty + 1)} className="px-3 py-2 hover:bg-secondary-100">+</button>
            </div>
            <button onClick={handleAdd} className="bg-brand-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-brand-700 transition">
              Dodaj do koszyka
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
