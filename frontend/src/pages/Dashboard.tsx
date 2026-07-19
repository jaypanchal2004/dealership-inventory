import { useEffect, useState, type FormEvent } from 'react'
import { useAuth } from '../context/AuthContext'
import {
  listVehicles,
  searchVehicles,
  createVehicle,
  updateVehicle,
  deleteVehicle,
  purchaseVehicle,
  restockVehicle,
  type Vehicle,
  type VehicleInput,
} from '../api/vehicles'
import VehicleForm from '../components/VehicleForm'

function Dashboard() {
  const { role, logout } = useAuth()
  const isAdmin = role === 'admin'

  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [showAddForm, setShowAddForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [restockValues, setRestockValues] = useState<Record<string, string>>({})

  const [make, setMake] = useState('')
  const [category, setCategory] = useState('')
  const [minPrice, setMinPrice] = useState('')
  const [maxPrice, setMaxPrice] = useState('')

  async function loadVehicles() {
    setLoading(true)
    setError('')
    try {
      const hasFilters = make || category || minPrice || maxPrice
      const data = hasFilters
        ? await searchVehicles({
            make: make || undefined,
            category: category || undefined,
            min_price: minPrice ? parseFloat(minPrice) : undefined,
            max_price: maxPrice ? parseFloat(maxPrice) : undefined,
          })
        : await listVehicles()
      setVehicles(data)
    } catch {
      setError('Failed to load vehicles.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadVehicles()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function handleSearchSubmit(e: FormEvent) {
    e.preventDefault()
    loadVehicles()
  }

  function clearFilters() {
    setMake('')
    setCategory('')
    setMinPrice('')
    setMaxPrice('')
    setTimeout(loadVehicles, 0)
  }

  async function handleAdd(data: VehicleInput) {
    await createVehicle(data)
    setShowAddForm(false)
    await loadVehicles()
  }

  async function handleEdit(id: string, data: VehicleInput) {
    await updateVehicle(id, data)
    setEditingId(null)
    await loadVehicles()
  }

  async function handleDelete(id: string) {
    if (!confirm('Delete this vehicle? This cannot be undone.')) return
    try {
      await deleteVehicle(id)
      await loadVehicles()
    } catch {
      setError('Failed to delete vehicle.')
    }
  }

  async function handlePurchase(id: string) {
    try {
      await purchaseVehicle(id)
      await loadVehicles()
    } catch {
      setError('Purchase failed — vehicle may be out of stock.')
    }
  }

  async function handleRestock(id: string) {
    const qty = parseInt(restockValues[id] ?? '', 10)
    if (!qty || qty <= 0) return
    try {
      await restockVehicle(id, qty)
      setRestockValues((prev) => ({ ...prev, [id]: '' }))
      await loadVehicles()
    } catch {
      setError('Restock failed.')
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Dealership Inventory</h1>
        <div className="flex items-center gap-3">
          {isAdmin && (
            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">Admin</span>
          )}
          <button onClick={logout} className="text-sm text-gray-600 hover:underline">
            Log out
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto p-6">
        {error && <p className="bg-red-100 text-red-700 text-sm p-2 rounded mb-4">{error}</p>}

        <form onSubmit={handleSearchSubmit} className="bg-white p-4 rounded-lg shadow mb-6 flex flex-wrap gap-3 items-end">
          <div>
            <label className="text-xs text-gray-500 block">Make</label>
            <input value={make} onChange={(e) => setMake(e.target.value)}
              className="border border-gray-300 rounded px-2 py-1" />
          </div>
          <div>
            <label className="text-xs text-gray-500 block">Category</label>
            <input value={category} onChange={(e) => setCategory(e.target.value)}
              className="border border-gray-300 rounded px-2 py-1" />
          </div>
          <div>
            <label className="text-xs text-gray-500 block">Min Price</label>
            <input type="number" value={minPrice} onChange={(e) => setMinPrice(e.target.value)}
              className="border border-gray-300 rounded px-2 py-1 w-24" />
          </div>
          <div>
            <label className="text-xs text-gray-500 block">Max Price</label>
            <input type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)}
              className="border border-gray-300 rounded px-2 py-1 w-24" />
          </div>
          <button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700">
            Search
          </button>
          <button type="button" onClick={clearFilters} className="text-sm text-gray-500 hover:underline">
            Clear
          </button>
        </form>

       <div className="mb-6">
  {isAdmin && (
    !showAddForm ? (
      <button onClick={() => setShowAddForm(true)}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
        + Add Vehicle
      </button>
    ) : (
      <VehicleForm submitLabel="Add Vehicle" onSubmit={handleAdd} onCancel={() => setShowAddForm(false)} />
    )
  )}
      </div>

        {loading ? (
          <p className="text-gray-500">Loading vehicles...</p>
        ) : vehicles.length === 0 ? (
          <p className="text-gray-500">No vehicles found.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {vehicles.map((v) =>
              editingId === v.id ? (
                <VehicleForm key={v.id} initial={v} submitLabel="Save"
                  onSubmit={(data) => handleEdit(v.id, data)} onCancel={() => setEditingId(null)} />
              ) : (
                <div key={v.id} className="bg-white p-4 rounded-lg shadow border border-gray-200">
                  <h2 className="text-lg font-semibold text-gray-800">{v.make} {v.model}</h2>
                  <p className="text-sm text-gray-500">{v.category}</p>
                  <p className="text-xl font-bold text-blue-600 mt-2">${v.price.toLocaleString()}</p>
                  <p className="text-sm text-gray-600 mb-3">In stock: {v.quantity}</p>

                  <button onClick={() => handlePurchase(v.id)} disabled={v.quantity === 0}
                    className="w-full bg-blue-600 text-white py-1.5 rounded hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed mb-2">
                    {v.quantity === 0 ? 'Out of Stock' : 'Purchase'}
                  </button>

                  <div className="flex gap-2 mb-2">
  {isAdmin && (
    <button onClick={() => setEditingId(v.id)}
      className="flex-1 bg-gray-200 text-gray-700 py-1.5 rounded hover:bg-gray-300 text-sm">
      Edit
    </button>
  )}
  {isAdmin && (
    <button onClick={() => handleDelete(v.id)}
      className="flex-1 bg-red-100 text-red-700 py-1.5 rounded hover:bg-red-200 text-sm">
      Delete
    </button>
  )}
</div>

                  {isAdmin && (
                    <div className="flex gap-2 mt-2 pt-2 border-t border-gray-100">
                      <input type="number" min="1" placeholder="Qty"
                        value={restockValues[v.id] ?? ''}
                        onChange={(e) => setRestockValues((prev) => ({ ...prev, [v.id]: e.target.value }))}
                        className="w-20 border border-gray-300 rounded px-2 py-1 text-sm" />
                      <button onClick={() => handleRestock(v.id)}
                        className="flex-1 bg-purple-100 text-purple-700 py-1.5 rounded hover:bg-purple-200 text-sm">
                        Restock
                      </button>
                    </div>
                  )}
                </div>
              )
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default Dashboard