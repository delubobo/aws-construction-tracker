import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: { 'Content-Type': 'application/json' },
})

// --- Dashboard ---
export const fetchDashboard = () => api.get('/api/dashboard').then((r) => r.data)

// --- RFIs ---
export const fetchRFIs = (params = {}) =>
  api.get('/api/rfis', { params }).then((r) => r.data)
export const createRFI = (data) => api.post('/api/rfis', data).then((r) => r.data)
export const updateRFI = (id, data) =>
  api.patch(`/api/rfis/${id}`, data).then((r) => r.data)
export const deleteRFI = (id) => api.delete(`/api/rfis/${id}`)

// --- Submittals ---
export const fetchSubmittals = (params = {}) =>
  api.get('/api/submittals', { params }).then((r) => r.data)
export const createSubmittal = (data) =>
  api.post('/api/submittals', data).then((r) => r.data)
export const updateSubmittal = (id, data) =>
  api.patch(`/api/submittals/${id}`, data).then((r) => r.data)

// --- Change Orders ---
export const fetchChangeOrders = (params = {}) =>
  api.get('/api/change-orders', { params }).then((r) => r.data)
export const createChangeOrder = (data) =>
  api.post('/api/change-orders', data).then((r) => r.data)
export const updateChangeOrder = (id, data) =>
  api.patch(`/api/change-orders/${id}`, data).then((r) => r.data)

// --- OFM ---
export const fetchOFM = (params = {}) =>
  api.get('/api/ofm', { params }).then((r) => r.data)
export const createOFMItem = (data) => api.post('/api/ofm', data).then((r) => r.data)
export const updateOFMItem = (id, data) =>
  api.patch(`/api/ofm/${id}`, data).then((r) => r.data)

// --- Vendors ---
export const fetchVendors = (params = {}) =>
  api.get('/api/vendors', { params }).then((r) => r.data)
export const createVendor = (data) =>
  api.post('/api/vendors', data).then((r) => r.data)
export const updateVendor = (id, data) =>
  api.patch(`/api/vendors/${id}`, data).then((r) => r.data)
