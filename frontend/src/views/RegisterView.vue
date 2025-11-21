<template>
  <div class="auth-page fade-in">
    <div class="glass-card auth-form">
      <h2 class="title">Регистрация</h2>
      <p class="subtitle">Создайте аккаунт для бронирования</p>

      <div v-if="!done" class="form-group">
        <label>Ваше имя</label>
        <input v-model="full_name" placeholder="Иван Иванов" />

        <label>Email</label>
        <input v-model="email" placeholder="user@example.com" />

        <label>Пароль</label>
        <input v-model="password" type="password" placeholder="••••••••" />

        <button class="btn-primary full-width" @click="submit">
          Зарегистрироваться
        </button>
      </div>

      <div v-else class="success-message">
        <h3>Успешно!</h3>
        <p>Теперь вы можете войти в систему.</p>
        <router-link to="/login" class="btn-outline full-width">
          Перейти ко входу
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const email = ref('')
const full_name = ref('')
const password = ref('')
const done = ref(false)

async function submit() {
  await auth.register({
    full_name: full_name.value,
    email: email.value,
    password: password.value
  })
  done.value = true
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 1rem;
}

.auth-form {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
}

.subtitle {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  margin-top: -0.5rem;
  font-size: 0.9rem;
}

.full-width {
  width: 100%;
  margin-top: 1rem;
}

.success-message {
  text-align: center;
  color: #34d399;
}
</style>