import VendorChecklist from './VendorChecklist'

export default function VendorTable({ vendors, onVendorUpdated }) {
  return (
    <div className="bg-white rounded-xl border shadow-sm overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            {['Company', 'Contact', 'Trade', 'Email', 'Onboarding Progress'].map((h) => (
              <th key={h} className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {vendors.length === 0 ? (
            <tr>
              <td colSpan={5} className="px-4 py-8 text-center text-slate-400 text-sm">No vendors found.</td>
            </tr>
          ) : (
            vendors.map((v) => (
              <tr key={v.id} className="border-b border-slate-100 hover:bg-slate-50 align-top">
                <td className="px-4 py-4 text-sm font-semibold text-slate-900">{v.company_name}</td>
                <td className="px-4 py-4 text-sm text-slate-600">{v.contact_name || '—'}</td>
                <td className="px-4 py-4 text-sm text-slate-600">{v.trade || '—'}</td>
                <td className="px-4 py-4 text-xs text-slate-500">{v.contact_email || '—'}</td>
                <td className="px-4 py-4 min-w-[260px]">
                  <VendorChecklist vendor={v} onUpdated={onVendorUpdated} />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
