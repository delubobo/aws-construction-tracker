import { useState } from 'react'
import { Plus } from 'lucide-react'
import PageHeader from '@/components/layout/PageHeader'
import RFIFilters from '@/components/rfis/RFIFilters'
import RFITable from '@/components/rfis/RFITable'
import RFICreateModal from '@/components/rfis/RFICreateModal'
import { useRFIs } from '@/hooks/useRFIs'

export default function RFIs() {
  const [filters, setFilters] = useState({})
  const [sortBy, setSortBy] = useState('submitted_date')
  const [sortDir, setSortDir] = useState('desc')
  const [showModal, setShowModal] = useState(false)

  const { data: rfis, isLoading, mutate } = useRFIs({
    ...filters,
    sort_by: sortBy,
    sort_dir: sortDir,
  })

  const handleSort = (col) => {
    if (sortBy === col) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortBy(col)
      setSortDir('desc')
    }
  }

  const handleRFIUpdated = (updated) => {
    mutate((current) => current.map((r) => (r.id === updated.id ? updated : r)), false)
  }

  const handleRFICreated = (newRFI) => {
    mutate((current) => [newRFI, ...(current || [])], false)
  }

  const activeCount = rfis.filter((r) => r.status === 'Open' || r.status === 'In Review').length

  return (
    <div>
      <PageHeader
        title="RFI Register"
        subtitle={`${rfis.length} records${activeCount ? ` · ${activeCount} active` : ''}`}
        actions={
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700"
          >
            <Plus size={15} />
            New RFI
          </button>
        }
      />

      <RFIFilters filters={filters} onChange={setFilters} />

      {isLoading ? (
        <div className="bg-white rounded-xl border shadow-sm p-8 text-center text-slate-400">
          Loading…
        </div>
      ) : (
        <RFITable
          rfis={rfis}
          onRFIUpdated={handleRFIUpdated}
          sortBy={sortBy}
          sortDir={sortDir}
          onSort={handleSort}
        />
      )}

      {showModal && (
        <RFICreateModal
          onClose={() => setShowModal(false)}
          onCreated={handleRFICreated}
        />
      )}
    </div>
  )
}
