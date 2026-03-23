import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS = {
  Closed: '#22c55e',
  'In Review': '#f59e0b',
  Open: '#3b82f6',
}

export default function RFIStatusChart({ data }) {
  const chartData = Object.entries(data || {}).map(([name, value]) => ({ name, value }))

  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">RFI Status Breakdown</h3>
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={85}
            paddingAngle={3}
            dataKey="value"
          >
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name] || '#94a3b8'} />
            ))}
          </Pie>
          <Tooltip formatter={(v) => [v, 'RFIs']} />
          <Legend iconType="circle" iconSize={8} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
