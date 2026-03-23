import { useState } from 'react'
import { Plus } from 'lucide-react'
import PageHeader from '@/components/layout/PageHeader'
import SubmittalTable from '@/components/submittals/SubmittalTable'
import SubmittalCreateModal from '@/components/submittals/SubmittalCreateModal'
import { useSubmittals } from '@/hooks/useSubmittals'

export default function Submittals() {
  const [showModal, setShowModal] = useState(false)
  const [statusFilter, setStatusFilter] = useState('')
  const { data: submittals, isLoading, mutate } = useSubmittals(
    statusFilter ? { status: statusFilter } : {}
  )

  const handleCreated = (sub) => {
    mutate((current) => [sub, ...(current || [])], false)
  }

  return (
    <div>
      <PageHeader
        title="Submittal Register"
        subtitle={`${submittals.length} records`}
        actions={
          <div className="flex items-center gap-3">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="text-sm border border-slate-200 rounded-lg px-3 py-2 bg-white focus:outline-none"
            >
              <option value="">All Statuses</option>
              <option>Pending</option>
              <option>Approved</option>
              <option>Rejected</option>
              <option>Revise & Resubmit</option>
            </select>
            <button
              onClick={() => setShowModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700"
            >
              <Plus size={15} />
              New Submittal
            </button>
          </div>
        }
      />

      {isLoading ? (
        <div className="bg-white rounded-xl border shadow-sm p-8 text-center text-slate-400">Loading…</div>
      ) : (
        <SubmittalTable submittals={submittals} />
      )}

      {showModal && (
        <SubmittalCreateModal onClose={() => setShowModal(false)} onCreated={handleCreated} />
      )}
    </div>
  )
}
