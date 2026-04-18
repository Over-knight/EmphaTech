import React, { useEffect, useState } from 'react'
import api from '../services/api'

export default function Transactions() {
  const [items, setItems] = useState([])

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get('/transaction/list')
        setItems(res.data || [])
      } catch (err) {
        setItems([])
      }
    }
    load()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded shadow">
        <h2 className="text-lg font-semibold mb-4">Transactions</h2>
        {items.length === 0 ? (
          <div className="text-sm text-gray-600">No transactions yet</div>
        ) : (
          <ul>
            {items.map(tx => (
              <li key={tx.id} className="py-2 border-b">{tx.description || tx.type} - {tx.amount}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
