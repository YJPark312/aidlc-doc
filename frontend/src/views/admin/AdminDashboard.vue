<template>
  <div class="dashboard">
    <header class="top-bar">
      <span class="title">📊 주문 대시보드 — {{ storeName }}</span>
      <nav class="nav-links">
        <router-link to="/admin/menus">메뉴관리</router-link>
        <router-link to="/admin/tables">테이블관리</router-link>
        <button @click="logout" class="logout-btn">로그아웃</button>
      </nav>
    </header>

    <div class="table-grid">
      <div v-for="t in tableList" :key="t.id" class="table-card" :class="{ 'has-orders': t.orders.length }">
        <div class="table-header">
          <span class="table-num">테이블 {{ t.table_number }}</span>
          <span class="table-total">{{ t.total_amount.toLocaleString() }}원</span>
        </div>
        <div class="table-orders">
          <div v-for="order in t.orders" :key="order.id" class="mini-order" :class="[order.status, { 'new-order': isNew(order) }]">
            <span>#{{ order.id }} — {{ order.total_amount.toLocaleString() }}원</span>
            <div class="status-btns">
              <button v-if="order.status === 'pending'" @click="changeStatus(order.id, 'preparing')" class="btn-prep">준비</button>
              <button v-if="order.status === 'preparing'" @click="changeStatus(order.id, 'completed')" class="btn-done">완료</button>
            </div>
          </div>
          <div v-if="!t.orders.length" class="no-orders">주문 없음</div>
        </div>
        <div class="table-actions">
          <button @click="viewTableOrders(t)" class="btn-detail">상세보기</button>
        </div>
      </div>
    </div>

    <!-- Detail modal -->
    <div v-if="selectedTable" class="modal-overlay" @click="selectedTable = null">
      <div class="modal" @click.stop>
        <h2>테이블 {{ selectedTable.table_number }} 주문 상세</h2>
        <div v-for="order in detailOrders" :key="order.id" class="detail-order">
          <div class="detail-header">
            <span>#{{ order.id }} — <span :class="['status-tag', order.status]">{{ statusLabel(order.status) }}</span></span>
            <span>{{ formatTime(order.created_at) }}</span>
          </div>
          <div v-for="item in order.items" :key="item.id" class="detail-item">
            {{ item.menu_name }} × {{ item.quantity }} = {{ item.subtotal.toLocaleString() }}원
          </div>
          <div class="detail-total">{{ order.total_amount.toLocaleString() }}원</div>
          <div class="detail-actions">
            <button v-if="order.status === 'pending'" @click="changeStatus(order.id, 'preparing')" class="btn-prep">준비중으로</button>
            <button v-if="order.status === 'preparing'" @click="changeStatus(order.id, 'completed')" class="btn-done">완료처리</button>
            <button @click="removeOrder(order.id)" class="btn-del">삭제</button>
          </div>
        </div>
        <div v-if="!detailOrders.length" class="no-orders">주문이 없습니다</div>
        <button @click="selectedTable = null" class="btn-close">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { getTables, getOrdersByTable, updateOrderStatus, deleteOrder, subscribeOrders } from '../../api'

const router = useRouter()
const auth = useAuthStore()
const storeId = Number(localStorage.getItem('admin_store_id'))
const storeName = localStorage.getItem('admin_store_name') || ''

const tableList = ref([])
const selectedTable = ref(null)
const detailOrders = ref([])
const newOrderIds = ref(new Set())

const statusMap = { pending: '대기중', preparing: '준비중', completed: '완료' }
const statusLabel = (s) => statusMap[s] || s
const formatTime = (t) => new Date(t).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
const isNew = (order) => newOrderIds.value.has(order.id)

let unsubscribe = null

async function loadTables() {
  tableList.value = await getTables(storeId)
}

async function viewTableOrders(t) {
  selectedTable.value = t
  detailOrders.value = await getOrdersByTable(t.id)
}

async function changeStatus(orderId, status) {
  await updateOrderStatus(orderId, status)
  await loadTables()
  if (selectedTable.value) await viewTableOrders(selectedTable.value)
}

async function removeOrder(orderId) {
  if (!confirm('이 주문을 삭제하시겠습니까?')) return
  await deleteOrder(orderId)
  await loadTables()
  if (selectedTable.value) await viewTableOrders(selectedTable.value)
}

function logout() { auth.adminLogout(); router.push('/admin/login') }

onMounted(async () => {
  await loadTables()
  unsubscribe = subscribeOrders(storeId, async (event) => {
    if (event.type === 'new_order') {
      newOrderIds.value.add(event.order.id)
      setTimeout(() => newOrderIds.value.delete(event.order.id), 5000)
    }
    await loadTables()
    if (selectedTable.value) await viewTableOrders(selectedTable.value)
  })
})

onUnmounted(() => { unsubscribe?.() })
</script>

<style scoped>
.dashboard { min-height: 100vh; background: #f5f5f5; }
.top-bar { display: flex; align-items: center; padding: 12px 20px; background: #1565C0; color: white; flex-wrap: wrap; gap: 8px; }
.top-bar .title { font-size: 1.2rem; font-weight: bold; flex: 1; }
.nav-links { display: flex; gap: 12px; align-items: center; }
.nav-links a { color: white; text-decoration: none; padding: 6px 12px; border-radius: 6px; background: rgba(255,255,255,0.15); }
.logout-btn { background: rgba(255,255,255,0.2); color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; }
.table-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; padding: 20px; }
.table-card { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.table-card.has-orders { border-left: 4px solid #4CAF50; }
.table-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.table-num { font-weight: bold; font-size: 1.1rem; }
.table-total { color: #4CAF50; font-weight: bold; }
.mini-order { display: flex; justify-content: space-between; align-items: center; padding: 6px 8px; margin-bottom: 4px; border-radius: 6px; font-size: 0.9rem; background: #fafafa; }
.mini-order.pending { background: #FFF3E0; }
.mini-order.preparing { background: #E3F2FD; }
.mini-order.completed { background: #E8F5E9; }
.mini-order.new-order { animation: pulse 1s ease-in-out 3; }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); box-shadow: 0 0 8px rgba(76,175,80,0.4); } }
.status-btns button { padding: 4px 8px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8rem; color: white; }
.btn-prep { background: #1565C0; }
.btn-done { background: #2E7D32; }
.btn-del { background: #e53935; color: white; padding: 4px 8px; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
.no-orders { color: #999; font-size: 0.9rem; padding: 8px 0; }
.table-actions { margin-top: 8px; }
.btn-detail { width: 100%; padding: 8px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 6px; cursor: pointer; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: white; padding: 24px; border-radius: 16px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; }
.modal h2 { margin-top: 0; }
.detail-order { border: 1px solid #eee; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.detail-header { display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: bold; }
.status-tag { padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; }
.status-tag.pending { background: #FFF3E0; color: #E65100; }
.status-tag.preparing { background: #E3F2FD; color: #1565C0; }
.status-tag.completed { background: #E8F5E9; color: #2E7D32; }
.detail-item { font-size: 0.9rem; padding: 2px 0; }
.detail-total { font-weight: bold; text-align: right; margin-top: 6px; color: #4CAF50; }
.detail-actions { display: flex; gap: 6px; margin-top: 8px; }
.detail-actions button { font-size: 0.85rem; }
.btn-close { width: 100%; padding: 10px; margin-top: 12px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; cursor: pointer; }
</style>
