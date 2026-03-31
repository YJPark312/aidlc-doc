<template>
  <div class="orders-page">
    <header class="top-bar">
      <router-link to="/customer/menu" class="back-btn">← 메뉴</router-link>
      <span class="title">📋 주문 내역</span>
    </header>

    <div v-if="loading" class="loading">불러오는 중...</div>
    <div v-else-if="!orders.length" class="empty">주문 내역이 없습니다</div>

    <div v-else class="order-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span class="order-id">#{{ order.id }}</span>
          <span :class="['status', order.status]">{{ statusLabel(order.status) }}</span>
        </div>
        <div class="order-time">{{ formatTime(order.created_at) }}</div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <span>{{ item.menu_name }} × {{ item.quantity }}</span>
            <span>{{ item.subtotal.toLocaleString() }}원</span>
          </div>
        </div>
        <div class="order-total">합계: {{ order.total_amount.toLocaleString() }}원</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getOrdersBySession } from '../../api'

const orders = ref([])
const loading = ref(true)

const statusMap = { pending: '대기중', preparing: '준비중', completed: '완료' }
const statusLabel = (s) => statusMap[s] || s
const formatTime = (t) => new Date(t).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })

onMounted(async () => {
  const sessionId = Number(localStorage.getItem('session_id'))
  if (sessionId) {
    try { orders.value = await getOrdersBySession(sessionId) } catch {}
  }
  loading.value = false
})
</script>

<style scoped>
.orders-page { min-height: 100vh; }
.top-bar { display: flex; align-items: center; padding: 12px 16px; background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 10; }
.back-btn { text-decoration: none; color: #333; margin-right: 12px; }
.title { flex: 1; font-size: 1.2rem; font-weight: bold; }
.loading, .empty { text-align: center; padding: 60px 20px; color: #999; }
.order-list { padding: 16px; }
.order-card { background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.order-id { font-weight: bold; font-size: 1.1rem; }
.status { padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }
.status.pending { background: #FFF3E0; color: #E65100; }
.status.preparing { background: #E3F2FD; color: var(--kb-brown); }
.status.completed { background: #E8F5E9; color: #2E7D32; }
.order-time { font-size: 0.85rem; color: #999; margin-bottom: 10px; }
.order-items { border-top: 1px solid #f0f0f0; padding-top: 8px; }
.order-item { display: flex; justify-content: space-between; padding: 4px 0; font-size: 0.95rem; }
.order-total { border-top: 1px solid #f0f0f0; padding-top: 8px; margin-top: 8px; font-weight: bold; text-align: right; color: var(--kb-dark-yellow); }
</style>
