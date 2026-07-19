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
    <div className="min-h-screen bg-slate-100">
      <header className="bg-[#1e293b] shadow px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🚗</span>
          <div>
            <h1 className="text-lg font-bold text-white leading-tight">Jay's Car Dealership</h1>
            <p className="text-xs text-slate-400 leading-tight">
              {isAdmin ? 'Manage your inventory' : 'Browse our inventory'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {isAdmin && (
            <span className="text-xs bg-[#d97706] text-white font-medium px-2.5 py-1 rounded-full">
              Admin
            </span>
          )}
          <button onClick={logout} className="text-sm text-slate-300 hover:text-white hover:underline">
            Log out
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto p-6">
        {error && <p className="bg-red-100 text-red-700 text-sm p-2 rounded mb-4">{error}</p>}

        <form onSubmit={handleSearchSubmit} className="bg-white p-4 rounded-lg shadow mb-6 flex flex-wrap gap-3 items-end">
          <div>
            <label className="text-xs text-slate-500 block">Make</label>
            <input value={make} onChange={(e) => setMake(e.target.value)}
              className="border border-slate-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-[#d97706]" />
          </div>
          <div>
            <label className="text-xs text-slate-500 block">Category</label>
            <input value={category} onChange={(e) => setCategory(e.target.value)}
              className="border border-slate-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-[#d97706]" />
          </div>
          <div>
            <label className="text-xs text-slate-500 block">Min Price</label>
            <input type="number" value={minPrice} onChange={(e) => setMinPrice(e.target.value)}
              className="border border-slate-300 rounded px-2 py-1 w-24 focus:outline-none focus:ring-2 focus:ring-[#d97706]" />
          </div>
          <div>
            <label className="text-xs text-slate-500 block">Max Price</label>
            <input type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)}
              className="border border-slate-300 rounded px-2 py-1 w-24 focus:outline-none focus:ring-2 focus:ring-[#d97706]" />
          </div>
          <button type="submit" className="bg-[#1e293b] text-white px-3 py-1.5 rounded hover:bg-[#334155] font-medium">
            Search
          </button>
          <button type="button" onClick={clearFilters} className="text-sm text-slate-500 hover:underline">
            Clear
          </button>
        </form>

        {isAdmin && (
          <div className="mb-6 bg-amber-50 border border-amber-200 rounded-lg p-4">
            <p className="text-xs font-semibold text-amber-800 uppercase tracking-wide mb-3">
              Admin Controls
            </p>
            {!showAddForm ? (
              <button onClick={() => setShowAddForm(true)}
                className="bg-[#d97706] text-white px-4 py-2 rounded hover:bg-amber-700 font-medium">
                + Add Vehicle
              </button>
            ) : (
              <VehicleForm submitLabel="Add Vehicle" onSubmit={handleAdd} onCancel={() => setShowAddForm(false)} />
            )}
          </div>
        )}

        {loading ? (
          <p className="text-slate-500">Loading vehicles...</p>
        ) : vehicles.length === 0 ? (
          <p className="text-slate-500">
            {isAdmin ? "No vehicles yet — add your first one above." : "No vehicles found. Try adjusting your search."}
          </p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {vehicles.map((v) =>
              editingId === v.id ? (
                <VehicleForm key={v.id} initial={v} submitLabel="Save"
                  onSubmit={(data) => handleEdit(v.id, data)} onCancel={() => setEditingId(null)} />
              ) : (
                <div key={v.id} className="bg-white p-4 rounded-lg shadow border border-slate-200 hover:shadow-md transition-shadow">
                  <h2 className="text-lg font-semibold text-slate-800">{v.make} {v.model}</h2>
                  <p className="text-sm text-slate-500">{v.category}</p>
                  <p className="text-xl font-bold text-[#1e293b] mt-2">${v.price.toLocaleString()}</p>
                  <p className="text-sm text-slate-600 mb-3">In stock: {v.quantity}</p>

                  <button onClick={() => handlePurchase(v.id)} disabled={v.quantity === 0}
                    className="w-full bg-[#d97706] text-white py-1.5 rounded hover:bg-amber-700 disabled:opacity-40 disabled:cursor-not-allowed mb-2 font-medium transition-colors">
                    {v.quantity === 0 ? 'Out of Stock' : 'Purchase'}
                  </button>

                  {isAdmin && (
                    <>
                      <div className="flex gap-2 mb-2">
                        <button onClick={() => setEditingId(v.id)}
                          className="flex-1 bg-slate-200 text-slate-700 py-1.5 rounded hover:bg-slate-300 text-sm font-medium">
                          Edit
                        </button>
                        <button onClick={() => handleDelete(v.id)}
                          className="flex-1 bg-red-100 text-red-700 py-1.5 rounded hover:bg-red-200 text-sm font-medium">
                          Delete
                        </button>
                      </div>

                      <div className="flex gap-2 mt-2 pt-2 border-t border-amber-100 bg-amber-50 -mx-4 -mb-4 px-4 pb-4 rounded-b-lg">
                        <input type="number" min="1" placeholder="Qty"
                          value={restockValues[v.id] ?? ''}
                          onChange={(e) => setRestockValues((prev) => ({ ...prev, [v.id]: e.target.value }))}
                          className="w-20 border border-amber-300 rounded px-2 py-1 text-sm mt-2 focus:outline-none focus:ring-2 focus:ring-[#d97706]" />
                        <button onClick={() => handleRestock(v.id)}
                          className="flex-1 bg-amber-200 text-amber-800 py-1.5 rounded hover:bg-amber-300 text-sm font-medium mt-2">
                          Restock
                        </button>
                      </div>
                    </>
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