import React from 'react'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow p-4 flex justify-between">
        <h1 className="text-xl font-semibold">EmphaTech</h1>
        <div>
          <Link to="/transactions" className="mr-4">Transactions</Link>
          <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/login' }} className="text-sm text-red-600">Logout</button>
        </div>
      </header>

      <main className="p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white p-6 rounded shadow"> 
            <h2 className="text-lg font-semibold">Balance</h2>
            <div className="text-3xl font-bold mt-2">NGN 0.00</div>
            <div className="mt-4 flex gap-3">
              <Link to="/send" className="px-4 py-2 bg-green-600 text-white rounded">Send</Link>
              <Link to="/recharge" className="px-4 py-2 bg-yellow-500 text-white rounded">Recharge</Link>
            </div>
          </div>

          <div className="mt-6 bg-white p-6 rounded shadow">
            <h3 className="font-semibold">Recent Transactions</h3>
            <div className="mt-2 text-sm text-gray-600">No recent transactions</div>
          </div>
        </div>
      </main>
    </div>
  )
}
