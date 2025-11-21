<script setup>
import { useAuthStore } from './store/auth'
import { ref, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import './style.css'

const auth = useAuthStore()
const loading = ref(true)

onMounted(async () => {
  await auth.restore()
  loading.value = false
})
</script>

<template>
  <div v-if="!loading">
    <Navbar />
    <router-view />
  </div>

  <div v-else>
    Загрузка...
  </div>
</template>

