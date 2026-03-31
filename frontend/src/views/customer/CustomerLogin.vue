<template>
  <div class="login-page">
    <h1>🍽️ 테이블오더</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <input v-model.number="storeId" type="number" placeholder="매장 ID" required />
      <input v-model.number="tableNumber" type="number" placeholder="테이블 번호" required />
      <input v-model="password" type="password" placeholder="비밀번호" required />
      <button type="submit" :disabled="loading">{{ loading ? '로그인 중...' : '로그인' }}</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const storeId = ref(Number(localStorage.getItem('table_store_id')) || '')
const tableNumber = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

// Auto-login if token exists
if (localStorage.getItem('table_token')) {
  router.replace('/customer/menu')
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.tableLogin(storeId.value, tableNumber.value, password.value)
    router.push('/customer/menu')
  } catch (e) {
    error.value = e.response?.data?.detail || '로그인에 실패했습니다'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
.login-page h1 { font-size: 2rem; margin-bottom: 2rem; }
.login-form { display: flex; flex-direction: column; gap: 12px; width: 100%; max-width: 320px; }
.login-form input { padding: 12px; font-size: 1rem; border: 1px solid #ddd; border-radius: 8px; }
.login-form button { padding: 14px; font-size: 1.1rem; background: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer; }
.login-form button:disabled { background: #ccc; }
.error { color: #e53935; text-align: center; }
</style>
