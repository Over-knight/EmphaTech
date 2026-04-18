import React, { useState } from 'react'
import api from '../services/api'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    try {
      const res = await api.post('/user/login', { email, password })
      const token = res.data?.token
      if (token) {
        localStorage.setItem('token', token)
        window.location.href = '/'
      } else {
        setError('Invalid credentials')
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={submit} className="p-6 bg-white rounded shadow w-full max-w-md">
        <h2 className="text-2xl font-semibold mb-4">Sign in to EmphaTech</h2>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <label className="block mb-2">
          <span className="text-sm">Email</span>
          <input value={email} onChange={e => setEmail(e.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
        </label>
        <label className="block mb-4">
          <span className="text-sm">Password</span>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
        </label>
        <button className="w-full bg-blue-600 text-white py-2 rounded">Sign in</button>
      </form>
    </div>
  )
}
