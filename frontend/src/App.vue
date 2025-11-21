<script setup>
import { useAuthStore } from './store/auth'
import { ref, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'

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


<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>
