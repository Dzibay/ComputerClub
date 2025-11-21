<template>
  <div class="filters">
    <h3>Фильтры</h3>

    <label>CPU</label>
    <select v-model="cpu">
      <option value="">Любой</option>
      <option v-for="c in cpus" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>

    <label>GPU</label>
    <select v-model="gpu">
      <option value="">Любой</option>
      <option v-for="g in gpus" :key="g.id" :value="g.id">{{ g.name }}</option>
    </select>

    <label>OS</label>
    <select v-model="os">
      <option value="">Любая</option>
      <option v-for="o in oses" :key="o.id" :value="o.id">{{ o.name }}</option>
    </select>

    <label>Дата</label>
    <input type="datetime-local" v-model="date" />

    <label>Количество часов</label>
    <input type="number" min="1" v-model="hours" />

    <button @click="applyFilters">
      Применить
    </button>
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
.filters {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 280px;
  padding: 10px;
  border: 1px solid #ccc;
}
</style>
