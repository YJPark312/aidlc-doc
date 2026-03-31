import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // Customer routes
  {
    path: '/customer/login',
    name: 'CustomerLogin',
    component: () => import('../views/customer/CustomerLogin.vue')
  },
  {
    path: '/customer/menu',
    name: 'CustomerMenu',
    component: () => import('../views/customer/CustomerMenu.vue'),
    meta: { requiresTableAuth: true }
  },
  {
    path: '/customer/cart',
    name: 'CustomerCart',
    component: () => import('../views/customer/CustomerCart.vue'),
    meta: { requiresTableAuth: true }
  },
  {
    path: '/customer/orders',
    name: 'CustomerOrders',
    component: () => import('../views/customer/CustomerOrders.vue'),
    meta: { requiresTableAuth: true }
  },
  // Admin routes
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/AdminLogin.vue')
  },
  {
    path: '/admin/register',
    name: 'AdminRegister',
    component: () => import('../views/admin/AdminRegister.vue')
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: { requiresAdminAuth: true }
  },
  {
    path: '/admin/menus',
    name: 'AdminMenus',
    component: () => import('../views/admin/AdminMenus.vue'),
    meta: { requiresAdminAuth: true }
  },
  {
    path: '/admin/tables',
    name: 'AdminTables',
    component: () => import('../views/admin/AdminTables.vue'),
    meta: { requiresAdminAuth: true }
  },
  { path: '/', redirect: '/customer/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  if (to.meta.requiresTableAuth) {
    const token = localStorage.getItem('table_token')
    if (!token) return { name: 'CustomerLogin' }
  }
  if (to.meta.requiresAdminAuth) {
    const token = localStorage.getItem('admin_token')
    if (!token) return { name: 'AdminLogin' }
  }
})

export default router
