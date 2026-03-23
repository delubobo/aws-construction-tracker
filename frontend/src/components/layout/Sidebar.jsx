import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  FileQuestion,
  FileCheck,
  DollarSign,
  Package,
  Users,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/rfis', icon: FileQuestion, label: 'RFIs' },
  { to: '/submittals', icon: FileCheck, label: 'Submittals' },
  { to: '/change-orders', icon: DollarSign, label: 'Change Orders' },
  { to: '/ofm', icon: Package, label: 'OFM Tracker' },
  { to: '/vendors', icon: Users, label: 'Vendors' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white flex flex-col shrink-0">
      <div className="px-6 py-5 border-b border-slate-700">
        <div className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1">
          AWS DCCD
        </div>
        <div className="text-sm font-bold text-white leading-tight">
          RFI &amp; Change Order Tracker
        </div>
        <div className="text-xs text-slate-400 mt-1">Lubbock Region · Phase 2</div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              )
            }
          >
            <Icon size={17} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-4 border-t border-slate-700 text-xs text-slate-500">
        AWS Data Center Expansion
      </div>
    </aside>
  )
}
