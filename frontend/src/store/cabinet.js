import { defineStore } from 'pinia'
import api from '../api/axios'

export const useCabinetStore = defineStore('cabinet', {
  state: () => ({
    user: null,           // Имя, баланс
    activeBooking: null,  // Текущая бронь
    dictionaries: {       // Справочники для фильтров (загрузим 1 раз)
      cpus: [],
      gpus: [],
      oses: []
    },
    isLoading: false
  }),

  actions: {
    // 1. ЕДИНАЯ ЗАГРУЗКА ДАННЫХ
    async initCabinet() {
      if (this.user) return // Если уже загружено - не грузим повторно

      this.isLoading = true
      try {
        // Используем Promise.all для параллельной загрузки
        const [cabinetRes, cpusRes, gpusRes, osesRes] = await Promise.all([
          api.get('/api/cabinet'),       // Профиль + активная бронь
          api.get('/api/admin/cpus'),    // Справочники
          api.get('/api/admin/gpus'),
          api.get('/api/admin/oses')
        ])

        // Сохраняем данные
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

    // 2. ОТМЕНА БРОНИ (Обновляем стейт локально)
    async cancelBooking() {
      if (!this.activeBooking) return

      try {
        await api.post('/api/cabinet/cancel', { booking_id: this.activeBooking.id })
        
        // Мгновенное обновление UI
        this.activeBooking = null
      } catch (e) {
        console.error("Ошибка отмены", e)
        throw e
      }
    },

    // 3. СОЗДАНИЕ БРОНИ (Вызывается из формы бронирования)
    updateAfterBooking(price, newBooking) {
      if (this.user) {
        this.user.balance -= price // Списываем баланс визуально
      }
      this.activeBooking = newBooking // Устанавливаем активную бронь
    },

    // 4. ОЧИСТКА КАБИНЕТА (Вызывается при LogOut) [НОВОЕ]
    clearCabinet() {
      this.user = null
      this.activeBooking = null
      // Dictionaries (справочники) мы не чистим специально, 
      // чтобы следующему пользователю не пришлось их грузить заново.
      // Если хотите полный сброс всего, используйте this.$reset()
    }
  }
})