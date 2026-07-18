import client from './client'

export interface RegisterPayload {
  username: string
  email: string
  password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export async function register(data: RegisterPayload) {
  const response = await client.post('/api/auth/register', data)
  return response.data
}

export async function login(data: LoginPayload) {
  const response = await client.post('/api/auth/login', data)
  return response.data as { access_token: string; token_type: string }
}