import useSWR from 'swr'
import { fetchVendors } from '@/api/client'

export function useVendors(params = {}) {
  const key = ['/api/vendors', params]
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchVendors(params))
  return { data: data ?? [], error, isLoading, mutate }
}
