<template>
  <div>
    <h3>{{ pc.id ? "Изменить ПК" : "Создать ПК" }}</h3>

    <label>CPU</label>
    <select v-model="pc.cpu_id">
      <option v-for="c in cpus" :key="c.id" :value="c.id">
        {{ c.name }}
      </option>
    </select>

    <label>GPU</label>
    <select v-model="pc.gpu_id">
      <option v-for="g in gpus" :key="g.id" :value="g.id">
        {{ g.name }}
      </option>
    </select>

    <label>OS</label>
    <select v-model="pc.os_id">
      <option v-for="o in oses" :key="o.id" :value="o.id">
        {{ o.name }}
      </option>
    </select>

    <button @click="$emit('save', pc)">Сохранить</button>
    <button @click="$emit('cancel')">Отмена</button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../api/axios'

const props = defineProps({
  modelValue: Object
})

const pc = ref({ ...props.modelValue })

const cpus  = ref([])
const gpus  = ref([])
const oses  = ref([])

async function load() {
  cpus.value = (await api.get('/api/admin/cpus')).data
  gpus.value = (await api.get('/api/admin/gpus')).data
  oses.value = (await api.get('/api/admin/oses')).data
}

onMounted(load)

watch(() => props.modelValue, newVal => {
  pc.value = { ...newVal }
})
</script>

<style scoped>
label {
  display: block;
  margin-top: 10px;
}
select {
  width: 100%;
  margin-bottom: 10px;
}
</style>
