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
        <div class="menu-img">{{ menu.image_url ? '' : '🍽️' }}</div>
        <div class="menu-info">
          <h3>{{ menu.name }}</h3>
          <p class="desc">{{ menu.description }}</p>
          <p class="price">{{ menu.price.toLocaleString() }}원</p>
        </div>
      </div>
    </div>

    <div v-if="toast" class="toast">{{ toast }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMenus } from '../../api'
import { useCartStore } from '../../stores/cart'

const cartStore = useCartStore()
const categories = ref([])
const selectedCategory = ref(null)
const toast = ref('')

const storeId = Number(localStorage.getItem('table_store_id'))

const filteredMenus = computed(() => {
  const cat = categories.value.find(c => c.id === selectedCategory.value)
  return cat?.menus || []
})

onMounted(async () => {
  categories.value = await getMenus(storeId)
  if (categories.value.length) selectedCategory.value = categories.value[0].id
})

function addToCart(menu) {
  cartStore.addItem(menu)
  toast.value = `${menu.name} 추가됨`
  setTimeout(() => toast.value = '', 1500)
}
</script>

<style scoped>
.menu-page { padding-bottom: 20px; }
.top-bar { display: flex; align-items: center; padding: 12px 16px; background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 10; }
.top-bar .title { font-size: 1.3rem; font-weight: bold; flex: 1; }
.nav-btn { text-decoration: none; padding: 8px 12px; border-radius: 8px; background: #f5f5f5; margin-left: 8px; font-size: 0.9rem; }
.cart-btn { background: #4CAF50; color: white; }
.category-tabs { display: flex; gap: 8px; padding: 12px 16px; overflow-x: auto; background: #fafafa; border-bottom: 1px solid #eee; }
.category-tabs button { padding: 8px 16px; border: 1px solid #ddd; border-radius: 20px; background: white; white-space: nowrap; cursor: pointer; font-size: 0.95rem; }
.category-tabs button.active { background: #4CAF50; color: white; border-color: #4CAF50; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; padding: 16px; }
.menu-card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; cursor: pointer; min-height: 44px; }
.menu-card:active { transform: scale(0.97); }
.menu-img { height: 100px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; font-size: 2rem; }
.menu-info { padding: 10px; }
.menu-info h3 { font-size: 1rem; margin: 0 0 4px; }
.menu-info .desc { font-size: 0.8rem; color: #888; margin: 0 0 6px; }
.menu-info .price { font-size: 1.1rem; font-weight: bold; color: #4CAF50; margin: 0; }
.toast { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: #333; color: white; padding: 10px 24px; border-radius: 20px; font-size: 0.9rem; z-index: 100; }
</style>
