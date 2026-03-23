import { formatCurrency, formatDate, cn } from '@/lib/utils'

const STATUS_COLORS = {
  'Pending Approval': 'bg-amber-100 text-amber-700',
  Approved: 'bg-green-100 text-green-700',
  Rejected: 'bg-red-100 text-red-700',
  'On Hold': 'bg-slate-100 text-slate-600',
}

export default function ChangeOrderLog({ changeOrders }) {
  return (
    <div className="bg-white rounded-xl border shadow-sm overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            {['Number', 'Title', 'GC', 'Cost Impact', 'Schedule', 'Status', 'Submitted'].map((h) => (
              <th key={h} className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {changeOrders.length === 0 ? (
            <tr>
              <td colSpan={7} className="px-4 py-8 text-center text-slate-400 text-sm">No change orders found.</td>
            </tr>
          ) : (
            changeOrders.map((co) => (
              <tr key={co.id} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="px-4 py-3 text-xs font-mono font-semibold text-slate-500">{co.co_number}</td>
                <td className="px-4 py-3 text-sm font-medium text-slate-900 max-w-xs">{co.title}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{co.assigned_gc || '—'}</td>
                <td className="px-4 py-3 text-sm font-semibold text-slate-900">{formatCurrency(co.cost_impact)}</td>
                <td className="px-4 py-3 text-sm text-slate-600">
                  {co.schedule_impact > 0 ? `+${co.schedule_impact}d` : co.schedule_impact === 0 ? '—' : `${co.schedule_impact}d`}
                </td>
                <td className="px-4 py-3">
                  <span className={cn('text-xs px-2 py-1 rounded-full font-medium', STATUS_COLORS[co.status] || 'bg-slate-100 text-slate-600')}>
                    {co.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-slate-600">{formatDate(co.submitted_date)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
      <div className="px-4 py-2 border-t border-slate-100 text-xs text-slate-400">
        {changeOrders.length} record{changeOrders.length !== 1 ? 's' : ''}
      </div>
    </div>
  )
}
