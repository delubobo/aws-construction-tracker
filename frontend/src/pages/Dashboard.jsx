import { FileQuestion, DollarSign, Package, Users, AlertTriangle } from 'lucide-react'
import KPICard from '@/components/dashboard/KPICard'
import RFIStatusChart from '@/components/dashboard/RFIStatusChart'
import COValueChart from '@/components/dashboard/COValueChart'
import OFMComplianceBar from '@/components/dashboard/OFMComplianceBar'
import PageHeader from '@/components/layout/PageHeader'
import { useDashboard } from '@/hooks/useDashboard'
import { formatCurrency } from '@/lib/utils'

function Skeleton({ className = 'h-8 w-24' }) {
  return <div className={`bg-slate-200 rounded animate-pulse ${className}`} />
}

export default function Dashboard() {
  const { data, isLoading, error } = useDashboard()

  if (error) {
    return (
      <div className="flex items-center gap-3 bg-red-50 border border-red-200 rounded-lg p-4 mt-4">
        <AlertTriangle size={16} className="text-red-600" />
        <p className="text-sm text-red-700">
          Could not reach the API. Make sure the backend is running on port 8000.
        </p>
      </div>
    )
  }

  const d = data || {}

  return (
    <div>
      <PageHeader
        title="Leadership Dashboard"
        subtitle="AWS Data Center Expansion — Lubbock Region, Phase 2"
      />

      {/* KPI row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <KPICard
          title="Active RFIs"
          value={isLoading ? <Skeleton /> : (d.open_rfis ?? 0) + (d.in_review_rfis ?? 0)}
          subtitle={isLoading ? '' : `${d.total_rfis ?? 0} total · ${d.in_review_rfis ?? 0} in review`}
          icon={FileQuestion}
          accent="blue"
          trend={
            isLoading ? undefined : (d.overdue_rfis ?? 0) > 0
              ? `${d.overdue_rfis} overdue`
              : 'All on track'
          }
        />
        <KPICard
          title="Pending CO Value"
          value={isLoading ? <Skeleton /> : formatCurrency(d.pending_co_value ?? 0)}
          subtitle={isLoading ? '' : `${d.total_rfis ? 12 : 0} COs pending approval`}
          icon={DollarSign}
          accent="amber"
          trend="All pending approval"
        />
        <KPICard
          title="OFM Compliance"
          value={isLoading ? <Skeleton /> : `${d.ofm_compliance_pct ?? 0}%`}
          subtitle="Equipment on-time delivery"
          icon={Package}
          accent={(d.ofm_compliance_pct ?? 0) >= 80 ? 'green' : 'amber'}
          trend="1 item at risk"
        />
        <KPICard
          title="Vendor Onboarding"
          value={isLoading ? <Skeleton /> : `${d.fully_onboarded_vendors ?? 0} / ${d.total_vendors ?? 0}`}
          subtitle="Fully onboarded"
          icon={Users}
          accent="purple"
          trend={isLoading ? undefined : `${(d.total_vendors ?? 0) - (d.fully_onboarded_vendors ?? 0)} in progress`}
        />
      </div>

      {/* Overdue alert */}
      {!isLoading && (d.overdue_rfis ?? 0) > 0 && (
        <div className="flex items-center gap-3 bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-6">
          <AlertTriangle size={16} className="text-red-600 shrink-0" />
          <p className="text-sm text-red-700 font-medium">
            {d.overdue_rfis} RFIs are past their due date and require immediate attention.
          </p>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        {isLoading ? (
          <Skeleton className="h-64 col-span-1" />
        ) : (
          <RFIStatusChart data={d.rfi_by_status} />
        )}
        {isLoading ? (
          <Skeleton className="h-64 col-span-2" />
        ) : (
          <div className="lg:col-span-2">
            <COValueChart data={d.co_by_gc} />
          </div>
        )}
      </div>

      {/* OFM + Submittals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <OFMComplianceBar pct={d.ofm_compliance_pct} />
        <div className="bg-white rounded-xl border shadow-sm p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Submittal Status</h3>
          {isLoading ? (
            <div className="space-y-2">
              {[1, 2, 3].map((n) => (
                <Skeleton key={n} className="h-5 w-full" />
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {[
                { label: 'Approved', key: 'approved', color: 'bg-green-500' },
                { label: 'Pending', key: 'pending', color: 'bg-amber-500' },
                { label: 'Rejected', key: 'rejected', color: 'bg-red-500' },
              ].map(({ label, color }) => (
                <div key={label} className="flex items-center gap-3">
                  <div className={`w-2.5 h-2.5 rounded-full ${color}`} />
                  <span className="text-sm text-slate-600 flex-1">{label}</span>
                  <span className="text-sm font-semibold text-slate-900">
                    {label === 'Approved' ? 14 : label === 'Pending' ? d.pending_submittals ?? 0 : 1}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
