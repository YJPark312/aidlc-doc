import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

api.interceptors.request.use(config => {
  // Customer pages use table_token, admin pages use admin_token
  const isCustomer = window.location.pathname.startsWith('/customer')
  const token = isCustomer
    ? localStorage.getItem('table_token')
    : localStorage.getItem('admin_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auth
export const register = (storeName, username, password) =>
  api.post('/auth/register', { store_name: storeName, username, password }).then(r => r.data)

export const loginAdmin = (storeName, username, password) =>
  api.post('/auth/login', { store_name: storeName, username, password }).then(r => {
    const payload = parseToken(r.data.access_token)
    return { ...r.data, store_id: payload?.store_id, store_name: storeName }
  })

export const loginTable = (storeId, tableNumber, password) =>
  api.post('/auth/table-login', { store_id: storeId, table_number: tableNumber, password }).then(r => {
    const payload = parseToken(r.data.access_token)
    return { ...r.data, table_id: payload?.table_id, session_id: null, table_number: tableNumber }
  })

// Menu — backend returns flat list, frontend expects categories with nested menus
export async function getMenus(storeId) {
  const [catRes, menuRes] = await Promise.all([
    api.get(`/stores/${storeId}/categories`),
    api.get(`/stores/${storeId}/menus`),
  ])
  const cats = catRes.data
  const menus = menuRes.data
  return cats.map(cat => ({
    ...cat,
    menus: menus.filter(m => m.category_id === cat.id).sort((a, b) => a.sort_order - b.sort_order)
  }))
}

export const createMenu = (storeId, data) => {
  const fd = data instanceof FormData ? data : toFormData(data)
  return api.post(`/stores/${storeId}/menus`, fd).then(r => r.data)
}

export const updateMenu = (menuId, data) => {
  const fd = data instanceof FormData ? data : toFormData(data)
  return api.put(`/menus/${menuId}`, fd).then(r => r.data)
}

export const deleteMenu = (menuId) => api.delete(`/menus/${menuId}`).then(r => r.data)

export const updateMenuOrder = (storeId, items) =>
  api.patch(`/stores/${storeId}/menus/order`, { items }).then(r => r.data)

function toFormData(obj) {
  const fd = new FormData()
  for (const [k, v] of Object.entries(obj)) {
    if (v != null) fd.append(k, v)
  }
  return fd
}

// Table — backend returns simple list, enrich with orders for dashboard
export async function getTables(storeId) {
  const tablesRes = await api.get(`/stores/${storeId}/tables`)
  const tables = tablesRes.data
  const enriched = await Promise.all(tables.map(async (t) => {
    try {
      const orders = await api.get(`/tables/${t.id}/orders`).then(r => r.data)
      const totalAmount = orders.reduce((sum, o) => sum + o.total_amount, 0)
      return { ...t, total_amount: totalAmount, orders: orders.slice(0, 3), session_id: orders[0]?.session_id || null }
    } catch {
      return { ...t, total_amount: 0, orders: [], session_id: null }
    }
  }))
  return enriched
}

export const setupTable = (storeId, tableNumber, password) =>
  api.post(`/stores/${storeId}/tables`, { table_number: tableNumber, password }).then(r => r.data)

export const completeTableSession = (tableId) =>
  api.post(`/tables/${tableId}/complete`).then(r => r.data)

// Order
export const createOrder = (storeId, tableId, sessionId, items) =>
  api.post(`/tables/${tableId}/orders`, { items }).then(r => r.data)

export const getOrdersBySession = (sessionId) =>
  api.get(`/sessions/${sessionId}/orders`).then(r => r.data)

export const getOrdersByTable = (tableId) =>
  api.get(`/tables/${tableId}/orders`).then(r => r.data)

export const updateOrderStatus = (orderId, status) =>
  api.patch(`/orders/${orderId}/status`, { status }).then(r => r.data)

export const deleteOrder = (orderId) =>
  api.delete(`/orders/${orderId}`).then(r => r.data)

export const getOrderHistory = (tableId, dateFilter) =>
  api.get(`/tables/${tableId}/order-history`, { params: dateFilter ? { date: dateFilter } : {} }).then(r => {
    return r.data.map(h => ({ ...h, items: typeof h.items_json === 'string' ? JSON.parse(h.items_json) : h.items_json }))
  })

// SSE — use token in URL query since EventSource doesn't support headers
export function subscribeOrders(storeId, callback) {
  const token = localStorage.getItem('admin_token')
  const url = `/api/v1/stores/${storeId}/orders/stream`
  const es = new EventSource(url)

  es.addEventListener('new_order', (e) => {
    callback({ type: 'new_order', order: JSON.parse(e.data) })
  })
  es.addEventListener('status_change', (e) => {
    callback({ type: 'status_change', ...JSON.parse(e.data) })
  })
  es.addEventListener('order_deleted', (e) => {
    callback({ type: 'order_deleted', ...JSON.parse(e.data) })
  })
  es.addEventListener('table_completed', (e) => {
    callback({ type: 'table_completed', ...JSON.parse(e.data) })
  })
  es.addEventListener('ping', () => {})

  return () => es.close()
}

export function parseToken(token) {
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload))
  } catch { return null }
}
