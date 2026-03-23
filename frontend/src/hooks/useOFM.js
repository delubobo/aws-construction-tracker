import useSWR from 'swr'
import { fetchOFM } from '@/api/client'

export function useOFM(params = {}) {
  const key = ['/api/ofm', params]
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchOFM(params))
  return { data: data ?? [], error, isLoading, mutate }
}
