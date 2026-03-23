import useSWR from 'swr'
import { fetchDashboard } from '@/api/client'

export function useDashboard() {
  const { data, error, isLoading, mutate } = useSWR('/api/dashboard', fetchDashboard, {
    refreshInterval: 30_000,
  })
  return { data, error, isLoading, mutate }
}
