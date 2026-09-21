import { defineStore } from 'pinia'
import { api, getToken, setToken } from '@/api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null, checked: false }),
  getters: { isAuthenticated: (s) => s.user !== null },
  actions: {
    async login(email, password) {
      const res = await api.post('/api/auth/login', { email, password })
      setToken(res.access_token)
      this.user = { email, display_name: res.display_name }
      this.checked = true
    },
    logout() {
      setToken(null)
      this.user = null
    },
    /** Vérifie le jeton en session au chargement de l'admin. */
    async restore() {
      if (this.checked) return
      this.checked = true
      if (!getToken()) return
      try {
        this.user = await api.get('/api/auth/me', { auth: true })
      } catch {
        setToken(null)
      }
    },
  },
})
