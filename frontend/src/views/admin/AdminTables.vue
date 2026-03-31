<template>
  <div class="admin-page">
    <header class="top-bar">
      <router-link to="/admin/dashboard" class="back-btn">← 대시보드</router-link>
      <span class="title">🪑 테이블 관리</span>
    </header>

    <!-- Add table form -->
    <form @submit.prevent="addTable" class="add-form">
      <input v-model.number="newTableNumber" type="number" placeholder="테이블 번호" min="1" required />
      <input v-model="newTablePassword" type="password" placeholder="테이블 비밀번호" required />
      <button type="submit">추가</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <!-- Table list -->
    <div class="table-list">
      <div v-for="t in tableList" :key="t.id" class="table-row">
        <div class="table-info">
          <span class="table-num">테이블 {{ t.table_number }}</span>
          <span class="table-status" :class="{ active: t.session_id }">
            {{ t.session_id ? '이용중' : '비어있음' }}
          </span>
          <span class="table-amount">{{ t.total_amount.toLocaleString() }}원</span>
        </div>
        <div class="table-actions">
          <button v-if="t.session_id" @click="completeSession(t.id)" class="btn-complete">이용완료</button>
          <button @click="viewHistory(t)" class="btn-history">과거내역</button>
        </div>
      </div>
      <div v-if="!tableList.length" class="empty">등록된 테이블이 없습니다</div>
    </div>

    <!-- History modal -->
    <div v-if="historyTable" class="modal-overlay" @click="historyTable = null">
      <div class="modal" @click.stop>
        <h2>테이블 {{ historyTable.table_number }} 과거 내역</h2>
        <input v-model="dateFilter" type="date" @change="loadHistory" class="date-filter" />
        <div v-for="h in historyList" :key="h.id" class="history-item">
          <div class="history-header">
            <span>#{{ h.order_id }}</span>
            <span>{{ formatTime(h.order_created_at) }}</span>
            <span class="history-amount">{{ h.total_amount.toLocaleString() }}원</span>
          </div>
          <div v-for="item in h.items" :key="item.id" class="history-detail">
            {{ item.menu_name }} × {{ item.quantity }}
          </div>
          <div class="history-completed">완료: {{ formatTime(h.completed_at) }}</div>
        </div>
        <div v-if="!historyList.length" class="empty">과거 내역이 없습니다</div>
        <button @click="historyTable = null" class="btn-close">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTables, setupTable, completeTableSession, getOrderHistory } from '../../api'

const storeId = Number(localStorage.getItem('admin_store_id'))
const tableList = ref([])
const newTableNumber = ref('')
const newTablePassword = ref('')
const error = ref('')
const historyTable = ref(null)
const historyList = ref([])
const dateFilter = ref('')

const formatTime = (t) => new Date(t).toLocaleString('ko-KR', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })

async function load() { tableList.value = await getTables(storeId) }

async function addTable() {
  error.value = ''
  try {
    await setupTable(storeId, newTableNumber.value, newTablePassword.value)
    newTableNumber.value = ''; newTablePassword.value = ''
    await load()
  } catch (e) { error.value = e.response?.data?.detail || '테이블 추가 실패' }
}

async function completeSession(tableId) {
  if (!confirm('이 테이블의 이용을 완료하시겠습니까? 현재 주문이 모두 과거 내역으로 이동됩니다.')) return
  await completeTableSession(tableId)
  await load()
}

async function viewHistory(t) {
  historyTable.value = t
  dateFilter.value = ''
  await loadHistory()
}

async function loadHistory() {
  historyList.value = await getOrderHistory(historyTable.value.id, dateFilter.value || undefined)
}

onMounted(load)
</script>

<style scoped>
.admin-page { min-height: 100vh; background: #f5f5f5; }
.top-bar { display: flex; align-items: center; padding: 12px 20px; background: var(--kb-brown); color: white; }
.back-btn { color: white; text-decoration: none; margin-right: 12px; }
.title { font-size: 1.2rem; font-weight: bold; }
.add-form { display: flex; gap: 8px; padding: 16px; background: white; margin: 16px; border-radius: 12px; flex-wrap: wrap; }
.add-form input { padding: 10px; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 120px; }
.add-form button { padding: 10px 20px; background: var(--kb-brown); color: white; border: none; border-radius: 8px; cursor: pointer; }
.error { color: #e53935; width: 100%; }
.table-list { padding: 0 16px; }
.table-row { display: flex; justify-content: space-between; align-items: center; background: white; padding: 14px; border-radius: 10px; margin-bottom: 8px; flex-wrap: wrap; gap: 8px; }
.table-info { display: flex; align-items: center; gap: 12px; flex: 1; }
.table-num { font-weight: bold; }
.table-status { padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; background: #f5f5f5; color: #999; }
.table-status.active { background: var(--kb-light-yellow); color: var(--kb-dark-yellow); }
.table-amount { font-weight: bold; color: var(--kb-dark-yellow); }
.table-actions { display: flex; gap: 6px; }
.btn-complete { padding: 6px 14px; background: #FFA726; color: white; border: none; border-radius: 6px; cursor: pointer; }
.btn-history { padding: 6px 14px; background: #78909C; color: white; border: none; border-radius: 6px; cursor: pointer; }
.empty { color: #999; padding: 20px; text-align: center; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: white; padding: 24px; border-radius: 16px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; }
.modal h2 { margin-top: 0; }
.date-filter { padding: 8px; border: 1px solid #ddd; border-radius: 6px; margin-bottom: 12px; width: 100%; }
.history-item { border: 1px solid #eee; border-radius: 8px; padding: 10px; margin-bottom: 8px; }
.history-header { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px; }
.history-amount { color: var(--kb-dark-yellow); }
.history-detail { font-size: 0.9rem; color: #666; }
.history-completed { font-size: 0.8rem; color: #999; margin-top: 4px; }
.btn-close { width: 100%; padding: 10px; margin-top: 12px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; cursor: pointer; }
</style>
