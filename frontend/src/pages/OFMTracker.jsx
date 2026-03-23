import PageHeader from '@/components/layout/PageHeader'
import OFMTable from '@/components/ofm/OFMTable'
import OFMComplianceBar from '@/components/dashboard/OFMComplianceBar'
import { useOFM } from '@/hooks/useOFM'

export default function OFMTracker() {
  const { data: items, isLoading } = useOFM()

  const total = items.length
  const green = items.filter((i) => i.rag_status === 'Green').length
  const pct = total > 0 ? Math.round((green / total) * 100) : 0

  return (
    <div>
      <PageHeader
        title="OFM Tracker"
        subtitle="Owner-Furnished Materials — delivery status"
      />

      <div className="mb-5 max-w-md">
        <OFMComplianceBar pct={pct} />
      </div>

      {isLoading ? (
        <div className="bg-white rounded-xl border shadow-sm p-8 text-center text-slate-400">Loading…</div>
      ) : (
        <OFMTable items={items} />
      )}
    </div>
  )
}
