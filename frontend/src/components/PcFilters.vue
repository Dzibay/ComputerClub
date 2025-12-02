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
        <label>Игра / Программа</label>
        <select v-model="software">
          <option value="">Любая</option>
          <option v-for="s in softwareList" :key="s.id" :value="s.id">{{ s.name }}</option>
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
import { useCabinetStore } from '../store/cabinet'

const cabinetStore = useCabinetStore()

// Данные из стора
const cpus = cabinetStore.dictionaries.cpus
const gpus = cabinetStore.dictionaries.gpus
const oses = cabinetStore.dictionaries.oses

// Локальный список софта (загружаем отдельно, если его нет в сторе)
const softwareList = ref([])

// Модели фильтров
const cpu = ref('')
const gpu = ref('')
const os = ref('')
const software = ref('') // Новое поле
const date = ref('')
const hours = ref(1)

const emit = defineEmits(['apply'])

async function loadSoftware() {
  try {
    const res = await api.get('/api/admin/software')
    softwareList.value = res.data
  } catch (e) {
    console.error("Ошибка загрузки списка ПО", e)
  }
}

function applyFilters() {
  const filters = {
    cpu_id: cpu.value || undefined,
    gpu_id: gpu.value || undefined,
    os_id: os.value || undefined,
    software_id: software.value || undefined, // Передаем ID софта
    filter_date: date.value || undefined,
    filter_hours: hours.value || undefined
  }
  emit('apply', filters)
}

onMounted(() => {
  loadSoftware()
})
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

.field label {
  display: block;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.4rem;
}

.field select, .field input {
  width: 100%;
  padding: 0.7rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-glass);
  border-radius: 6px;
  color: white;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.field select:focus, .field input:focus {
  border-color: var(--primary);
  outline: none;
}

.field.small {
  flex: 0 0 80px; 
  min-width: 80px;
}

.full-btn {
  width: 100%;
  height: 44px; /* Чуть подкорректировал высоту */
  margin-bottom: 1px;
}

input[type="datetime-local"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}
</style>