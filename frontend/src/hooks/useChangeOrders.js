import useSWR from 'swr'
import { fetchChangeOrders } from '@/api/client'

export function useChangeOrders(params = {}) {
  const key = ['/api/change-orders', params]
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchChangeOrders(params))
  return { data: data ?? [], error, isLoading, mutate }
}
