<template>
  <div class="pc-editor glass-card fade-in">

    <h3 class="title">{{ pc.id ? "Изменить ПК" : "Создать ПК" }}</h3>

    <div class="editor-grid">
      <div class="hardware-col">
        <div class="form-group">
          <label>CPU</label>
          <select v-model.number="pc.cpu_id">
            <option disabled value="">Выберите CPU</option>
            <option v-for="c in cpus" :key="c.id" :value="c.id">
              {{ c.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>GPU</label>
          <select v-model.number="pc.gpu_id">
            <option disabled value="">Выберите GPU</option>
            <option v-for="g in gpus" :key="g.id" :value="g.id">
              {{ g.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>OS</label>
          <select v-model.number="pc.os_id">
            <option disabled value="">Выберите OS</option>
            <option v-for="o in oses" :key="o.id" :value="o.id">
              {{ o.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="software-col">
        <label>Установленные программы</label>
        <div class="software-list custom-scroll">
          <div 
            v-for="sw in softwareList" 
            :key="sw.id" 
            class="checkbox-item"
            :class="{ active: selectedSoftware.includes(sw.id) }"
            @click="toggleSoftware(sw.id)"
          >
            <div class="custom-checkbox">
              <span v-if="selectedSoftware.includes(sw.id)">✔</span>
            </div>
            {{ sw.name }}
          </div>
        </div>
      </div>
    </div>

    <div class="actions">
      <button class="btn-primary" @click="savePc">Сохранить</button>
      <button class="btn-secondary" @click="$emit('cancel')">Отмена</button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../api/axios'

const props = defineProps({
  modelValue: Object
})

const emit = defineEmits(["save", "cancel"])

// Основные данные ПК
const pc = ref({
  cpu_id: "",
  gpu_id: "",
  os_id: "",
  ...props.modelValue
})

// Массив ID выбранных программ
const selectedSoftware = ref([])

// Справочники
const cpus = ref([])
const gpus = ref([])
const oses = ref([])
const softwareList = ref([])

async function load() {
  // Загружаем все справочники параллельно
  const [resCpu, resGpu, resOs, resSw] = await Promise.all([
    api.get('/api/admin/cpus'),
    api.get('/api/admin/gpus'),
    api.get('/api/admin/oses'),
    api.get('/api/admin/software')
  ])

  cpus.value = resCpu.data
  gpus.value = resGpu.data
  oses.value = resOs.data
  softwareList.value = resSw.data

  initForm(props.modelValue)
}

// Инициализация формы данными
function initForm(data) {
  if (!data) return
  
  pc.value = { ...data }

  // Если у ПК есть список софта (приходит с бэка как массив объектов pc_software),
  // нам нужно вытащить оттуда ID программ.
  if (data.pc_software && Array.isArray(data.pc_software)) {
    // Структура с бэка: [{ software: { id: 1, name: '...' } }, ...]
    selectedSoftware.value = data.pc_software.map(item => item.software.id)
  } else {
    selectedSoftware.value = []
  }
}

function toggleSoftware(id) {
  const index = selectedSoftware.value.indexOf(id)
  if (index === -1) {
    selectedSoftware.value.push(id)
  } else {
    selectedSoftware.value.splice(index, 1)
  }
}

function savePc() {
  const payload = {
    cpu_id: pc.value.cpu_id || null,
    gpu_id: pc.value.gpu_id || null,
    os_id: pc.value.os_id || null,
    software_ids: selectedSoftware.value // Отправляем массив ID
  }

  if (pc.value.id) payload.id = pc.value.id

  emit("save", payload)
}

onMounted(load)

watch(() => props.modelValue, newVal => {
  initForm(newVal)
})
</script>

<style scoped>
.pc-editor {
  padding: 20px;
}

.title {
  margin-bottom: 1.5rem;
  color: var(--primary);
  text-transform: uppercase;
}

.editor-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 15px;
}

select, input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  margin-top: 5px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.15);
  color: white;
  outline: none;
}
select:focus { border-color: var(--primary); }

/* --- Software Checkbox List Styles --- */
.software-col {
  display: flex;
  flex-direction: column;
}

.software-list {
  flex-grow: 1;
  max-height: 250px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 6px;
  padding: 0.5rem;
  margin-top: 5px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  cursor: pointer;
  transition: background 0.2s;
  border-radius: 4px;
}

.checkbox-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.checkbox-item.active {
  background: rgba(99, 102, 241, 0.15);
}

.custom-checkbox {
  width: 18px;
  height: 18px;
  border: 1px solid var(--text-muted);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--primary);
}

.active .custom-checkbox {
  border-color: var(--primary);
  background: rgba(99, 102, 241, 0.2);
}

/* --- Actions --- */
.actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-primary {
  padding: 10px 20px;
  background: var(--primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: white;
  font-weight: 600;
}

.btn-secondary {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid var(--border-glass);
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-muted);
}
.btn-secondary:hover { color: white; border-color: white; }

/* Custom Scrollbar */
.custom-scroll::-webkit-scrollbar { width: 6px; }
.custom-scroll::-webkit-scrollbar-track { background: transparent; }
.custom-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }

@media (max-width: 600px) {
  .editor-grid { grid-template-columns: 1fr; }
}
</style>