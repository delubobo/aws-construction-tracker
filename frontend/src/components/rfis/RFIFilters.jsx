export default function RFIFilters({ filters, onChange }) {
  const update = (key, value) => onChange({ ...filters, [key]: value || undefined })

  return (
    <div className="flex flex-wrap gap-3 mb-4">
      {/* Status */}
      <select
        value={filters.status || ''}
        onChange={(e) => update('status', e.target.value)}
        className="text-sm border border-slate-200 rounded-lg px-3 py-2 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Statuses</option>
        <option value="Open">Open</option>
        <option value="In Review">In Review</option>
        <option value="Closed">Closed</option>
      </select>

      {/* Priority */}
      <select
        value={filters.priority || ''}
        onChange={(e) => update('priority', e.target.value)}
        className="text-sm border border-slate-200 rounded-lg px-3 py-2 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Priorities</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>

      {/* GC */}
      <select
        value={filters.assigned_gc || ''}
        onChange={(e) => update('assigned_gc', e.target.value)}
        className="text-sm border border-slate-200 rounded-lg px-3 py-2 bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All GCs</option>
        <option value="Turner Construction">Turner Construction</option>
        <option value="Hensel Phelps">Hensel Phelps</option>
        <option value="McCarthy Building Companies">McCarthy Building Companies</option>
      </select>

      {Object.values(filters).some(Boolean) && (
        <button
          onClick={() => onChange({})}
          className="text-sm text-slate-500 hover:text-red-600 px-3 py-2"
        >
          Clear filters
        </button>
      )}
    </div>
  )
}
