// API adapter - switch between mock and real backend
// Change this flag to false (or use env var) when backend is ready
const USE_MOCK = false

const api = USE_MOCK
  ? await import('./mock/index.js')
  : await import('./real/index.js')

export const {
  register, loginAdmin, loginTable,
  getMenus, createMenu, updateMenu, deleteMenu, updateMenuOrder,
  setupTable, getTables, completeTableSession,
  createOrder, getOrdersBySession, getOrdersByTable,
  updateOrderStatus, deleteOrder, getOrderHistory,
  subscribeOrders, parseToken
} = api
