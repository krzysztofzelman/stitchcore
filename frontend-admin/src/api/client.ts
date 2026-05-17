import axios from 'axios'

const API = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

API.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('admin_refresh_token')
      if (refresh) {
        try {
          const { data } = await axios.post('/api/v1/auth/refresh', { refresh_token: refresh })
          localStorage.setItem('admin_access_token', data.access_token)
          original.headers.Authorization = `Bearer ${data.access_token}`
          return API(original)
        } catch {
          localStorage.removeItem('admin_access_token')
          localStorage.removeItem('admin_refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  },
)

export default API

export const authApi = {
  login: (data: { email: string; password: string }) => API.post('/auth/login', data),
  me: () => API.get('/auth/me'),
}

export const productsApi = {
  list: (params?: any) => API.get('/products', { params }),
  get: (id: number) => API.get(`/products/${id}`),
  create: (data: any) => API.post('/products', data),
  update: (id: number, data: any) => API.put(`/products/${id}`, data),
  categories: () => API.get('/categories'),
  createCategory: (data: any) => API.post('/categories', data),
  createVariant: (productId: number, data: any) => API.post(`/products/${productId}/variants`, data),
}

export const ordersApi = {
  list: (params?: any) => API.get('/orders', { params }),
  get: (id: number) => API.get(`/orders/${id}`),
  updateStatus: (id: number, data: any) => API.patch(`/orders/${id}/status`, data),
}

export const inventoryApi = {
  stock: (params?: any) => API.get('/inventory/stock', { params }),
  adjust: (data: any) => API.post('/inventory/stock/adjust', data),
  locations: () => API.get('/inventory/locations'),
  createLocation: (data: any) => API.post('/inventory/locations', data),
  movements: (params?: any) => API.get('/inventory/movements', { params }),
}
