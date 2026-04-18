import React, { useState } from 'react'
import api from '../services/api'

export default function Send() {
  const [account, setAccount] = useState('')
  const [bankCode, setBankCode] = useState('')
  const [amount, setAmount] = useState('')
  const [message, setMessage] = useState(null)

  async function submit(e) {
    e.preventDefault()
    try {
      const res = await api.post('/transaction/send-money', { account, bankCode, amount })
      setMessage(res.data?.message || 'Sent')
    } catch (err) {
      setMessage(err?.response?.data?.message || 'Error')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
        <h2 className="text-lg font-semibold mb-4">Send Money</h2>
        {message && <div className="mb-3 text-sm text-green-700">{message}</div>}
        <form onSubmit={submit}>
          <input placeholder="Account number" value={account} onChange={e => setAccount(e.target.value)} className="mb-2 block w-full border px-3 py-2 rounded" />
          <input placeholder="Bank code" value={bankCode} onChange={e => setBankCode(e.target.value)} className="mb-2 block w-full border px-3 py-2 rounded" />
          <input placeholder="Amount" value={amount} onChange={e => setAmount(e.target.value)} className="mb-4 block w-full border px-3 py-2 rounded" />
          <button className="w-full bg-green-600 text-white py-2 rounded">Send</button>
        </form>
      </div>
    </div>
  )
}
