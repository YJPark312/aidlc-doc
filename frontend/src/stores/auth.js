import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginAdmin, loginTable, register, parseToken } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const adminToken = ref(localStorage.getItem('admin_token'))
  const tableToken = ref(localStorage.getItem('table_token'))

  const adminInfo = computed(() => adminToken.value ? parseToken(adminToken.value) : null)
  const tableInfo = computed(() => tableToken.value ? parseToken(tableToken.value) : null)

  async function adminLogin(storeName, username, password) {
    const res = await loginAdmin(storeName, username, password)
    adminToken.value = res.access_token
    localStorage.setItem('admin_token', res.access_token)
    localStorage.setItem('admin_store_id', res.store_id)
    localStorage.setItem('admin_store_name', res.store_name)
    return res
  }

  async function adminRegister(storeName, username, password) {
    return await register(storeName, username, password)
  }

  async function tableLogin(storeId, tableNumber, password) {
    const res = await loginTable(storeId, tableNumber, password)
    tableToken.value = res.access_token
    localStorage.setItem('table_token', res.access_token)
    localStorage.setItem('table_id', res.table_id)
    localStorage.setItem('table_store_id', storeId)
    if (res.session_id) localStorage.setItem('session_id', res.session_id)
    return res
  }

  function adminLogout() {
    adminToken.value = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_store_id')
    localStorage.removeItem('admin_store_name')
  }

  function tableLogout() {
    tableToken.value = null
    localStorage.removeItem('table_token')
    localStorage.removeItem('table_id')
    localStorage.removeItem('table_store_id')
    localStorage.removeItem('session_id')
  }

  return { adminToken, tableToken, adminInfo, tableInfo, adminLogin, adminRegister, tableLogin, adminLogout, tableLogout }
})
