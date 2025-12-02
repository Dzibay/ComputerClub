import { defineStore } from 'pinia'
import api from '../api/axios'

export const useCabinetStore = defineStore('cabinet', {
  state: () => ({
    user: null,
    activeBooking: null,
    dictionaries: {
      cpus: [],
      gpus: [],
      oses: []
    },
    isLoading: false
  }),

  actions: {
    // 1. ЕДИНАЯ ЗАГРУЗКА ДАННЫХ
    async initCabinet() {
      if (this.user) return

      this.isLoading = true
      try {
        const [cabinetRes, cpusRes, gpusRes, osesRes] = await Promise.all([
          api.get('/api/cabinet'),
          api.get('/api/admin/cpus'),
          api.get('/api/admin/gpus'),
          api.get('/api/admin/oses')
        ])

        this.user = cabinetRes.data.user
        this.activeBooking = cabinetRes.data.active_booking
        
        this.dictionaries.cpus = cpusRes.data
        this.dictionaries.gpus = gpusRes.data
        this.dictionaries.oses = osesRes.data

      } catch (e) {
        console.error("Ошибка инициализации кабинета", e)
      } finally {
        this.isLoading = false
      }
    },

    // 2. ОТМЕНА БРОНИ
    async cancelBooking() {
      if (!this.activeBooking) return

      try {
        await api.post('/api/cabinet/cancel', { booking_id: this.activeBooking.id })
        
        this.activeBooking = null
      } catch (e) {
        console.error("Ошибка отмены", e)
        throw e
      }
    },

    // 3. СОЗДАНИЕ БРОНИ
    updateAfterBooking(price, newBooking) {
      if (this.user) {
        this.user.balance -= price
      }
      this.activeBooking = newBooking
    },

    // 4. ОЧИСТКА КАБИНЕТА (Вызывается при LogOut)
    clearCabinet() {
      this.user = null
      this.activeBooking = null
    }
  }
})