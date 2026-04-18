import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Send from './pages/Send'
import Recharge from './pages/Recharge'
import Transactions from './pages/Transactions'

function App() {
  const isAuthenticated = !!localStorage.getItem('token')

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
      />
      <Route path="/send" element={isAuthenticated ? <Send /> : <Navigate to="/login" />} />
      <Route path="/recharge" element={isAuthenticated ? <Recharge /> : <Navigate to="/login" />} />
      <Route path="/transactions" element={isAuthenticated ? <Transactions /> : <Navigate to="/login" />} />
    </Routes>
  )
}

export default App
