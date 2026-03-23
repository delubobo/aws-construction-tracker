import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { formatCurrency } from '@/lib/utils'

export default function COValueChart({ data }) {
  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Change Order Value by GC</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data || []} margin={{ top: 4, right: 8, left: 8, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey="gc" tick={{ fontSize: 11 }} />
          <YAxis
            tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
            tick={{ fontSize: 11 }}
            width={55}
          />
          <Tooltip formatter={(v) => [formatCurrency(v), 'CO Value']} />
          <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
