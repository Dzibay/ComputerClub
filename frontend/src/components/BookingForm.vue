<template>
  <div class="booking-form">
    <h3>Бронирование ПК #{{ pc.id }}</h3>

    <label>Тариф</label>
    <select v-model="tariff">
      <option value="" disabled>Выбери тариф</option>
      <option v-for="t in tariffs" :key="t.id" :value="t">
        {{ t.name }} — {{ t.price_per_hour }}₽/час
      </option>
    </select>

    <label>Начало</label>
    <input type="datetime-local" v-model="startTime" />

    <label>Количество часов</label>
    <input type="number" min="1" v-model="hours" />

    <button @click="book">Забронировать</button>

    <p v-if="msg" class="msg">{{ msg }}</p>
    <p v-if="err" class="err">{{ err }}</p>
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

    msg.value = 'Бронь успешно создана'
    emit('created')
  } catch (e) {
    err.value = e.response?.data?.error || 'Ошибка'
  }
}

const emit = defineEmits(['created'])
onMounted(loadTariffs)
</script>

<style scoped>
.booking-form {
  margin-top: 20px;
  padding: 15px;
  max-width: 350px;
  border: 1px solid #ccc;
}
.msg {
  color: green;
}
.err {
  color: red;
}
</style>
