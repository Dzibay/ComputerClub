<template>
  <nav class="navbar">
    <router-link to="/" class="logo">Computer Club</router-link>

    <div class="links">
      <router-link to="/">Главная</router-link>

      <template v-if="auth.isAuthenticated">
        <router-link to="/cabinet">Личный кабинет</router-link>

        <router-link
          v-if="auth.user?.role === 'Admin'"
          to="/admin"
        >Админ</router-link>

        <button class="logout" @click="logout">Выход</button>
      </template>

      <template v-else>
        <router-link to="/login">Вход</router-link>
        <router-link to="/register">Регистрация</router-link>
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
.navbar {
  background: #222;
  color: white;
  padding: 10px 20px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar .logo {
  color: white;
  font-weight: bold;
  font-size: 20px;
  text-decoration: none;
}

.links {
  display: flex;
  gap: 15px;
  align-items: center;
}

a {
  color: #ddd;
  text-decoration: none;
}

a.router-link-active {
  color: white;
}

.logout {
  background: transparent;
  border: 1px solid #bbb;
  padding: 4px 10px;
  color: #eee;
  cursor: pointer;
}

.logout:hover {
  background: #444;
}
</style>
