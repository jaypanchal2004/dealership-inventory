import axios from 'axios'

// Checks Vercel's environment variable in production, falls back to local during development
const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const client = axios.create({
  baseURL: BASE_URL,
})

// Attach the JWT to every request automatically, if we have one
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default client