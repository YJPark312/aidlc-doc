<template>
  <div class="login-page">
    <h1>🔐 관리자 로그인</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <input v-model="storeName" placeholder="매장명" required />
      <input v-model="username" placeholder="사용자명" required />
      <input v-model="password" type="password" placeholder="비밀번호" required />
      <button type="submit" :disabled="loading">{{ loading ? '로그인 중...' : '로그인' }}</button>
      <p v-if="error" class="error">{{ error }}</p>
      <router-link to="/admin/register" class="link">회원가입</router-link>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const storeName = ref('')
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    await auth.adminLogin(storeName.value, username.value, password.value)
    router.push('/admin/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || '로그인 실패'
  } finally { loading.value = false }
}
</script>

<style scoped>
.login-page { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
.login-page h1 { margin-bottom: 2rem; }
.login-form { display: flex; flex-direction: column; gap: 12px; width: 100%; max-width: 360px; }
.login-form input { padding: 12px; font-size: 1rem; border: 1px solid #ddd; border-radius: 8px; }
.login-form button { padding: 14px; font-size: 1.1rem; background: var(--kb-brown); color: white; border: none; border-radius: 8px; cursor: pointer; }
.login-form button:disabled { background: #ccc; }
.error { color: #e53935; text-align: center; }
.link { text-align: center; color: var(--kb-brown); }
</style>
