import { reactive } from 'vue'

const state = reactive({ items: [] })
let counter = 0

/** Notifications éphémères de l'administration. */
export function useToast() {
  function push(message, type = 'success', ms = 3500) {
    const id = ++counter
    state.items.push({ id, message, type })
    setTimeout(() => {
      const i = state.items.findIndex((t) => t.id === id)
      if (i >= 0) state.items.splice(i, 1)
    }, ms)
  }
  return {
    items: state.items,
    success: (m) => push(m, 'success'),
    error: (m) => push(m, 'error', 6000),
  }
}
