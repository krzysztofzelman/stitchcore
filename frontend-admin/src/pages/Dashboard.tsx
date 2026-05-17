import { useEffect, useState } from 'react'
import { Grid, Card, CardContent, Typography } from '@mui/material'
import { ordersApi, productsApi, inventoryApi } from '../api/client'

export default function Dashboard() {
  const [stats, setStats] = useState({ products: 0, orders: 0, stockItems: 0, lowStock: 0 })

  useEffect(() => {
    productsApi.list({ page_size: 1 }).then(({ data }) => setStats((s) => ({ ...s, products: data.count || 0 })))
    ordersApi.list({ page_size: 1 }).then(({ data }) => setStats((s) => ({ ...s, orders: data.count || 0 })))
    inventoryApi.stock().then(({ data }) => {
      setStats((s) => ({ ...s, stockItems: data.length, lowStock: data.filter((i: any) => i.quantity <= i.low_stock_threshold).length }))
    })
  }, [])

  const cards = [
    { title: 'Produkty', value: stats.products, color: '#2563eb' },
    { title: 'Zamówienia', value: stats.orders, color: '#7c3aed' },
    { title: 'Pozycje magazynowe', value: stats.stockItems, color: '#059669' },
    { title: 'Niski stan', value: stats.lowStock, color: '#dc2626' },
  ]

  return (
    <div>
      <Typography variant="h4" fontWeight={700} mb={4}>Dashboard</Typography>
      <Grid container spacing={3}>
        {cards.map((c) => (
          <Grid item xs={12} sm={6} md={3} key={c.title}>
            <Card>
              <CardContent>
                <Typography variant="body2" color="text.secondary">{c.title}</Typography>
                <Typography variant="h3" fontWeight={700} sx={{ color: c.color }}>{c.value}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  )
}
