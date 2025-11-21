<template>
  <div class="auth-page fade-in">
    <div class="glass-card auth-form">
      <h2>Вход</h2>
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Пароль" />

      <button @click="submit">Войти</button>

      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref(null)

async function submit() {
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.error || 'Ошибка входа'
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}
.auth-form {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}
</style>
