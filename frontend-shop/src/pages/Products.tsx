import { useEffect, useState } from 'react'
import { productsApi } from '../api/client'
import ProductCard from '../components/ProductCard'

interface ProductItem {
  id: number
  name: string
  slug: string
  price: number
  compare_price: number | null
  brand: string
  category_name: string | null
  has_variants: boolean
}

export default function Products() {
  const [products, setProducts] = useState<ProductItem[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    productsApi.list({ search: search || undefined, page_size: 50 })
      .then(({ data }) => setProducts(data.results || []))
      .finally(() => setLoading(false))
  }, [search])

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-secondary-800 mb-6">Produkty</h1>
      <input
        type="text"
        placeholder="Szukaj produktów..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full max-w-md border border-secondary-300 rounded-lg px-4 py-2 mb-8 focus:outline-none focus:ring-2 focus:ring-brand-500"
      />
      {loading ? (
        <div className="text-center py-12 text-secondary-400">Ładowanie...</div>
      ) : products.length === 0 ? (
        <div className="text-center py-12 text-secondary-500">Brak produktów</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((p) => (
            <ProductCard key={p.id} {...p} />
          ))}
        </div>
      )}
    </div>
  )
}
