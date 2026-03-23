import PageHeader from '@/components/layout/PageHeader'
import VendorTable from '@/components/vendors/VendorTable'
import { useVendors } from '@/hooks/useVendors'

export default function Vendors() {
  const { data: vendors, isLoading, mutate } = useVendors()

  const fullyOnboarded = vendors.filter((v) => v.onboarding_status === 'Fully Onboarded').length

  const handleVendorUpdated = (updated) => {
    mutate((current) => current.map((v) => (v.id === updated.id ? updated : v)), false)
  }

  return (
    <div>
      <PageHeader
        title="Vendor Onboarding"
        subtitle={`${fullyOnboarded} of ${vendors.length} fully onboarded`}
      />

      {isLoading ? (
        <div className="bg-white rounded-xl border shadow-sm p-8 text-center text-slate-400">Loading…</div>
      ) : (
        <VendorTable vendors={vendors} onVendorUpdated={handleVendorUpdated} />
      )}
    </div>
  )
}
