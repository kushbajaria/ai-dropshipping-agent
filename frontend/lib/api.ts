import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'test-key-123'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json',
  },
})

export const analyzeProduct = async (data: any) => {
  try {
    const response = await api.post('/products/analyze', data)
    return response.data
  } catch (error) {
    throw error
  }
}

export const analyzeBatch = async (products: any[]) => {
  try {
    const response = await api.post('/products/analyze-products', {
      products,
    })
    return response.data
  } catch (error) {
    throw error
  }
}

export default api
