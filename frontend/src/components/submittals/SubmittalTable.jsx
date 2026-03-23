import { formatDate, cn } from '@/lib/utils'

const STATUS_COLORS = {
  Pending: 'bg-amber-100 text-amber-700',
  Approved: 'bg-green-100 text-green-700',
  Rejected: 'bg-red-100 text-red-700',
  'Revise & Resubmit': 'bg-orange-100 text-orange-700',
}

export default function SubmittalTable({ submittals }) {
  return (
    <div className="bg-white rounded-xl border shadow-sm overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            {['Number', 'Description', 'Spec', 'GC', 'Rev', 'Status', 'Response Due', 'Returned'].map((h) => (
              <th key={h} className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {submittals.length === 0 ? (
            <tr>
              <td colSpan={8} className="px-4 py-8 text-center text-slate-400 text-sm">No submittals found.</td>
            </tr>
          ) : (
            submittals.map((s) => (
              <tr key={s.id} className="border-b border-slate-100 hover:bg-slate-50">
                <td className="px-4 py-3 text-xs font-mono font-semibold text-slate-500">{s.submittal_number}</td>
                <td className="px-4 py-3 text-sm font-medium text-slate-900 max-w-xs">{s.description}</td>
                <td className="px-4 py-3 text-xs text-slate-500 font-mono">{s.spec_section || '—'}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{s.assigned_gc || '—'}</td>
                <td className="px-4 py-3 text-sm text-center text-slate-600">{s.revision}</td>
                <td className="px-4 py-3">
                  <span className={cn('text-xs px-2 py-1 rounded-full font-medium', STATUS_COLORS[s.status] || 'bg-slate-100 text-slate-600')}>
                    {s.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-slate-600">{formatDate(s.response_due)}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{formatDate(s.returned_date)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
      <div className="px-4 py-2 border-t border-slate-100 text-xs text-slate-400">
        {submittals.length} record{submittals.length !== 1 ? 's' : ''}
      </div>
    </div>
  )
}
