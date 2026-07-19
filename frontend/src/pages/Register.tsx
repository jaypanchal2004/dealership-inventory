import { useState, type FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register as registerRequest, login as loginRequest } from '../api/auth'
import { useAuth } from '../context/AuthContext'

function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await registerRequest({ username, email, password })
      const data = await loginRequest({ email, password })
      login(data.access_token)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#1e293b] px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-[#d97706] mb-3">
            <span className="text-2xl">🚗</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Jay's Car Dealership</h1>
          <p className="text-sm text-slate-400 mt-1">Create an account to get started</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-white p-8 rounded-lg shadow-2xl w-full"
        >
          <h2 className="text-xl font-semibold mb-6 text-slate-800">Create Account</h2>

          {error && (
            <p className="bg-red-100 text-red-700 text-sm p-2 rounded mb-4">
              {error}
            </p>
          )}

          <label className="block mb-3">
            <span className="text-sm text-slate-600">Username</span>
            <input
              type="text"
              required
              minLength={3}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 w-full border border-slate-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#d97706]"
            />
          </label>

          <label className="block mb-3">
            <span className="text-sm text-slate-600">Email</span>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full border border-slate-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#d97706]"
            />
          </label>

          <label className="block mb-6">
            <span className="text-sm text-slate-600">Password</span>
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full border border-slate-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#d97706]"
            />
            <span className="text-xs text-slate-400">At least 8 characters</span>
          </label>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#1e293b] text-white py-2 rounded hover:bg-[#334155] disabled:opacity-50 font-medium transition-colors"
          >
            {loading ? 'Creating account...' : 'Register'}
          </button>

          <p className="text-sm text-slate-600 mt-4 text-center">
            Already have an account?{' '}
            <Link to="/login" className="text-[#d97706] font-medium hover:underline">
              Log In
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}

export default Register