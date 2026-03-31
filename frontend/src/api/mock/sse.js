// Mock SSE event bus for real-time order notifications
const listeners = new Map() // storeId -> Set<callback>

export const sseManager = {
  subscribe(storeId, callback) {
    if (!listeners.has(storeId)) listeners.set(storeId, new Set())
    listeners.get(storeId).add(callback)
    return () => listeners.get(storeId)?.delete(callback)
  },
  emit(storeId, event) {
    listeners.get(storeId)?.forEach(cb => cb(event))
  }
}
