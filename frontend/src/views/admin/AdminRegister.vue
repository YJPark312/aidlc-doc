<template>
  <div class="login-page">
    <h1>📝 관리자 회원가입</h1>
    <form @submit.prevent="handleRegister" class="login-form">
      <input v-model="storeName" placeholder="매장명" required />
      <input v-model="username" placeholder="사용자명" required />
      <input v-model="password" type="password" placeholder="비밀번호" required />
      <button type="submit" :disabled="loading">{{ loading ? '가입 중...' : '회원가입' }}</button>
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
      <router-link to="/admin/login" class="link">로그인으로 돌아가기</router-link>
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
const success = ref('')

async function handleRegister() {
  loading.value = true; error.value = ''; success.value = ''
  try {
    await auth.adminRegister(storeName.value, username.value, password.value)
    success.value = '회원가입 완료! 로그인 페이지로 이동합니다.'
    setTimeout(() => router.push('/admin/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || '회원가입 실패'
  } finally { loading.value = false }
}
</script>

<style scoped>
.login-page { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
.login-page h1 { margin-bottom: 2rem; }
.login-form { display: flex; flex-direction: column; gap: 12px; width: 100%; max-width: 360px; }
.login-form input { padding: 12px; font-size: 1rem; border: 1px solid #ddd; border-radius: 8px; }
.login-form button { padding: 14px; font-size: 1.1rem; background: #1565C0; color: white; border: none; border-radius: 8px; cursor: pointer; }
.login-form button:disabled { background: #ccc; }
.error { color: #e53935; text-align: center; }
.success { color: #2E7D32; text-align: center; }
.link { text-align: center; color: #1565C0; }
</style>
