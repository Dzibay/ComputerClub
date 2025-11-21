<template>
  <div class="filters-container">
    <div class="filter-header">
      <h3>🚀 Поиск станции</h3>
      <span class="filter-hint">Настройте параметры под себя</span>
    </div>

    <div class="filters-grid">
      <div class="field">
        <label>Процессор (CPU)</label>
        <select v-model="cpu">
          <option value="">Все модели</option>
          <option v-for="c in cpus" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <div class="field">
        <label>Видеокарта (GPU)</label>
        <select v-model="gpu">
          <option value="">Все карты</option>
          <option v-for="g in gpus" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
      </div>

      <div class="field">
        <label>Операционка</label>
        <select v-model="os">
          <option value="">Любая OS</option>
          <option v-for="o in oses" :key="o.id" :value="o.id">{{ o.name }}</option>
        </select>
      </div>

      <div class="field">
        <label>Дата и время</label>
        <input type="datetime-local" v-model="date" class="date-input" />
      </div>

      <div class="field small">
        <label>Часы</label>
        <input type="number" min="1" max="12" v-model="hours" />
      </div>

      <div class="field action">
        <button class="btn-primary full-btn" @click="applyFilters">
          Найти
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/axios'

const cpus = ref([])
const gpus = ref([])
const oses = ref([])

const cpu = ref('')
const gpu = ref('')
const os = ref('')
const date = ref('')
const hours = ref(1)

async function load() {
  cpus.value = (await api.get('/api/admin/cpus')).data
  gpus.value = (await api.get('/api/admin/gpus')).data
  oses.value = (await api.get('/api/admin/oses')).data
}

function applyFilters() {
  const filters = {
    cpu_id: cpu.value || undefined,
    gpu_id: gpu.value || undefined,
    os_id: os.value || undefined,
    filter_date: date.value || undefined,
    filter_hours: hours.value || undefined
  }
  emit('apply', filters)
}

const emit = defineEmits(['apply'])
onMounted(load)
</script>

<style scoped>
.filter-header {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.filter-hint {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.2rem;
  align-items: end;
}

.field.small {
  flex: 0 0 80px; /* Узкое поле для часов */
  min-width: 80px;
}

.full-btn {
  width: 100%;
  height: 46px; /* Высота чтобы совпадать с инпутами */
  margin-bottom: 1rem; /* Компенсация margin-bottom у инпутов */
}

/* Убираем иконку календаря в Chrome для темной темы */
input[type="datetime-local"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}
</style>