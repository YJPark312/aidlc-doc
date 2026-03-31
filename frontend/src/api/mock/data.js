// Mock data store - shared mutable state for mock API
let storeIdSeq = 2
let userIdSeq = 2
let tableIdSeq = 4
let sessionIdSeq = 1
let orderIdSeq = 1
let menuIdSeq = 100
let categoryIdSeq = 10

const stores = [
  { id: 1, name: '맛있는식당', created_at: new Date().toISOString() }
]
const users = [
  { id: 1, store_id: 1, username: 'admin', password_hash: '1234', created_at: new Date().toISOString() }
]
const tables = [
  { id: 1, store_id: 1, table_number: 1, password_hash: '1111' },
  { id: 2, store_id: 1, table_number: 2, password_hash: '1111' },
  { id: 3, store_id: 1, table_number: 3, password_hash: '1111' }
]
const sessions = []
const orders = []
const orderItems = []
const orderHistory = []
const categories = []
const menus = []

// Seed data helper
export function seedIfEmpty(storeId) {
  if (categories.some(c => c.store_id === storeId)) return

  const cats = [
    { id: categoryIdSeq++, store_id: storeId, name: '메인 메뉴', sort_order: 0 },
    { id: categoryIdSeq++, store_id: storeId, name: '사이드', sort_order: 1 },
    { id: categoryIdSeq++, store_id: storeId, name: '음료', sort_order: 2 }
  ]
  categories.push(...cats)

  const seedMenus = [
    { name: '불고기 정식', price: 12000, description: '소불고기와 밑반찬 세트', category_id: cats[0].id, image_url: null },
    { name: '김치찌개', price: 9000, description: '돼지고기 김치찌개', category_id: cats[0].id, image_url: null },
    { name: '된장찌개', price: 8000, description: '두부 된장찌개', category_id: cats[0].id, image_url: null },
    { name: '비빔밥', price: 10000, description: '야채 비빔밥', category_id: cats[0].id, image_url: null },
    { name: '계란말이', price: 5000, description: '부드러운 계란말이', category_id: cats[1].id, image_url: null },
    { name: '감자튀김', price: 4000, description: '바삭한 감자튀김', category_id: cats[1].id, image_url: null },
    { name: '콜라', price: 2000, description: '코카콜라 355ml', category_id: cats[2].id, image_url: null },
    { name: '사이다', price: 2000, description: '칠성사이다 355ml', category_id: cats[2].id, image_url: null },
  ]
  seedMenus.forEach((m, i) => {
    menus.push({ id: menuIdSeq++, store_id: storeId, sort_order: i, is_deleted: false, created_at: new Date().toISOString(), ...m })
  })
}

// Auto-seed for pre-loaded store
seedIfEmpty(1)

export {
  stores, users, tables, sessions, orders, orderItems, orderHistory, categories, menus
}

// Sequence incrementors
export function nextStoreId() { return storeIdSeq++ }
export function nextUserId() { return userIdSeq++ }
export function nextTableId() { return tableIdSeq++ }
export function nextSessionId() { return sessionIdSeq++ }
export function nextOrderId() { return orderIdSeq++ }
export function nextMenuId() { return menuIdSeq++ }
export function nextCategoryId() { return categoryIdSeq++ }
