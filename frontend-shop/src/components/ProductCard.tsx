import { Link } from 'react-router-dom'

interface ProductCardProps {
  id: number
  name: string
  price: number
  compare_price?: number | null
  brand: string
  category_name?: string | null
  has_variants: boolean
}

export default function ProductCard({ id, name, price, compare_price, brand, category_name, has_variants }: ProductCardProps) {
  const discount = compare_price ? Math.round((1 - price / compare_price) * 100) : 0

  return (
    <Link to={`/products/${id}`} className="group bg-white rounded-lg shadow-sm border border-secondary-200 overflow-hidden hover:shadow-md transition">
      <div className="h-48 bg-gradient-to-br from-brand-100 to-brand-200 flex items-center justify-center">
        <span className="text-4xl text-brand-400">🧵</span>
      </div>
      <div className="p-4">
        {category_name && (
          <span className="text-xs text-brand-600 font-medium uppercase tracking-wide">{category_name}</span>
        )}
        <h3 className="font-semibold text-secondary-800 group-hover:text-brand-600 transition mt-1">{name}</h3>
        <p className="text-sm text-secondary-500">{brand}</p>
        <div className="mt-2 flex items-center gap-2">
          <span className="text-lg font-bold text-brand-700">{price.toFixed(2)} zł</span>
          {compare_price && (
            <>
              <span className="text-sm text-secondary-400 line-through">{compare_price.toFixed(2)} zł</span>
              <span className="text-xs bg-red-100 text-red-700 px-1.5 py-0.5 rounded">-{discount}%</span>
            </>
          )}
        </div>
        {has_variants && <span className="text-xs text-secondary-400 mt-1 block">Dostępne warianty</span>}
      </div>
    </Link>
  )
}
