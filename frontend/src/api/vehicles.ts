import client from './client'

export interface Vehicle {
  id: string
  make: string
  model: string
  category: string
  price: number
  quantity: number
}

export interface VehicleInput {
  make: string
  model: string
  category: string
  price: number
  quantity: number
}

export interface SearchFilters {
  make?: string
  category?: string
  min_price?: number
  max_price?: number
}

export async function listVehicles(): Promise<Vehicle[]> {
  const res = await client.get('/api/vehicles')
  return res.data
}

export async function searchVehicles(filters: SearchFilters): Promise<Vehicle[]> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== '')
  )
  const res = await client.get('/api/vehicles/search', { params })
  return res.data
}

export async function createVehicle(data: VehicleInput): Promise<Vehicle> {
  const res = await client.post('/api/vehicles', data)
  return res.data
}

export async function updateVehicle(id: string, data: VehicleInput): Promise<Vehicle> {
  const res = await client.put(`/api/vehicles/${id}`, data)
  return res.data
}

export async function deleteVehicle(id: string): Promise<void> {
  await client.delete(`/api/vehicles/${id}`)
}

export async function purchaseVehicle(id: string): Promise<Vehicle> {
  const res = await client.post(`/api/vehicles/${id}/purchase`)
  return res.data
}

export async function restockVehicle(id: string, quantity: number): Promise<Vehicle> {
  const res = await client.post(`/api/vehicles/${id}/restock`, { quantity })
  return res.data
}