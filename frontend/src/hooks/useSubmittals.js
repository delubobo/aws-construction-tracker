import useSWR from 'swr'
import { fetchSubmittals } from '@/api/client'

export function useSubmittals(params = {}) {
  const key = ['/api/submittals', params]
  const { data, error, isLoading, mutate } = useSWR(key, () => fetchSubmittals(params))
  return { data: data ?? [], error, isLoading, mutate }
}
