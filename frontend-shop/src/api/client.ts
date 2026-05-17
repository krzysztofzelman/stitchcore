import axios from 'axios'

const API = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
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
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const { data } = await axios.post('/api/v1/auth/refresh', { refresh_token: refresh })
          localStorage.setItem('access_token', data.access_token)
          original.headers.Authorization = `Bearer ${data.access_token}`
          return API(original)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  },
)

export default API

// ── Auth ───────────────────────────────────────────────────────────
export const authApi = {
  register: (data: { email: string; password: string; first_name: string; last_name: string }) =>
    API.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    API.post('/auth/login', data),
  me: () => API.get('/auth/me'),
}

// ── Products ───────────────────────────────────────────────────────
export const productsApi = {
  list: (params?: { search?: string; category_id?: number; page?: number; page_size?: number }) =>
    API.get('/products', { params }),
  get: (id: number) => API.get(`/products/${id}`),
  categories: () => API.get('/categories'),
}

// ── Orders ─────────────────────────────────────────────────────────
export const ordersApi = {
  list: (params?: { page?: number; page_size?: number }) =>
    API.get('/orders', { params }),
  get: (id: number) => API.get(`/orders/${id}`),
  create: (data: any) => API.post('/orders', data),
}

// ── Cart (localStorage) ────────────────────────────────────────────
export interface CartItem {
  product_id: number
  variant_id?: number
  product_name: string
  variant_label: string
  quantity: number
  unit_price: number
  image?: string
}
