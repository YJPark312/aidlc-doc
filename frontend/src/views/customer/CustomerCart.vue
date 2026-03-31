<template>
  <div class="cart-page">
    <header class="top-bar">
      <router-link to="/customer/menu" class="back-btn">← 메뉴</router-link>
      <span class="title">🛒 장바구니</span>
      <button v-if="cartStore.items.length" class="clear-btn" @click="cartStore.clear()">비우기</button>
    </header>

    <div v-if="!cartStore.items.length" class="empty">장바구니가 비어있습니다</div>

    <div v-else class="cart-list">
      <div v-for="item in cartStore.items" :key="item.menu_id" class="cart-item">
        <div class="item-info">
          <h3>{{ item.name }}</h3>
          <p>{{ (item.price * item.quantity).toLocaleString() }}원</p>
        </div>
        <div class="qty-controls">
          <button @click="cartStore.updateQuantity(item.menu_id, item.quantity - 1)">−</button>
          <span>{{ item.quantity }}</span>
          <button @click="cartStore.updateQuantity(item.menu_id, item.quantity + 1)">+</button>
        </div>
        <button class="remove-btn" @click="cartStore.removeItem(item.menu_id)">✕</button>
      </div>
    </div>

    <div v-if="cartStore.items.length" class="cart-footer">
      <div class="total">총 {{ cartStore.totalAmount.toLocaleString() }}원</div>
      <button class="order-btn" :disabled="ordering" @click="placeOrder">
        {{ ordering ? '주문 중...' : '주문하기' }}
      </button>
    </div>

    <!-- Order success modal -->
    <div v-if="orderResult" class="modal-overlay" @click="closeResult">
      <div class="modal" @click.stop>
        <h2>✅ 주문 완료!</h2>
        <p>주문번호: <strong>#{{ orderResult.id }}</strong></p>
        <p>{{ countdown }}초 후 메뉴 화면으로 이동합니다</p>
      </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../../stores/cart'
import { createOrder } from '../../api'

const router = useRouter()
const cartStore = useCartStore()
const ordering = ref(false)
const error = ref('')
const orderResult = ref(null)
const countdown = ref(5)

async function placeOrder() {
  ordering.value = true
  error.value = ''
  try {
    const storeId = Number(localStorage.getItem('table_store_id'))
    const tableId = Number(localStorage.getItem('table_id'))
    const sessionId = Number(localStorage.getItem('session_id')) || null
    const items = cartStore.items.map(i => ({ menu_id: i.menu_id, quantity: i.quantity }))
    const result = await createOrder(storeId, tableId, sessionId, items)
    if (result.session_id) localStorage.setItem('session_id', result.session_id)
    cartStore.clear()
    orderResult.value = result
    // Auto redirect countdown
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) { clearInterval(timer); router.push('/customer/menu') }
    }, 1000)
  } catch (e) {
    error.value = e.response?.data?.detail || '주문에 실패했습니다'
  } finally {
    ordering.value = false
  }
}

function closeResult() { router.push('/customer/menu') }
</script>

<style scoped>
.cart-page { min-height: 100vh; padding-bottom: 100px; }
.top-bar { display: flex; align-items: center; padding: 12px 16px; background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 10; }
.back-btn { text-decoration: none; color: #333; margin-right: 12px; }
.title { flex: 1; font-size: 1.2rem; font-weight: bold; }
.clear-btn { background: none; border: none; color: #e53935; cursor: pointer; }
.empty { text-align: center; padding: 60px 20px; color: #999; font-size: 1.1rem; }
.cart-list { padding: 16px; }
.cart-item { display: flex; align-items: center; padding: 12px; background: white; border-radius: 10px; margin-bottom: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.item-info { flex: 1; }
.item-info h3 { margin: 0 0 4px; font-size: 1rem; }
.item-info p { margin: 0; color: var(--kb-dark-yellow); font-weight: bold; }
.qty-controls { display: flex; align-items: center; gap: 10px; margin: 0 12px; }
.qty-controls button { width: 32px; height: 32px; border-radius: 50%; border: 1px solid #ddd; background: #f5f5f5; font-size: 1.2rem; cursor: pointer; }
.qty-controls span { font-size: 1.1rem; min-width: 20px; text-align: center; }
.remove-btn { background: none; border: none; font-size: 1.2rem; color: #999; cursor: pointer; }
.cart-footer { position: fixed; bottom: 0; left: 0; right: 0; background: white; padding: 16px; border-top: 1px solid #eee; display: flex; align-items: center; gap: 16px; }
.total { font-size: 1.2rem; font-weight: bold; flex: 1; }
.order-btn { padding: 14px 32px; background: var(--kb-yellow); color: var(--kb-brown); border: none; border-radius: 10px; font-size: 1.1rem; font-weight: bold; cursor: pointer; }
.order-btn:disabled { background: #ccc; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: white; padding: 32px; border-radius: 16px; text-align: center; min-width: 280px; }
.modal h2 { color: var(--kb-dark-yellow); }
.error { color: #e53935; text-align: center; padding: 12px; }
</style>
