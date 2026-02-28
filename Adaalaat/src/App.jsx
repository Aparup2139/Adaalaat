import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './components/LandingPage'
import AuthPage from './components/AuthPage'
import ClientDashboard from './components/ClientDashboard'
import LawyerDashboard from './components/LawyerDashboard'
import FindLawyer from './components/FindLawyer'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/dashboard" element={<ClientDashboard />} />
        <Route path="/lawyer-dashboard" element={<LawyerDashboard />} />
        <Route path="/find-lawyer" element={<FindLawyer />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
