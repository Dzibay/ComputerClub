<template>
  <div class="booking-form glass-card fade-in">

    <h3 class="title">Бронирование ПК #{{ pc.id }}</h3>

    <div class="form-group">
      <label>Тариф</label>
      <select v-model="tariff">
        <option value="" disabled>Выбери тариф</option>
        <option v-for="t in tariffs" :key="t.id" :value="t">
          {{ t.name }} — {{ t.price_per_hour }}₽/час
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>Начало</label>
      <input type="datetime-local" v-model="startTime" />
    </div>

    <div class="form-group">
      <label>Количество часов</label>
      <input type="number" min="1" v-model="hours" />
    </div>

    <button class="btn-primary submit-btn" @click="book">
      Забронировать
    </button>

    <p v-if="msg" class="msg success glass-card">{{ msg }}</p>
    <p v-if="err" class="msg error glass-card">{{ err }}</p>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/axios'

const props = defineProps({
  pc: Object
})

const tariffs = ref([])
const tariff = ref(null)
const startTime = ref('')
const hours = ref(1)

const msg = ref('')
const err = ref('')

async function loadTariffs() {
  tariffs.value = (await api.get('/api/admin/tariffs')).data
}

async function book() {
  msg.value = ''
  err.value = ''

  try {
    await api.post('/api/bookings', {
      pc_id: props.pc.id,
      tariff_id: tariff.value.id,
      start_time: startTime.value,
      duration_hours: hours.value
    })

    msg.value = 'Бронь успешно создана!'
    emit('created')
  } catch (e) {
    err.value = e.response?.data?.error || 'Ошибка бронирования'
  }
}

const emit = defineEmits(['created'])
onMounted(loadTariffs)
</script>

<style scoped>

</style>
