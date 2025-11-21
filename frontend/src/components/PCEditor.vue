<template>
  <div class="pc-editor glass-card fade-in">

    <h3 class="title">{{ pc.id ? "Изменить ПК" : "Создать ПК" }}</h3>

    <!-- CPU -->
    <div class="form-group">
      <label>CPU</label>
      <select v-model.number="pc.cpu_id">
        <option disabled value="">Выберите CPU</option>
        <option v-for="c in cpus" :key="c.id" :value="c.id">
          {{ c.name }}
        </option>
      </select>
    </div>

    <!-- GPU -->
    <div class="form-group">
      <label>GPU</label>
      <select v-model.number="pc.gpu_id">
        <option disabled value="">Выберите GPU</option>
        <option v-for="g in gpus" :key="g.id" :value="g.id">
          {{ g.name }}
        </option>
      </select>
    </div>

    <!-- OS -->
    <div class="form-group">
      <label>OS</label>
      <select v-model.number="pc.os_id">
        <option disabled value="">Выберите OS</option>
        <option v-for="o in oses" :key="o.id" :value="o.id">
          {{ o.name }}
        </option>
      </select>
    </div>

    <!-- Buttons -->
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

const pc = ref({
  cpu_id: "",
  gpu_id: "",
  os_id: "",
  ...props.modelValue
})

const cpus = ref([])
const gpus = ref([])
const oses = ref([])

async function load() {
  cpus.value = (await api.get('/api/admin/cpus')).data
  gpus.value = (await api.get('/api/admin/gpus')).data
  oses.value = (await api.get('/api/admin/oses')).data
}

function savePc() {
  const payload = {
    cpu_id: pc.value.cpu_id || null,
    gpu_id: pc.value.gpu_id || null,
    os_id: pc.value.os_id || null
  }

  // Если редактирование — добавляем id
  if (pc.value.id) payload.id = pc.value.id

  emit("save", payload)
}

onMounted(load)

watch(() => props.modelValue, newVal => {
  pc.value = { ...newVal }
})
</script>

<style scoped>
.pc-editor {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

select, input {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  margin-top: 5px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.15);
  color: white;
}

.actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.btn-primary {
  padding: 10px 16px;
  background: var(--primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-secondary {
  padding: 10px 16px;
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 6px;
  cursor: pointer;
}
</style>
