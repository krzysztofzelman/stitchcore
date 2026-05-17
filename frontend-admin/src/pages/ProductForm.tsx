import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  TextField, Button, Typography, Alert, Paper, Box,
} from '@mui/material'
import { productsApi } from '../api/client'

interface Category {
  id: number
  name: string
}

export default function ProductForm() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = Boolean(id)
  const [categories, setCategories] = useState<Category[]>([])
  const [form, setForm] = useState({
    name: '', slug: '', description: '', price: 0, compare_price: 0,
    category_id: 0, brand: '', sku: '', size: '', color: '', price_adjustment: 0,
  })
  const [error, setError] = useState('')

  useEffect(() => {
    productsApi.categories().then(({ data }) => setCategories(data || []))
    if (isEdit) {
      productsApi.get(Number(id)).then(({ data }) => {
        setForm({
          name: data.name || '', slug: data.slug || '', description: data.description || '',
          price: data.price || 0, compare_price: data.compare_price || 0,
          category_id: data.category_id || 0, brand: data.brand || '',
          sku: '', size: '', color: '', price_adjustment: 0,
        })
      })
    }
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (isEdit) {
        await productsApi.update(Number(id), {
          name: form.name, slug: form.slug, description: form.description,
          price: form.price, compare_price: form.compare_price || null,
          category_id: form.category_id || null, brand: form.brand,
        })
      } else {
        const { data } = await productsApi.create({
          name: form.name, slug: form.slug, description: form.description,
          price: form.price, compare_price: form.compare_price || null,
          category_id: form.category_id || null, brand: form.brand,
        })
        if (form.sku) {
          await productsApi.createVariant(data.id, {
            sku: form.sku, size: form.size, color: form.color,
            price_adjustment: form.price_adjustment,
          })
        }
      }
      navigate('/products')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Błąd zapisu')
    }
  }

  const set = (k: string, v: any) => setForm((prev) => ({ ...prev, [k]: v }))

  return (
    <Box maxWidth={600}>
      <Typography variant="h4" fontWeight={700} mb={3}>{isEdit ? 'Edytuj produkt' : 'Nowy produkt'}</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <TextField label="Nazwa" fullWidth required sx={{ mb: 2 }} value={form.name} onChange={(e) => set('name', e.target.value)} />
          <TextField label="Slug" fullWidth required sx={{ mb: 2 }} value={form.slug} onChange={(e) => set('slug', e.target.value)} />
          <TextField label="Opis" fullWidth multiline rows={3} sx={{ mb: 2 }} value={form.description} onChange={(e) => set('description', e.target.value)} />
          <TextField label="Cena" type="number" fullWidth required sx={{ mb: 2 }} value={form.price} onChange={(e) => set('price', Number(e.target.value))} />
          <TextField label="Cena porównawcza" type="number" fullWidth sx={{ mb: 2 }} value={form.compare_price} onChange={(e) => set('compare_price', Number(e.target.value))} />
          <TextField label="Marka" fullWidth sx={{ mb: 2 }} value={form.brand} onChange={(e) => set('brand', e.target.value)} />
          <TextField label="Kategoria ID" type="number" fullWidth sx={{ mb: 2 }} value={form.category_id} onChange={(e) => set('category_id', Number(e.target.value))} />
          {!isEdit && (
            <>
              <Typography variant="subtitle2" mt={2} mb={1}>Pierwszy wariant (opcjonalnie)</Typography>
              <TextField label="SKU" fullWidth sx={{ mb: 2 }} value={form.sku} onChange={(e) => set('sku', e.target.value)} />
              <TextField label="Rozmiar" fullWidth sx={{ mb: 2 }} value={form.size} onChange={(e) => set('size', e.target.value)} />
              <TextField label="Kolor" fullWidth sx={{ mb: 2 }} value={form.color} onChange={(e) => set('color', e.target.value)} />
              <TextField label="Korekta ceny" type="number" fullWidth sx={{ mb: 2 }} value={form.price_adjustment} onChange={(e) => set('price_adjustment', Number(e.target.value))} />
            </>
          )}
          <Box display="flex" gap={2} mt={2}>
            <Button type="submit" variant="contained">{isEdit ? 'Zapisz' : 'Utwórz'}</Button>
            <Button variant="outlined" onClick={() => navigate('/products')}>Anuluj</Button>
          </Box>
        </form>
      </Paper>
    </Box>
  )
}
