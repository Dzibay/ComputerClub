<template>
  <div class="cabinet-layout">

    <!-- Боковое меню -->
    <aside class="sidebar">
      <div class="profile-block" v-if="user">
        <h3>{{ user.full_name }}</h3>
        <p class="balance">Баланс: {{ user.balance }}₽</p>
      </div>

      <nav>
        <RouterLink to="/cabinet" exact-active-class="active">Главная</RouterLink>
        <RouterLink to="/cabinet/bookings" exact-active-class="active">Бронирование</RouterLink>
        <RouterLink to="/cabinet/payments" exact-active-class="active">Платежи</RouterLink>
        <RouterLink to="/cabinet/settings" exact-active-class="active">Настройки</RouterLink>
      </nav>
    </aside>

    <!-- Основной контент -->
    <main class="content">
      <router-view />
    </main>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()

// берём пользователя из auth
const user = computed(() => auth.user)
</script>

<style scoped>
.cabinet-layout {
  display: flex;
  height: calc(100vh - 60px);
}

.sidebar {
  width: 240px;
  background: #202831;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.profile-block {
  margin-bottom: 20px;
}

.balance {
  margin-top: 4px;
  font-size: 14px;
  opacity: 0.7;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

nav a {
  text-decoration: none;
  color: #cfd8dc;
  padding: 8px 12px;
  border-radius: 6px;
}

nav a.active {
  background: #3fa9f5;
  color: white;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
