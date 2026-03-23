import { cn } from '@/lib/utils'

const RAG = {
  Green: { dot: 'bg-green-500', badge: 'bg-green-100 text-green-700', label: 'Green' },
  Amber: { dot: 'bg-amber-500', badge: 'bg-amber-100 text-amber-700', label: 'Amber' },
  Red: { dot: 'bg-red-500', badge: 'bg-red-100 text-red-700', label: 'Red' },
}

export default function OFMStatusBadge({ status }) {
  const cfg = RAG[status] || RAG.Green
  return (
    <span className={cn('inline-flex items-center gap-1.5 text-xs px-2 py-1 rounded-full font-medium', cfg.badge)}>
      <span className={cn('w-2 h-2 rounded-full', cfg.dot)} />
      {cfg.label}
    </span>
  )
}
