<template>
  <div class="admin-page">
    <header class="top-bar">
      <router-link to="/admin/dashboard" class="back-btn">← 대시보드</router-link>
      <span class="title">🍽️ 메뉴 관리</span>
    </header>

    <!-- Add/Edit form -->
    <form @submit.prevent="saveMenu" class="menu-form">
      <h3>{{ editingMenu ? '메뉴 수정' : '메뉴 등록' }}</h3>
      <input v-model="form.name" placeholder="메뉴명" required />
      <input v-model.number="form.price" type="number" placeholder="가격" min="0" required />
      <input v-model="form.description" placeholder="설명" />
      <select v-model.number="form.category_id" required>
        <option value="" disabled>카테고리 선택</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
      <input v-model="form.image_url" placeholder="이미지 URL (선택)" />
      <div class="form-actions">
        <button type="submit">{{ editingMenu ? '수정' : '등록' }}</button>
        <button v-if="editingMenu" type="button" @click="cancelEdit">취소</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </form>

    <!-- Menu list by category -->
    <div v-for="cat in categories" :key="cat.id" class="category-section">
      <h3>{{ cat.name }}</h3>
      <div v-for="menu in cat.menus" :key="menu.id" class="menu-row">
        <span class="menu-name">{{ menu.name }}</span>
        <span class="menu-price">{{ menu.price.toLocaleString() }}원</span>
        <button @click="startEdit(menu)" class="btn-edit">수정</button>
        <button @click="removeMenu(menu.id)" class="btn-del">삭제</button>
      </div>
      <div v-if="!cat.menus.length" class="empty">메뉴가 없습니다</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getMenus, createMenu, updateMenu, deleteMenu } from '../../api'

const storeId = Number(localStorage.getItem('admin_store_id'))
const categories = ref([])
const editingMenu = ref(null)
const error = ref('')
const form = reactive({ name: '', price: '', description: '', category_id: '', image_url: '' })

async function load() { categories.value = await getMenus(storeId) }

async function saveMenu() {
  error.value = ''
  try {
    if (editingMenu.value) {
      await updateMenu(editingMenu.value.id, { ...form })
      editingMenu.value = null
    } else {
      await createMenu(storeId, { ...form })
    }
    Object.assign(form, { name: '', price: '', description: '', category_id: '', image_url: '' })
    await load()
  } catch (e) { error.value = e.response?.data?.detail || '저장 실패' }
}

function startEdit(menu) {
  editingMenu.value = menu
  Object.assign(form, { name: menu.name, price: menu.price, description: menu.description || '', category_id: menu.category_id, image_url: menu.image_url || '' })
}

function cancelEdit() {
  editingMenu.value = null
  Object.assign(form, { name: '', price: '', description: '', category_id: '', image_url: '' })
}

async function removeMenu(menuId) {
  if (!confirm('이 메뉴를 삭제하시겠습니까?')) return
  await deleteMenu(menuId)
  await load()
}

onMounted(load)
</script>

<style scoped>
.admin-page { min-height: 100vh; background: #f5f5f5; }
.top-bar { display: flex; align-items: center; padding: 12px 20px; background: #1565C0; color: white; }
.back-btn { color: white; text-decoration: none; margin-right: 12px; }
.title { font-size: 1.2rem; font-weight: bold; }
.menu-form { background: white; margin: 16px; padding: 16px; border-radius: 12px; display: flex; flex-direction: column; gap: 10px; }
.menu-form h3 { margin: 0 0 8px; }
.menu-form input, .menu-form select { padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; }
.form-actions { display: flex; gap: 8px; }
.form-actions button { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; }
.form-actions button:first-child { background: #1565C0; color: white; }
.form-actions button:last-child { background: #f5f5f5; }
.error { color: #e53935; }
.category-section { margin: 16px; }
.category-section h3 { margin-bottom: 8px; }
.menu-row { display: flex; align-items: center; gap: 10px; background: white; padding: 12px; border-radius: 8px; margin-bottom: 6px; }
.menu-name { flex: 1; font-weight: 500; }
.menu-price { color: #4CAF50; font-weight: bold; min-width: 80px; text-align: right; }
.btn-edit { padding: 6px 12px; background: #FFA726; color: white; border: none; border-radius: 6px; cursor: pointer; }
.btn-del { padding: 6px 12px; background: #e53935; color: white; border: none; border-radius: 6px; cursor: pointer; }
.empty { color: #999; padding: 8px; }
</style>
