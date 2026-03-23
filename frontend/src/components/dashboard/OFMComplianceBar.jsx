import { cn } from '@/lib/utils'

export default function OFMComplianceBar({ pct }) {
  const value = pct ?? 0
  const color = value >= 80 ? 'bg-green-500' : value >= 60 ? 'bg-amber-500' : 'bg-red-500'

  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-1">OFM On-Time Compliance</h3>
      <p className="text-3xl font-bold text-slate-900 mb-3">{value.toFixed(1)}%</p>
      <div className="w-full bg-slate-100 rounded-full h-3">
        <div
          className={cn('h-3 rounded-full transition-all duration-500', color)}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
      <p className="text-xs text-slate-500 mt-2">Equipment deliveries on or before scheduled date</p>
    </div>
  )
}
