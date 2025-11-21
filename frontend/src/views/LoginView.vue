<template>
  <div>
    <h2>Вход</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Пароль" />

    <button @click="submit">Войти</button>

    <div v-if="error" class="error">{{ error }}</div>
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
.error {
  color: red;
  margin-top: 10px;
}
</style>
