import { useState } from 'react'
import { updateRFI } from '@/api/client'
import { formatDate, isOverdue, cn } from '@/lib/utils'

const STATUS_COLORS = {
  Open: 'bg-blue-100 text-blue-700',
  'In Review': 'bg-amber-100 text-amber-700',
  Closed: 'bg-green-100 text-green-700',
}

const PRIORITY_COLORS = {
  High: 'bg-red-100 text-red-700',
  Medium: 'bg-slate-100 text-slate-600',
  Low: 'bg-slate-50 text-slate-400',
}

export default function RFIRow({ rfi, onUpdated }) {
  const [editingStatus, setEditingStatus] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleStatusChange = async (newStatus) => {
    setSaving(true)
    try {
      const updated = await updateRFI(rfi.id, {
        status: newStatus,
        closed_date: newStatus === 'Closed' ? new Date().toISOString().slice(0, 10) : null,
      })
      onUpdated(updated)
    } finally {
      setSaving(false)
      setEditingStatus(false)
    }
  }

  const overdue = isOverdue(rfi.due_date) && rfi.status !== 'Closed'

  return (
    <tr className={cn('border-b border-slate-100 hover:bg-slate-50 transition-colors', overdue && 'bg-red-50 hover:bg-red-50')}>
      <td className="px-4 py-3 text-xs font-mono font-semibold text-slate-500">{rfi.rfi_number}</td>
      <td className="px-4 py-3">
        <div className="text-sm font-medium text-slate-900">{rfi.title}</div>
        {rfi.spec_section && (
          <div className="text-xs text-slate-400 mt-0.5">Spec {rfi.spec_section}</div>
        )}
      </td>
      <td className="px-4 py-3">
        {editingStatus ? (
          <select
            autoFocus
            disabled={saving}
            defaultValue={rfi.status}
            onChange={(e) => handleStatusChange(e.target.value)}
            onBlur={() => setEditingStatus(false)}
            className="text-xs border border-blue-400 rounded px-2 py-1 bg-white focus:outline-none"
          >
            <option value="Open">Open</option>
            <option value="In Review">In Review</option>
            <option value="Closed">Closed</option>
          </select>
        ) : (
          <button
            onClick={() => setEditingStatus(true)}
            title="Click to change status"
            className={cn(
              'text-xs px-2 py-1 rounded-full font-medium cursor-pointer hover:opacity-80',
              STATUS_COLORS[rfi.status] || 'bg-slate-100 text-slate-600'
            )}
          >
            {rfi.status}
          </button>
        )}
      </td>
      <td className="px-4 py-3">
        <span className={cn('text-xs px-2 py-1 rounded-full font-medium', PRIORITY_COLORS[rfi.priority] || '')}>
          {rfi.priority}
        </span>
      </td>
      <td className="px-4 py-3 text-sm text-slate-600">{rfi.assigned_gc || '—'}</td>
      <td className="px-4 py-3 text-sm text-slate-600">{formatDate(rfi.submitted_date)}</td>
      <td className={cn('px-4 py-3 text-sm', overdue ? 'text-red-600 font-semibold' : 'text-slate-600')}>
        {formatDate(rfi.due_date)}
        {overdue && <span className="ml-1 text-xs">(overdue)</span>}
      </td>
    </tr>
  )
}
