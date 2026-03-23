import { cn } from '@/lib/utils'

export default function KPICard({ title, value, subtitle, icon: Icon, accent = 'blue', trend }) {
  const accentMap = {
    blue: 'bg-blue-50 text-blue-700 border-blue-100',
    amber: 'bg-amber-50 text-amber-700 border-amber-100',
    red: 'bg-red-50 text-red-700 border-red-100',
    green: 'bg-green-50 text-green-700 border-green-100',
    purple: 'bg-purple-50 text-purple-700 border-purple-100',
  }

  const iconBgMap = {
    blue: 'bg-blue-100 text-blue-600',
    amber: 'bg-amber-100 text-amber-600',
    red: 'bg-red-100 text-red-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
  }

  return (
    <div
      className={cn(
        'rounded-xl border p-5 bg-white shadow-sm flex flex-col gap-3',
        'hover:shadow-md transition-shadow'
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">{title}</p>
          <p className="text-3xl font-bold text-slate-900 mt-1">{value}</p>
          {subtitle && <p className="text-sm text-slate-500 mt-0.5">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={cn('p-2.5 rounded-lg', iconBgMap[accent])}>
            <Icon size={20} />
          </div>
        )}
      </div>
      {trend && (
        <div className={cn('text-xs px-2 py-1 rounded-full border w-fit font-medium', accentMap[accent])}>
          {trend}
        </div>
      )}
    </div>
  )
}
