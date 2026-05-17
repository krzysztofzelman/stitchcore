import { Routes, Route, Navigate } from 'react-router-dom'
import { CircularProgress, Box, Typography, Button } from '@mui/material'
import { useAuth } from './contexts/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import ProductForm from './pages/ProductForm'
import Orders from './pages/Orders'
import OrderDetail from './pages/OrderDetail'
import Inventory from './pages/Inventory'

function Protected({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) return <Box display="flex" justifyContent="center" py={8}><CircularProgress /></Box>
  if (!user) return <Navigate to="/login" replace />
  if (user.role !== 'admin') {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="100vh" bgcolor="#f1f5f9">
        <Typography variant="h5" fontWeight={700} color="error" mb={2}>Brak dostępu</Typography>
        <Typography variant="body1" color="text.secondary" mb={3}>Ta sekcja dostępna jest tylko dla administratorów.</Typography>
        <Button variant="contained" onClick={() => {
          localStorage.removeItem('admin_access_token')
          localStorage.removeItem('admin_refresh_token')
          window.location.href = '/login'
        }}>Wyloguj</Button>
      </Box>
    )
  }
  return <>{children}</>
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Protected><Layout /></Protected>}>
        <Route index element={<Dashboard />} />
        <Route path="products" element={<Products />} />
        <Route path="products/new" element={<ProductForm />} />
        <Route path="products/:id" element={<ProductForm />} />
        <Route path="orders" element={<Orders />} />
        <Route path="orders/:id" element={<OrderDetail />} />
        <Route path="inventory" element={<Inventory />} />
      </Route>
    </Routes>
  )
}
