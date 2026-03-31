import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

api.interceptors.request.use(config => {
  const adminToken = localStorage.getItem('admin_token')
  const tableToken = localStorage.getItem('table_token')
  const token = adminToken || tableToken
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auth
export const register = (storeName, username, password) =>
  api.post('/auth/register', { store_name: storeName, username, password }).then(r => r.data)
export const loginAdmin = (storeName, username, password) =>
  api.post('/auth/login', { store_name: storeName, username, password }).then(r => r.data)
export const loginTable = (storeId, tableNumber, password) =>
  api.post('/auth/table-login', { store_id: storeId, table_number: tableNumber, password }).then(r => r.data)

// Menu
export const getMenus = (storeId) => api.get(`/stores/${storeId}/menus`).then(r => r.data)
export const createMenu = (storeId, data) => api.post(`/stores/${storeId}/menus`, data).then(r => r.data)
export const updateMenu = (menuId, data) => api.put(`/menus/${menuId}`, data).then(r => r.data)
export const deleteMenu = (menuId) => api.delete(`/menus/${menuId}`).then(r => r.data)
export const updateMenuOrder = (storeId, menuOrders) => api.patch(`/stores/${storeId}/menus/order`, menuOrders).then(r => r.data)

// Table
export const setupTable = (storeId, tableNumber, password) =>
  api.post(`/stores/${storeId}/tables`, { table_number: tableNumber, password }).then(r => r.data)
export const getTables = (storeId) => api.get(`/stores/${storeId}/tables`).then(r => r.data)
export const completeTableSession = (tableId) => api.post(`/tables/${tableId}/complete`).then(r => r.data)

// Order
export const createOrder = (storeId, tableId, sessionId, items) =>
  api.post(`/tables/${tableId}/orders`, { store_id: storeId, session_id: sessionId, items }).then(r => r.data)
export const getOrdersBySession = (sessionId) => api.get(`/sessions/${sessionId}/orders`).then(r => r.data)
export const getOrdersByTable = (tableId) => api.get(`/tables/${tableId}/orders`).then(r => r.data)
export const updateOrderStatus = (orderId, status) => api.patch(`/orders/${orderId}/status`, { status }).then(r => r.data)
export const deleteOrder = (orderId) => api.delete(`/orders/${orderId}`).then(r => r.data)
export const getOrderHistory = (tableId, dateFilter) =>
  api.get(`/tables/${tableId}/order-history`, { params: dateFilter ? { date: dateFilter } : {} }).then(r => r.data)

// SSE
export function subscribeOrders(storeId, callback) {
  const es = new EventSource(`/api/v1/stores/${storeId}/orders/stream`)
  es.onmessage = (e) => callback(JSON.parse(e.data))
  return () => es.close()
}

export function parseToken(token) {
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload))
  } catch { return null }
}
