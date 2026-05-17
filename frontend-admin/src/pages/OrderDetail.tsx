import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Typography, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Button, Box, Select, MenuItem, TextField, Alert,
} from '@mui/material'
import { ordersApi } from '../api/client'

interface OrderItem {
  product_name: string
  variant_label: string
  quantity: number
  unit_price: number
}

interface Order {
  id: number
  order_number: string
  status: string
  total: number
  shipping_address: string
  shipping_method: string
  tracking_number: string
  notes: string
  created_at: string
  items: OrderItem[]
}

const statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']

export default function OrderDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [order, setOrder] = useState<Order | null>(null)
  const [status, setStatus] = useState('')
  const [tracking, setTracking] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (id) {
      ordersApi.get(Number(id)).then(({ data }) => {
        setOrder(data)
        setStatus(data.status)
        setTracking(data.tracking_number || '')
      })
    }
  }, [id])

  const handleUpdate = async () => {
    try {
      await ordersApi.updateStatus(Number(id), { status, tracking_number: tracking || null })
      setMessage('Zaktualizowano')
    } catch (err: any) {
      setMessage('Błąd: ' + (err.response?.data?.detail || 'nieznany'))
    }
  }

  if (!order) return <Typography>Ładowanie...</Typography>

  return (
    <div>
      <Button onClick={() => navigate('/orders')} sx={{ mb: 2 }}>&larr; Powrót</Button>
      <Typography variant="h4" fontWeight={700} mb={2}>{order.order_number}</Typography>
      {message && <Alert severity={message.startsWith('Błąd') ? 'error' : 'success'} sx={{ mb: 2 }}>{message}</Alert>}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" mb={2}>Szczegóły</Typography>
        <Typography>Status: {order.status}</Typography>
        <Typography>Kwota: {Number(order.total).toFixed(2)} zł</Typography>
        <Typography>Adres: {order.shipping_address || 'Odbiór osobisty'}</Typography>
        <Typography>Metoda: {order.shipping_method}</Typography>
        <Typography>Nr przesyłki: {order.tracking_number || '-'}</Typography>
        <Typography>Uwagi: {order.notes || '-'}</Typography>
        <Typography>Data: {new Date(order.created_at).toLocaleDateString('pl-PL')}</Typography>
      </Paper>

      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Produkt</TableCell>
              <TableCell>Wariant</TableCell>
              <TableCell align="right">Ilość</TableCell>
              <TableCell align="right">Cena</TableCell>
              <TableCell align="right">Suma</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {order.items.map((item, idx) => (
              <TableRow key={idx}>
                <TableCell>{item.product_name}</TableCell>
                <TableCell>{item.variant_label || '-'}</TableCell>
                <TableCell align="right">{item.quantity}</TableCell>
                <TableCell align="right">{Number(item.unit_price).toFixed(2)} zł</TableCell>
                <TableCell align="right">{(item.quantity * Number(item.unit_price)).toFixed(2)} zł</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" mb={2}>Zarządzanie</Typography>
        <Box display="flex" gap={2} mb={2}>
          <Select value={status} onChange={(e) => setStatus(e.target.value)} size="small" sx={{ minWidth: 160 }}>
            {statuses.map((s) => <MenuItem key={s} value={s}>{s}</MenuItem>)}
          </Select>
          <TextField label="Nr przesyłki" size="small" value={tracking} onChange={(e) => setTracking(e.target.value)} />
        </Box>
        <Button variant="contained" onClick={handleUpdate}>Aktualizuj</Button>
      </Paper>
    </div>
  )
}
