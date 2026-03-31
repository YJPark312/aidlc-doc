import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('cart_items') || '[]'))

  const totalAmount = computed(() => items.value.reduce((sum, i) => sum + i.price * i.quantity, 0))
  const totalCount = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))

  function save() { localStorage.setItem('cart_items', JSON.stringify(items.value)) }

  function addItem(menu) {
    const existing = items.value.find(i => i.menu_id === menu.id)
    if (existing) { existing.quantity++ } else {
      items.value.push({ menu_id: menu.id, name: menu.name, price: menu.price, quantity: 1 })
    }
    save()
  }

  function removeItem(menuId) {
    items.value = items.value.filter(i => i.menu_id !== menuId)
    save()
  }

  function updateQuantity(menuId, qty) {
    const item = items.value.find(i => i.menu_id === menuId)
    if (!item) return
    if (qty <= 0) { removeItem(menuId); return }
    item.quantity = qty
    save()
  }

  function clear() { items.value = []; save() }

  return { items, totalAmount, totalCount, addItem, removeItem, updateQuantity, clear }
})
