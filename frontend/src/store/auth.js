import { defineStore } from 'pinia'
import api from '../api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(email, password) {
      const { data } = await api.post('/api/auth/login', { email, password })
      this.token = data.access_token
      this.user = data.user

      localStorage.setItem('token', this.token)
      api.defaults.headers.common.Authorization = `Bearer ${this.token}`
    },

    async restore() {
      if (!this.token) return

      api.defaults.headers.common.Authorization = `Bearer ${this.token}`

      try {
        const { data } = await api.get('/api/auth/me')
        this.user = data
      } catch (err) {
        // токен протух — принудительный выход
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common.Authorization
    }
  }
})
