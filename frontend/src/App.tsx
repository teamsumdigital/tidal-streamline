import { Routes, Route } from 'react-router-dom'
import { ClientPortal } from './pages/ClientPortal'
import { InternalDashboard } from './pages/InternalDashboard'
import { MarketScanResults } from './pages/MarketScanResults'
import { Layout } from './components/Layout'

function App() {
  return (
    <Layout>
      <Routes>
        {/* Public client-facing route */}
        <Route path="/" element={<ClientPortal />} />
        <Route path="/client" element={<ClientPortal />} />
        
        {/* Market scan results */}
        <Route path="/scan/:scanId" element={<MarketScanResults />} />
        
        {/* Internal Tidal team routes */}
        <Route path="/dashboard" element={<InternalDashboard />} />
        <Route path="/admin" element={<InternalDashboard />} />
        
        {/* Catch all - redirect to client portal */}
        <Route path="*" element={<ClientPortal />} />
      </Routes>
    </Layout>
  )
}

export default App