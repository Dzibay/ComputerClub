<template>
  <nav class="navbar glass-nav fade-in">
    <router-link to="/" class="logo">
      <span class="logo-main">CYBER</span>
      <span class="logo-sub">CLUB</span>
    </router-link>

    <div class="links">
      <router-link to="/" class="nav-link">Главная</router-link>

      <template v-if="auth.isAuthenticated">
        <router-link to="/cabinet" class="nav-link">Кабинет</router-link>
        
        <router-link 
          v-if="auth.user?.role === 'Admin'" 
          to="/admin" 
          class="nav-link admin-link"
        >
          Админ
        </router-link>

        <button class="btn-outline logout-btn" @click="logout">
          Выход
        </button>
      </template>

      <template v-else>
        <router-link to="/login" class="nav-link">Вход</router-link>
        <router-link to="/register" class="btn-primary nav-btn">
          Регистрация
        </router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
/* Специфичные отступы для навбара, если глобальных мало */
.logout-btn {
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  margin-left: 1rem;
}

.admin-link {
  color: #fbbf24; /* Amber 400 */
  position: relative;
}

.admin-link::after {
  content: '•';
  position: absolute;
  top: -5px;
  right: -8px;
  color: #fbbf24;
  font-size: 1.2rem;
}
</style>