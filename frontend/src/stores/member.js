import { defineStore } from 'pinia'
import { api } from '@/api/client'

/** Compte joueur. L'authentification passe par un cookie httpOnly posé par le serveur. */
export const useMemberStore = defineStore('member', {
  state: () => ({ member: null, checked: false }),
  getters: { isLoggedIn: (s) => s.member !== null },
  actions: {
    async restore() {
      if (this.checked) return
      this.checked = true
      try { this.member = await api.get('/api/account/me') } catch { this.member = null }
    },
    async register(payload) {
      this.member = await api.post('/api/account/register', payload)
      this.checked = true
    },
    async login(email, password) {
      this.member = await api.post('/api/account/login', { email, password })
      this.checked = true
    },
    async logout() {
      await api.post('/api/account/logout', {})
      this.member = null
    },
    async update(payload) {
      this.member = await api.put('/api/account/me', payload)
    },
    async changePassword(current_password, new_password) {
      await api.post('/api/account/password', { current_password, new_password })
    },
    async remove() {
      await api.delete('/api/account/me')
      this.member = null
    },
  },
})
