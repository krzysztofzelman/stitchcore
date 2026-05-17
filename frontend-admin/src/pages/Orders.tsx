import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  Paper, Typography, Chip,
} from '@mui/material'
import { ordersApi } from '../api/client'

interface Order {
  id: number
  order_number: string
  status: string
  total: number
  created_at: string
}

const statusColors: Record<string, 'warning' | 'info' | 'primary' | 'success' | 'error'> = {
  pending: 'warning', confirmed: 'info', processing: 'primary',
  shipped: 'primary', delivered: 'success', cancelled: 'error',
}

export default function Orders() {
  const [orders, setOrders] = useState<Order[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    ordersApi.list({ page_size: 100 }).then(({ data }) => setOrders(data.results || []))
  }, [])

  return (
    <div>
      <Typography variant="h4" fontWeight={700} mb={2}>Zamówienia</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nr zamówienia</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right">Kwota</TableCell>
              <TableCell>Data</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map((o) => (
              <TableRow key={o.id} hover sx={{ cursor: 'pointer' }} onClick={() => navigate(`/orders/${o.id}`)}>
                <TableCell>{o.order_number}</TableCell>
                <TableCell>
                  <Chip label={o.status} color={statusColors[o.status] || 'default'} size="small" />
                </TableCell>
                <TableCell align="right">{Number(o.total).toFixed(2)} zł</TableCell>
                <TableCell>{new Date(o.created_at).toLocaleDateString('pl-PL')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}
