<template>
  <div>
    <h2>Регистрация</h2>

    <input v-model="full_name" placeholder="Имя" />
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Пароль" />

    <button @click="submit">Зарегистрироваться</button>

    <p v-if="done">Регистрация успешна!</p>
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
