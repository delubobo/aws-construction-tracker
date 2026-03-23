import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AppShell from '@/components/layout/AppShell'
import Dashboard from '@/pages/Dashboard'
import RFIs from '@/pages/RFIs'
import Submittals from '@/pages/Submittals'
import ChangeOrders from '@/pages/ChangeOrders'
import OFMTracker from '@/pages/OFMTracker'
import Vendors from '@/pages/Vendors'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/rfis" element={<RFIs />} />
          <Route path="/submittals" element={<Submittals />} />
          <Route path="/change-orders" element={<ChangeOrders />} />
          <Route path="/ofm" element={<OFMTracker />} />
          <Route path="/vendors" element={<Vendors />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
