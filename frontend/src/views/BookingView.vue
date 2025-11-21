<template>
  <div class="booking-page fade-in">
    
    <h2 class="page-title">Бронирование</h2>

    <section class="filters-section glass-card">
      <PcFilters @apply="applyFilters" />
    </section>

    <section class="list-section">
      <PcList v-if="filteredPcs" :pcs="filteredPcs" @select="scrollToForm" />
    </section>

    <div v-if="selectedPc" id="booking-form" class="form-section glass-card fade-in">
      <div class="form-header">
        <h3>Подтверждение брони</h3>
        <button class="close-btn" @click="selectedPc = null">✕</button>
      </div>
      
      <p class="selected-info">
        Вы выбрали <strong>Station {{ selectedPc.id }}</strong>
      </p>

      <BookingForm :pc="selectedPc" @created="refresh" />
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted, nextTick } from 'vue'
import api from '../api/axios'
import PcFilters from '../components/PcFilters.vue'
import PcList from '../components/PcList.vue'
import BookingForm from '../components/BookingForm.vue'

// allPcs хранит "сырые" данные с сервера (все пк)
const allPcs = ref([])
// filteredPcs хранит то, что видит пользователь
const filteredPcs = ref([])
const selectedPc = ref(null)

// 1. Загрузка данных (Выполняется 1 раз при маунте)
async function fetchPcs() {
  try {
    const { data } = await api.get('/api/bookings/pcs')
    allPcs.value = data
    filteredPcs.value = data // Изначально показываем всё
    console.log(allPcs)
  } catch (e) {
    console.error('Ошибка загрузки ПК:', e)
  }
}

// 2. Локальная фильтрация (Без запросов к API)
function applyFilters(filters = {}) {
  let result = allPcs.value

  // --- Фильтрация по железу ---
  if (filters.cpu_id)
    result = result.filter(pc => pc.cpu_id == filters.cpu_id)

  if (filters.gpu_id)
    result = result.filter(pc => pc.gpu_id == filters.gpu_id)

  if (filters.os_id)
    result = result.filter(pc => pc.os_id == filters.os_id)

  // --- Фильтрация по времени (Client-side intersection check) ---
  // filters.filter_date приходит в формате "YYYY-MM-DDTHH:MM" из datetime-local
  // filters.filter_hours это длительность (число)
  
  if (filters.filter_date && filters.filter_hours) {
    const reqStart = new Date(filters.filter_date)
    // Вычисляем конец желаемой брони: start + duration hours
    const reqEnd = new Date(reqStart.getTime() + filters.filter_hours * 3600000)

    result = result.filter(pc => {
      // Если у ПК нет броней (busy пустой), он свободен -> true
      if (!pc.busy || pc.busy.length === 0) return true

      // Проверяем пересечение с существующими бронями
      // ПК подходит, если НЕТ ни одного пересечения
      const hasConflict = pc.busy.some(usage => {
        const busyStart = new Date(usage.start)
        const busyEnd = new Date(usage.end)
        console.log(reqStart)
        console.log(busyEnd)
        console.log(reqEnd)
        console.log(busyStart)
        console.log(reqStart < busyEnd && reqEnd > busyStart)

        // Формула пересечения диапазонов: (StartA < EndB) && (EndA > StartB)
        return (reqStart < busyEnd && reqEnd > busyStart)
      })

      return !hasConflict
    })
  }

  filteredPcs.value = result
}

function refresh() {
  selectedPc.value = null
  fetchPcs() // Перезагружаем данные, чтобы обновить занятость после успешной брони
}

function scrollToForm(pc) {
  selectedPc.value = pc
  nextTick(() => {
    document.getElementById('booking-form')?.scrollIntoView({ behavior: 'smooth' })
  })
}

onMounted(() => {
  fetchPcs()
})
</script>

<style scoped>
/* Стили остались без изменений */
.booking-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 3rem 1rem;
}

.filters-section {
  padding: 2rem;
  margin-bottom: 2rem;
}

.list-section {
  margin-bottom: 2rem;
}

.form-section {
  padding: 2rem;
  border: 1px solid var(--primary);
  box-shadow: 0 0 30px rgba(99, 102, 241, 0.1);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.5rem;
  cursor: pointer;
}
.close-btn:hover { color: white; }

.selected-info {
  margin-bottom: 1.5rem;
  color: var(--text-muted);
}
.selected-info strong { color: var(--primary); }
</style>