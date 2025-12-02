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

const allPcs = ref([])
const filteredPcs = ref([])
const selectedPc = ref(null)

async function fetchPcs() {
  try {
    const { data } = await api.get('/api/bookings/pcs')
    // Бэкенд теперь возвращает поле pc_software = [{software: {...}}, ...]
    allPcs.value = data
    filteredPcs.value = data 
    console.log(allPcs)
  } catch (e) {
    console.error('Ошибка загрузки ПК:', e)
  }
}

function applyFilters(filters = {}) {
  let result = allPcs.value

  // --- Фильтрация по железу ---
  if (filters.cpu_id)
    result = result.filter(pc => pc.cpu_id == filters.cpu_id)

  if (filters.gpu_id)
    result = result.filter(pc => pc.gpu_id == filters.gpu_id)

  if (filters.os_id)
    result = result.filter(pc => pc.os_id == filters.os_id)

  // --- НОВОЕ: Фильтрация по софту ---
  // filters.software_id приходит из PcFilters
  if (filters.software_id) {
    result = result.filter(pc => {
      // pc.pc_software - это массив связей, внутри каждой есть объект software
      // Проверяем, есть ли в этом массиве программа с нужным ID
      return pc.pc_software && pc.pc_software.some(link => link.software.id == filters.software_id)
    })
  }

  // --- Фильтрация по времени ---
  if (filters.filter_date && filters.filter_hours) {
    const reqStart = new Date(filters.filter_date)
    const reqEnd = new Date(reqStart.getTime() + filters.filter_hours * 3600000)

    result = result.filter(pc => {
      if (!pc.busy || pc.busy.length === 0) return true

      const hasConflict = pc.busy.some(usage => {
        const busyStart = new Date(usage.start)
        const busyEnd = new Date(usage.end)
        return (reqStart < busyEnd && reqEnd > busyStart)
      })

      return !hasConflict
    })
  }

  filteredPcs.value = result
}

function refresh() {
  selectedPc.value = null
  fetchPcs() 
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
/* Стили без изменений */
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