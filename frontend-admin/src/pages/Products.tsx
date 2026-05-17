import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Typography, Chip,
} from '@mui/material'
import { productsApi } from '../api/client'

interface ProductItem {
  id: number
  name: string
  price: number
  brand: string
  category_name: string | null
  has_variants: boolean
}

export default function Products() {
  const [products, setProducts] = useState<ProductItem[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    productsApi.list({ page_size: 100 }).then(({ data }) => setProducts(data.results || []))
  }, [])

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Typography variant="h4" fontWeight={700}>Produkty</Typography>
        <Button variant="contained" onClick={() => navigate('/products/new')}>Dodaj produkt</Button>
      </div>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nazwa</TableCell>
              <TableCell>Marka</TableCell>
              <TableCell>Kategoria</TableCell>
              <TableCell align="right">Cena</TableCell>
              <TableCell>Warianty</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {products.map((p) => (
              <TableRow key={p.id} hover sx={{ cursor: 'pointer' }} onClick={() => navigate(`/products/${p.id}`)}>
                <TableCell>{p.name}</TableCell>
                <TableCell>{p.brand}</TableCell>
                <TableCell>{p.category_name || '-'}</TableCell>
                <TableCell align="right">{Number(p.price).toFixed(2)} zł</TableCell>
                <TableCell>{p.has_variants ? <Chip label="Tak" size="small" color="primary" /> : '-'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}
