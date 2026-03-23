import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Download, FileText, Sheet } from 'lucide-react'
import Sidebar from './Sidebar'
import axios from 'axios'

async function downloadBlob(url, filename) {
  const res = await axios.get(url, { responseType: 'blob' })
  const href = URL.createObjectURL(res.data)
  const a = document.createElement('a')
  a.href = href
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(href)
}

export default function AppShell() {
  const [exporting, setExporting] = useState(null)

  const handleExport = async (type) => {
    setExporting(type)
    try {
      const today = new Date().toISOString().slice(0, 10)
      if (type === 'csv') {
        await downloadBlob('/api/export/csv', `tracker-${today}.csv`)
      } else {
        await downloadBlob('/api/export/pdf', `tracker-${today}.pdf`)
      }
    } finally {
      setExporting(null)
    }
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-auto">
        {/* Top bar with export buttons */}
        <div className="flex items-center justify-end gap-2 px-6 py-3 border-b border-slate-200 bg-white">
          <span className="text-xs text-slate-400 mr-2">Export</span>
          <button
            onClick={() => handleExport('csv')}
            disabled={exporting === 'csv'}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-600 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50"
          >
            <Sheet size={13} />
            {exporting === 'csv' ? 'Exporting…' : 'CSV'}
          </button>
          <button
            onClick={() => handleExport('pdf')}
            disabled={exporting === 'pdf'}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-600 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50"
          >
            <FileText size={13} />
            {exporting === 'pdf' ? 'Generating…' : 'PDF Report'}
          </button>
        </div>
        <main className="flex-1">
          <div className="max-w-7xl mx-auto px-6 py-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
