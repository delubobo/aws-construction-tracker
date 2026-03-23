import { useState } from 'react'
import { createSubmittal } from '@/api/client'

const EMPTY = {
  description: '',
  spec_section: '',
  assigned_gc: '',
  reviewer: 'R. Lan (Project Engineer)',
  submitted_date: new Date().toISOString().slice(0, 10),
  response_due: '',
  status: 'Pending',
  revision: 1,
}

export default function SubmittalCreateModal({ onClose, onCreated }) {
  const [form, setForm] = useState(EMPTY)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const set = (key, value) => setForm((f) => ({ ...f, [key]: value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.description.trim()) return setError('Description is required.')
    setSaving(true)
    setError(null)
    try {
      const sub = await createSubmittal({
        ...form,
        assigned_gc: form.assigned_gc || undefined,
        response_due: form.response_due || undefined,
        spec_section: form.spec_section || undefined,
        revision: parseInt(form.revision) || 1,
      })
      onCreated(sub)
      onClose()
    } catch {
      setError('Failed to create submittal.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg mx-4 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-900">New Submittal</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 text-xl leading-none">&times;</button>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-4">
          {error && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</div>
          )}
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1">Description *</label>
            <input required value={form.description} onChange={(e) => set('description', e.target.value)}
              className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Submittal description…" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Spec Section</label>
              <input value={form.spec_section} onChange={(e) => set('spec_section', e.target.value)}
                placeholder="03 30 00"
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Revision</label>
              <input type="number" min="1" value={form.revision} onChange={(e) => set('revision', e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1">Assigned GC</label>
            <select value={form.assigned_gc} onChange={(e) => set('assigned_gc', e.target.value)}
              className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="">— Select —</option>
              <option>Turner Construction</option>
              <option>Hensel Phelps</option>
              <option>McCarthy Building Companies</option>
            </select>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Submit Date</label>
              <input type="date" value={form.submitted_date} onChange={(e) => set('submitted_date', e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">Response Due</label>
              <input type="date" value={form.response_due} onChange={(e) => set('response_due', e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-slate-600 hover:text-slate-800">Cancel</button>
            <button type="submit" disabled={saving}
              className="px-5 py-2 text-sm font-semibold bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {saving ? 'Creating…' : 'Create Submittal'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
