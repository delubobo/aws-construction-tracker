import { useState } from 'react'
import { Plus } from 'lucide-react'
import PageHeader from '@/components/layout/PageHeader'
import CORunningTotal from '@/components/change_orders/CORunningTotal'
import ChangeOrderLog from '@/components/change_orders/ChangeOrderLog'
import COCreateModal from '@/components/change_orders/COCreateModal'
import { useChangeOrders } from '@/hooks/useChangeOrders'

export default function ChangeOrders() {
  const [showModal, setShowModal] = useState(false)
  const { data: cos, isLoading, mutate } = useChangeOrders()

  const pendingValue = cos
    .filter((c) => c.status === 'Pending Approval')
    .reduce((sum, c) => sum + c.cost_impact, 0)
  const totalValue = cos.reduce((sum, c) => sum + c.cost_impact, 0)
  const pendingCount = cos.filter((c) => c.status === 'Pending Approval').length

  const handleCreated = (co) => {
    mutate((current) => [co, ...(current || [])], false)
  }

  return (
    <div>
      <PageHeader
        title="Change Order Log"
        subtitle={`${cos.length} change orders`}
        actions={
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700"
          >
            <Plus size={15} />
            New CO
          </button>
        }
      />

      {!isLoading && (
        <CORunningTotal pendingValue={pendingValue} totalValue={totalValue} count={pendingCount} />
      )}

      {isLoading ? (
        <div className="bg-white rounded-xl border shadow-sm p-8 text-center text-slate-400">Loading…</div>
      ) : (
        <ChangeOrderLog changeOrders={cos} />
      )}

      {showModal && (
        <COCreateModal onClose={() => setShowModal(false)} onCreated={handleCreated} />
      )}
    </div>
  )
}
