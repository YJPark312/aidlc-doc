<template>
  <div class="menu-page">
    <header class="top-bar">
      <span class="title">🍽️ 메뉴</span>
      <router-link to="/customer/orders" class="nav-btn">📋 주문내역</router-link>
      <router-link to="/customer/cart" class="nav-btn cart-btn">🛒 {{ cartStore.totalCount }}</router-link>
    </header>

    <nav class="category-tabs">
      <button v-for="cat in categories" :key="cat.id"
        :class="{ active: selectedCategory === cat.id }"
        @click="selectedCategory = cat.id">{{ cat.name }}</button>
    </nav>

    <div class="menu-grid">
      <div v-for="menu in filteredMenus" :key="menu.id" class="menu-card" @click="addToCart(menu)">
        <div class="menu-img">
          <img v-if="menu.image_url" :src="menu.image_url" :alt="menu.name" />
          <span v-else>🍽️</span>
        </div>
        <div class="menu-info">
          <h3>{{ menu.name }}</h3>
          <p class="desc">{{ menu.description }}</p>
          <p class="price">{{ menu.price.toLocaleString() }}원</p>
        </div>
      </div>
    </div>

    <div v-if="toast" class="toast">{{ toast }}</div>

    <!-- 픽업 알림 모달 -->
    <div v-if="showPickup" class="pickup-overlay">
      <div class="pickup-modal">
        <div class="pickup-icon">🔔</div>
        <h2>메뉴가 준비되었습니다</h2>
        <p>픽업해주세요!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getMenus, subscribeOrders } from '../../api'
import { useCartStore } from '../../stores/cart'

const cartStore = useCartStore()
const categories = ref([])
const selectedCategory = ref(null)
const toast = ref('')
const showPickup = ref(false)

const storeId = Number(localStorage.getItem('table_store_id'))
let unsubscribe = null

const filteredMenus = computed(() => {
  const cat = categories.value.find(c => c.id === selectedCategory.value)
  return cat?.menus || []
})

onMounted(async () => {
  categories.value = await getMenus(storeId)
  if (categories.value.length) selectedCategory.value = categories.value[0].id

  unsubscribe = subscribeOrders(storeId, (event) => {
    if (event.type === 'status_change' && event.status === 'completed') {
      showPickup.value = true
      setTimeout(() => { showPickup.value = false }, 5000)
    }
  })
})

onUnmounted(() => { unsubscribe?.() })

function addToCart(menu) {
  cartStore.addItem(menu)
  toast.value = `${menu.name} 추가됨`
  setTimeout(() => toast.value = '', 1500)
}
</script>

<style scoped>
.menu-page { padding-bottom: 20px; }
.top-bar { display: flex; align-items: center; padding: 12px 16px; background: var(--kb-brown); color: white; position: sticky; top: 0; z-index: 10; }
.top-bar .title { font-size: 1.3rem; font-weight: bold; flex: 1; }
.nav-btn { text-decoration: none; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.15); color: white; margin-left: 8px; font-size: 0.9rem; }
.cart-btn { background: var(--kb-yellow); color: var(--kb-brown); font-weight: bold; }
.category-tabs { display: flex; gap: 8px; padding: 12px 16px; overflow-x: auto; background: var(--kb-light-yellow); border-bottom: 1px solid #eee; }
.category-tabs button { padding: 8px 16px; border: 1px solid #ddd; border-radius: 20px; background: white; white-space: nowrap; cursor: pointer; font-size: 0.95rem; }
.category-tabs button.active { background: var(--kb-yellow); color: var(--kb-brown); border-color: var(--kb-yellow); font-weight: bold; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; padding: 16px; }
.menu-card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; cursor: pointer; min-height: 44px; }
.menu-card:active { transform: scale(0.97); }
.menu-img { height: 120px; background: var(--kb-light-yellow); display: flex; align-items: center; justify-content: center; font-size: 2rem; }
.menu-img img { width: 100%; height: 100%; object-fit: cover; }
.menu-info { padding: 10px; }
.menu-info h3 { font-size: 1rem; margin: 0 0 4px; }
.menu-info .desc { font-size: 0.8rem; color: #888; margin: 0 0 6px; }
.menu-info .price { font-size: 1.1rem; font-weight: bold; color: var(--kb-dark-yellow); margin: 0; }
.toast { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: var(--kb-brown); color: var(--kb-yellow); padding: 10px 24px; border-radius: 20px; font-size: 0.9rem; z-index: 100; }
.pickup-overlay { position: fixed; inset: 0; background: rgba(74,55,40,0.85); display: flex; align-items: center; justify-content: center; z-index: 200; animation: fadeIn 0.3s; }
.pickup-modal { background: white; padding: 40px; border-radius: 20px; text-align: center; min-width: 300px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); animation: popIn 0.4s; }
.pickup-icon { font-size: 4rem; margin-bottom: 12px; animation: ring 0.5s ease-in-out 3; }
.pickup-modal h2 { color: var(--kb-brown); font-size: 1.5rem; margin-bottom: 8px; }
.pickup-modal p { color: var(--kb-dark-yellow); font-size: 1.2rem; font-weight: bold; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes popIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes ring { 0%, 100% { transform: rotate(0); } 25% { transform: rotate(15deg); } 75% { transform: rotate(-15deg); } }
</style>
