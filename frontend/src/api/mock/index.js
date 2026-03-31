import {
  stores, users, tables, sessions, orders, orderItems, orderHistory, categories, menus,
  seedIfEmpty, nextStoreId, nextUserId, nextTableId, nextSessionId, nextOrderId, nextMenuId, nextCategoryId
} from './data.js'
import { sseManager } from './sse.js'

function delay(ms = 100) { return new Promise(r => setTimeout(r, ms)) }
function makeToken(payload) { return btoa(JSON.stringify(payload)) }
function parseToken(token) { try { return JSON.parse(atob(token)) } catch { return null } }

// ── Auth ──
export async function register(storeName, username, password) {
  await delay()
  if (stores.find(s => s.name === storeName)) throw { response: { status: 409, data: { detail: '이미 존재하는 매장명입니다' } } }
  const store = { id: nextStoreId(), name: storeName, created_at: new Date().toISOString() }
  stores.push(store)
  const user = { id: nextUserId(), store_id: store.id, username, password_hash: password, created_at: new Date().toISOString() }
  users.push(user)
  seedIfEmpty(store.id)
  return { user: { id: user.id, username }, store: { id: store.id, name: store.name } }
}

export async function loginAdmin(storeName, username, password) {
  await delay()
  const store = stores.find(s => s.name === storeName)
  if (!store) throw { response: { status: 401, data: { detail: '매장을 찾을 수 없습니다' } } }
  const user = users.find(u => u.store_id === store.id && u.username === username && u.password_hash === password)
  if (!user) throw { response: { status: 401, data: { detail: '인증 정보가 올바르지 않습니다' } } }
  return { access_token: makeToken({ user_id: user.id, store_id: store.id, role: 'admin' }), store_id: store.id, store_name: store.name }
}

export async function loginTable(storeId, tableNumber, password) {
  await delay()
  const t = tables.find(t => t.store_id === storeId && t.table_number === tableNumber && t.password_hash === password)
  if (!t) throw { response: { status: 401, data: { detail: '테이블 인증 실패' } } }
  const activeSession = sessions.find(s => s.table_id === t.id && s.is_active)
  return { access_token: makeToken({ table_id: t.id, store_id: storeId, role: 'table', table_number: tableNumber }), table_id: t.id, session_id: activeSession?.id || null }
}

// ── Menu ──
export async function getMenus(storeId) {
  await delay()
  seedIfEmpty(storeId)
  const cats = categories.filter(c => c.store_id === storeId).sort((a, b) => a.sort_order - b.sort_order)
  return cats.map(cat => ({
    ...cat,
    menus: menus.filter(m => m.category_id === cat.id && !m.is_deleted && m.store_id === storeId).sort((a, b) => a.sort_order - b.sort_order)
  }))
}

export async function createMenu(storeId, data) {
  await delay()
  const menu = { id: nextMenuId(), store_id: storeId, is_deleted: false, sort_order: menus.length, created_at: new Date().toISOString(), ...data }
  menus.push(menu)
  return menu
}

export async function updateMenu(menuId, data) {
  await delay()
  const menu = menus.find(m => m.id === menuId && !m.is_deleted)
  if (!menu) throw { response: { status: 404, data: { detail: '메뉴를 찾을 수 없습니다' } } }
  Object.assign(menu, data)
  return menu
}

export async function deleteMenu(menuId) {
  await delay()
  const menu = menus.find(m => m.id === menuId)
  if (!menu) throw { response: { status: 404, data: { detail: '메뉴를 찾을 수 없습니다' } } }
  menu.is_deleted = true
}

export async function updateMenuOrder(storeId, menuOrders) {
  await delay()
  menuOrders.forEach(({ menu_id, sort_order }) => {
    const m = menus.find(m => m.id === menu_id && m.store_id === storeId)
    if (m) m.sort_order = sort_order
  })
}

// ── Table ──
export async function setupTable(storeId, tableNumber, password) {
  await delay()
  if (tables.find(t => t.store_id === storeId && t.table_number === tableNumber))
    throw { response: { status: 409, data: { detail: '이미 존재하는 테이블 번호입니다' } } }
  const t = { id: nextTableId(), store_id: storeId, table_number: tableNumber, password_hash: password }
  tables.push(t)
  return t
}

export async function getTables(storeId) {
  await delay()
  return tables.filter(t => t.store_id === storeId).map(t => {
    const activeSession = sessions.find(s => s.table_id === t.id && s.is_active)
    const tableOrders = activeSession ? orders.filter(o => o.session_id === activeSession.id) : []
    const totalAmount = tableOrders.reduce((sum, o) => sum + o.total_amount, 0)
    return { ...t, session_id: activeSession?.id || null, total_amount: totalAmount, orders: tableOrders.slice(-3).reverse() }
  })
}

export async function completeTableSession(tableId) {
  await delay()
  const session = sessions.find(s => s.table_id === tableId && s.is_active)
  if (!session) throw { response: { status: 404, data: { detail: '활성 세션이 없습니다' } } }
  const now = new Date().toISOString()
  const sessionOrders = orders.filter(o => o.session_id === session.id)
  sessionOrders.forEach(o => {
    const items = orderItems.filter(i => i.order_id === o.id)
    orderHistory.push({
      id: orderHistory.length + 1, order_id: o.id, store_id: o.store_id, table_id: o.table_id,
      session_id: o.session_id, status: 'completed', total_amount: o.total_amount,
      order_created_at: o.created_at, completed_at: now, items_json: JSON.stringify(items)
    })
  })
  // Remove orders and items
  sessionOrders.forEach(o => {
    const idx = orders.indexOf(o)
    if (idx >= 0) orders.splice(idx, 1)
    for (let i = orderItems.length - 1; i >= 0; i--) {
      if (orderItems[i].order_id === o.id) orderItems.splice(i, 1)
    }
  })
  session.is_active = false
  session.completed_at = now
  const table = tables.find(t => t.id === tableId)
  sseManager.emit(table.store_id, { type: 'table_completed', table_id: tableId })
}

// ── Order ──
export async function createOrder(storeId, tableId, sessionId, items) {
  await delay()
  if (!items?.length) throw { response: { status: 400, data: { detail: '주문 항목이 비어있습니다' } } }
  let sid = sessionId
  if (!sid || !sessions.find(s => s.id === sid && s.is_active)) {
    const newSession = { id: nextSessionId(), table_id: tableId, started_at: new Date().toISOString(), completed_at: null, is_active: true }
    sessions.push(newSession)
    sid = newSession.id
  }
  const orderId = nextOrderId()
  let totalAmount = 0
  const createdItems = items.map(item => {
    const menu = menus.find(m => m.id === item.menu_id && !m.is_deleted)
    if (!menu) throw { response: { status: 400, data: { detail: `메뉴 ID ${item.menu_id}를 찾을 수 없습니다` } } }
    const subtotal = menu.price * item.quantity
    totalAmount += subtotal
    const oi = { id: orderItems.length + 1, order_id: orderId, menu_id: menu.id, menu_name: menu.name, menu_price: menu.price, quantity: item.quantity, subtotal }
    orderItems.push(oi)
    return oi
  })
  const order = { id: orderId, store_id: storeId, table_id: tableId, session_id: sid, status: 'pending', total_amount: totalAmount, created_at: new Date().toISOString(), items: createdItems }
  orders.push(order)
  sseManager.emit(storeId, { type: 'new_order', order })
  return { ...order, session_id: sid }
}

export async function getOrdersBySession(sessionId) {
  await delay()
  return orders.filter(o => o.session_id === sessionId).map(o => ({
    ...o, items: orderItems.filter(i => i.order_id === o.id)
  })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
}

export async function getOrdersByTable(tableId) {
  await delay()
  const activeSession = sessions.find(s => s.table_id === tableId && s.is_active)
  if (!activeSession) return []
  return orders.filter(o => o.session_id === activeSession.id).map(o => ({
    ...o, items: orderItems.filter(i => i.order_id === o.id)
  })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
}

export async function updateOrderStatus(orderId, status) {
  await delay()
  const order = orders.find(o => o.id === orderId)
  if (!order) throw { response: { status: 404, data: { detail: '주문을 찾을 수 없습니다' } } }
  order.status = status
  sseManager.emit(order.store_id, { type: 'status_change', order_id: orderId, status })
  return order
}

export async function deleteOrder(orderId) {
  await delay()
  const idx = orders.findIndex(o => o.id === orderId)
  if (idx < 0) throw { response: { status: 404, data: { detail: '주문을 찾을 수 없습니다' } } }
  const order = orders[idx]
  orders.splice(idx, 1)
  for (let i = orderItems.length - 1; i >= 0; i--) {
    if (orderItems[i].order_id === orderId) orderItems.splice(i, 1)
  }
  sseManager.emit(order.store_id, { type: 'order_deleted', order_id: orderId })
}

export async function getOrderHistory(tableId, dateFilter) {
  await delay()
  let history = orderHistory.filter(h => h.table_id === tableId)
  if (dateFilter) {
    history = history.filter(h => h.completed_at.startsWith(dateFilter))
  }
  return history.sort((a, b) => new Date(b.completed_at) - new Date(a.completed_at))
    .map(h => ({ ...h, items: JSON.parse(h.items_json) }))
}

export function subscribeOrders(storeId, callback) {
  return sseManager.subscribe(storeId, callback)
}

export { parseToken }
