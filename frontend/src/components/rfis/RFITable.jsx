import { useState } from 'react'
import { ChevronUp, ChevronDown } from 'lucide-react'
import RFIRow from './RFIRow'
import { cn } from '@/lib/utils'

const COLUMNS = [
  { key: 'rfi_number', label: 'Number', sortable: true },
  { key: 'title', label: 'Title', sortable: false },
  { key: 'status', label: 'Status', sortable: true },
  { key: 'priority', label: 'Priority', sortable: true },
  { key: 'assigned_gc', label: 'GC', sortable: true },
  { key: 'submitted_date', label: 'Submitted', sortable: true },
  { key: 'due_date', label: 'Due Date', sortable: true },
]

export default function RFITable({ rfis, onRFIUpdated, sortBy, sortDir, onSort }) {
  const renderSortIcon = (col) => {
    if (!col.sortable) return null
    if (sortBy !== col.key) return <ChevronUp size={12} className="text-slate-300 ml-1" />
    return sortDir === 'asc'
      ? <ChevronUp size={12} className="text-blue-600 ml-1" />
      : <ChevronDown size={12} className="text-blue-600 ml-1" />
  }

  return (
    <div className="bg-white rounded-xl border shadow-sm overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            {COLUMNS.map((col) => (
              <th
                key={col.key}
                onClick={() => col.sortable && onSort(col.key)}
                className={cn(
                  'px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide select-none',
                  col.sortable && 'cursor-pointer hover:text-slate-700'
                )}
              >
                <span className="inline-flex items-center">
                  {col.label}
                  {renderSortIcon(col)}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rfis.length === 0 ? (
            <tr>
              <td colSpan={7} className="px-4 py-8 text-center text-slate-400 text-sm">
                No RFIs match the current filters.
              </td>
            </tr>
          ) : (
            rfis.map((rfi) => (
              <RFIRow key={rfi.id} rfi={rfi} onUpdated={onRFIUpdated} />
            ))
          )}
        </tbody>
      </table>
      <div className="px-4 py-2 border-t border-slate-100 text-xs text-slate-400">
        {rfis.length} record{rfis.length !== 1 ? 's' : ''}
      </div>
    </div>
  )
}
