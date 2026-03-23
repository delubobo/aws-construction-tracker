import { DollarSign } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'

export default function CORunningTotal({ pendingValue, totalValue, count }) {
  return (
    <div className="flex items-center gap-6 bg-amber-50 border border-amber-200 rounded-xl px-5 py-4 mb-5">
      <div className="p-2.5 bg-amber-100 rounded-lg text-amber-600">
        <DollarSign size={20} />
      </div>
      <div>
        <p className="text-xs font-semibold text-amber-600 uppercase tracking-wide">Pending Approval</p>
        <p className="text-2xl font-bold text-amber-900">{formatCurrency(pendingValue)}</p>
        <p className="text-xs text-amber-600 mt-0.5">{count} change order{count !== 1 ? 's' : ''} awaiting approval</p>
      </div>
      {totalValue !== pendingValue && (
        <div className="ml-auto text-right">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Total CO Value</p>
          <p className="text-xl font-bold text-slate-800">{formatCurrency(totalValue)}</p>
        </div>
      )}
    </div>
  )
}
