import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
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

export default function Home() {
  const [products, setProducts] = useState<ProductItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    productsApi.list({ page_size: 8 }).then(({ data }) => {
      setProducts(data.results || [])
    }).finally(() => setLoading(false))
  }, [])

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-brand-600 to-brand-800 text-white">
        <div className="max-w-7xl mx-auto px-4 py-20 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">StitchCore</h1>
          <p className="text-xl text-brand-100 mb-8 max-w-2xl mx-auto">
            Nowoczesna odzież i obuwie. Wyraź swój styl z naszą kolekcją.
          </p>
          <Link
            to="/products"
            className="inline-block bg-white text-brand-700 font-semibold px-8 py-3 rounded-lg hover:bg-brand-50 transition"
          >
            Przeglądaj produkty
          </Link>
        </div>
      </section>

      {/* Products */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-2xl font-bold text-secondary-800 mb-8">Najnowsze produkty</h2>
        {loading ? (
          <div className="text-center py-8 text-secondary-400">Ładowanie...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((p) => (
              <ProductCard key={p.id} {...p} />
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
