import useSWR from 'swr'
import { fetchRFIs } from '@/api/client'

export function useRFIs(params = {}) {
  const key = ['/api/rfis', params]
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchRFIs(params))
  return { data: data ?? [], error, isLoading, mutate }
}
