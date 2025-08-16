import { Routes, Route } from 'react-router-dom'
import { ClientPortal } from './pages/ClientPortal'
import { InternalDashboard } from './pages/InternalDashboard'
import { MarketScanResults } from './pages/MarketScanResults'
import { DataExport } from './pages/DataExport'
import { Layout } from './components/Layout'
import { CandidateCardDemo } from './components/ui/CandidateCardDemo'

function App() {
  return (
    <Layout>
      <Routes>
        {/* Public client-facing route */}
        <Route path="/" element={<ClientPortal />} />
        <Route path="/client" element={<ClientPortal />} />
        
        {/* Payroll calculation results */}
        <Route path="/scan/:scanId" element={<MarketScanResults />} />
        
        {/* Data export for Canva templates */}
        <Route path="/scan/:scanId/export" element={<DataExport />} />
        
        {/* Internal Tidal team routes */}
        <Route path="/dashboard" element={<InternalDashboard />} />
        <Route path="/admin" element={<InternalDashboard />} />
        
        {/* Demo routes for development */}
        <Route path="/demo/candidate-card" element={<CandidateCardDemo />} />
        
        {/* Catch all - redirect to client portal */}
        <Route path="*" element={<ClientPortal />} />
      </Routes>
    </Layout>
  )
}

export default App