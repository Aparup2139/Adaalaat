import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './components/LandingPage'
import AuthPage from './components/AuthPage'
import ClientDashboard from './components/ClientDashboard'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/dashboard" element={<ClientDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
