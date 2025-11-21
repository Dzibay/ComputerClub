<template>
  <div class="cabinet-page fade-in">
    <h2 class="page-title">Личный кабинет</h2>

    <div v-if="profile" class="cabinet-wrapper">

      <div class="glass-card user-card">
        <h3 class="section-title">👤 Профиль</h3>
        
        <div class="card-content">
          <div class="info-block">
            <span class="label">Имя игрока</span>
            <span class="value highlight">{{ profile.user.full_name }}</span>
          </div>

          <div class="info-block">
            <span class="label">Текущий баланс</span>
            <span class="value balance">{{ profile.user.balance }} ₽</span>
          </div>
        </div>
      </div>

      <div class="glass-card booking-card" :class="{ 'active-glow': profile.active_booking }">
        <h3 class="section-title">🎮 Активная сессия</h3>

        <div v-if="profile.active_booking" class="booking-details">
          <div class="row">
            <span class="label">Компьютер:</span>
            <span class="value">PC #{{ profile.active_booking.pc_id }}</span>
          </div>
          <div class="row">
            <span class="label">Начало:</span>
            <span class="value">{{ new Date(profile.active_booking.start_time).toLocaleString() }}</span>
          </div>

          <button class="btn-danger cancel-btn" @click="cancel(profile.active_booking.id)">
            Отменить бронь
          </button>
        </div>

        <div v-else class="empty-state">
          <p>Сейчас вы не играете.</p>
          <router-link to="/booking" class="btn-outline small">Забронировать</router-link>
        </div>
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

<style scoped>
.cabinet-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.user-card, .booking-card {
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-block {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 0.3rem;
}

.value {
  font-size: 1.2rem;
  font-weight: 600;
}

.balance { color: #34d399; font-size: 1.5rem; }
.highlight { color: var(--primary); }

.booking-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}

.row {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-glass);
  padding-bottom: 0.5rem;
}

.cancel-btn {
  margin-top: auto;
  width: 100%;
}

.empty-state {
  color: var(--text-muted);
  text-align: center;
  padding: 1rem 0;
}
.active-glow {
  border-color: var(--primary);
  box-shadow: var(--glow);
}
</style>