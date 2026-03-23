import { useState } from 'react'
import { updateVendor } from '@/api/client'
import { cn } from '@/lib/utils'

const STEPS = [
  { key: 'nda_signed', label: 'NDA Signed' },
  { key: 'orientation_complete', label: 'Orientation' },
  { key: 'badge_issued', label: 'Badge Issued' },
  { key: 'site_access_approved', label: 'Site Access' },
]

export default function VendorChecklist({ vendor, onUpdated }) {
  const [saving, setSaving] = useState(null)

  const completed = STEPS.filter((s) => vendor[s.key]).length
  const pct = Math.round((completed / STEPS.length) * 100)

  const handleToggle = async (key) => {
    setSaving(key)
    try {
      const updated = await updateVendor(vendor.id, { [key]: !vendor[key] })
      onUpdated(updated)
    } finally {
      setSaving(null)
    }
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-semibold text-slate-500">{vendor.onboarding_status}</span>
        <span className="text-xs text-slate-400">{completed}/{STEPS.length}</span>
      </div>
      {/* Progress bar */}
      <div className="w-full bg-slate-100 rounded-full h-1.5 mb-2">
        <div
          className={cn('h-1.5 rounded-full transition-all duration-300', pct === 100 ? 'bg-green-500' : 'bg-blue-500')}
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="flex gap-1 flex-wrap">
        {STEPS.map(({ key, label }) => (
          <button
            key={key}
            disabled={saving === key}
            onClick={() => handleToggle(key)}
            className={cn(
              'text-xs px-2 py-1 rounded-md border font-medium transition-colors',
              vendor[key]
                ? 'bg-green-100 border-green-200 text-green-700'
                : 'bg-slate-50 border-slate-200 text-slate-400 hover:bg-slate-100',
              saving === key && 'opacity-50 cursor-not-allowed'
            )}
          >
            {vendor[key] ? '✓ ' : ''}{label}
          </button>
        ))}
      </div>
    </div>
  )
}
