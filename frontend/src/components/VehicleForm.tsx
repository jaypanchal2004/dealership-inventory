import { useState, type FormEvent } from 'react'
import type { VehicleInput } from '../api/vehicles'

interface Props {
  initial?: VehicleInput
  onSubmit: (data: VehicleInput) => Promise<void>
  onCancel: () => void
  submitLabel: string
}

function VehicleForm({ initial, onSubmit, onCancel, submitLabel }: Props) {
  const [make, setMake] = useState(initial?.make ?? '')
  const [model, setModel] = useState(initial?.model ?? '')
  const [category, setCategory] = useState(initial?.category ?? '')
  const [price, setPrice] = useState(initial?.price?.toString() ?? '')
  const [quantity, setQuantity] = useState(initial?.quantity?.toString() ?? '')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      await onSubmit({
        make,
        model,
        category,
        price: parseFloat(price),
        quantity: parseInt(quantity, 10),
      })
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Something went wrong.')
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow border border-gray-200 space-y-3">
      {error && <p className="bg-red-100 text-red-700 text-sm p-2 rounded">{error}</p>}
      <div className="grid grid-cols-2 gap-3">
        <input required placeholder="Make" value={make} onChange={(e) => setMake(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2" />
        <input required placeholder="Model" value={model} onChange={(e) => setModel(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2" />
        <input required placeholder="Category" value={category} onChange={(e) => setCategory(e.target.value)}
          className="border border-gray-300 rounded px-3 py-2" />
        <input required type="number" min="0.01" step="0.01" placeholder="Price" value={price}
          onChange={(e) => setPrice(e.target.value)} className="border border-gray-300 rounded px-3 py-2" />
        <input required type="number" min="0" placeholder="Quantity" value={quantity}
          onChange={(e) => setQuantity(e.target.value)} className="border border-gray-300 rounded px-3 py-2" />
      </div>
      <div className="flex gap-2">
        <button type="submit" disabled={saving}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
          {saving ? 'Saving...' : submitLabel}
        </button>
        <button type="button" onClick={onCancel}
          className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">
          Cancel
        </button>
      </div>
    </form>
  )
}

export default VehicleForm