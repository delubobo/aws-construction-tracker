import { formatDate, cn } from '@/lib/utils'
import OFMStatusBadge from './OFMStatusBadge'

export default function OFMTable({ items }) {
  // Sort Red first, then Amber, then Green
  const sorted = [...items].sort((a, b) => {
    const order = { Red: 0, Amber: 1, Green: 2 }
    return (order[a.rag_status] ?? 3) - (order[b.rag_status] ?? 3)
  })

  return (
    <div className="bg-white rounded-xl border shadow-sm overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            {['Tag', 'Description', 'Supplier', 'Expected', 'Actual', 'Variance', 'Status', 'Notes'].map((h) => (
              <th key={h} className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.length === 0 ? (
            <tr>
              <td colSpan={8} className="px-4 py-8 text-center text-slate-400 text-sm">No OFM items found.</td>
            </tr>
          ) : (
            sorted.map((item) => (
              <tr
                key={item.id}
                className={cn(
                  'border-b border-slate-100 hover:bg-slate-50',
                  item.rag_status === 'Red' && 'bg-red-50 hover:bg-red-50',
                  item.rag_status === 'Amber' && 'bg-amber-50 hover:bg-amber-50'
                )}
              >
                <td className="px-4 py-3 text-xs font-mono font-bold text-slate-700">{item.equipment_tag}</td>
                <td className="px-4 py-3 text-sm text-slate-900 max-w-xs">{item.description}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{item.supplier || '—'}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{formatDate(item.expected_delivery)}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{formatDate(item.actual_delivery) || '—'}</td>
                <td className="px-4 py-3 text-sm font-medium">
                  {item.variance_days == null ? (
                    <span className="text-slate-400">—</span>
                  ) : item.variance_days > 0 ? (
                    <span className="text-red-600">+{item.variance_days}d late</span>
                  ) : item.variance_days < 0 ? (
                    <span className="text-green-600">{Math.abs(item.variance_days)}d early</span>
                  ) : (
                    <span className="text-green-600">On time</span>
                  )}
                </td>
                <td className="px-4 py-3"><OFMStatusBadge status={item.rag_status} /></td>
                <td className="px-4 py-3 text-xs text-slate-500 max-w-xs truncate" title={item.notes}>{item.notes || '—'}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
