<template>
  <div>
    <h2>Личный кабинет</h2>

    <div v-if="profile">
      <p>Имя: {{ profile.user.full_name }}</p>
      <p>Баланс: {{ profile.user.balance }}₽</p>

      <div v-if="profile.active_booking">
        <h3>Активная бронь</h3>
        <p>ПК: {{ profile.active_booking.pc_id }}</p>
        <p>Начало: {{ profile.active_booking.start_time }}</p>

        <button @click="cancel(profile.active_booking.id)">Отменить</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/axios'

const profile = ref(null)

async function load() {
  const { data } = await api.get('/api/cabinet')
  profile.value = data
}

async function cancel(id) {
  await api.post('/api/cabinet/cancel', { booking_id: id })
  load()
}

onMounted(load)
</script>
