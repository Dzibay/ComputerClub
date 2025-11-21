<template>
  <div class="cabinet-layout fade-in">
    <div v-if="cabinetStore.isLoading" class="loading-overlay">
      Загрузка кабинета...
    </div>

    <template v-else>
      <aside class="sidebar glass-panel">
        <div class="profile-block" v-if="cabinetStore.user">
          <div class="avatar-placeholder">
            {{ cabinetStore.user.full_name.charAt(0).toUpperCase() }}
          </div>
          <h3 class="username">{{ cabinetStore.user.full_name }}</h3>
          <p class="balance-badge">
            {{ cabinetStore.user.balance }} ₽
          </p>
        </div>

        <nav class="nav-menu">
          <RouterLink to="/cabinet" exact-active-class="active">
            <span class="icon">🏠</span> Главная
          </RouterLink>
          <RouterLink to="/cabinet/bookings" active-class="active">
            <span class="icon">🎮</span> Бронирование
          </RouterLink>
          </nav>
      </aside>

      <main class="content glass-card">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </template>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCabinetStore } from '../store/cabinet'

const cabinetStore = useCabinetStore()

// Загружаем всё при входе в Layout
onMounted(() => {
  cabinetStore.initCabinet()
})
</script>

<style scoped>
/* Ваши стили + стиль лоадера */
.loading-overlay {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.2rem;
  color: var(--text-muted);
}

/* --- Layout Grid --- */
.cabinet-layout {
  display: grid;
  grid-template-columns: 280px 1fr; /* Фиксированное меню, гибкий контент */
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 3rem 1rem;
  min-height: 80vh;
}

/* --- Sidebar --- */
.sidebar {
  padding: 1.5rem;
  height: fit-content;
  position: sticky;
  top: 100px; /* Отступ от верха экрана при скролле */
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* --- Profile Block --- */
.profile-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-glass);
}

.avatar-placeholder {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary), #4f46e5);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
}

.username {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-main);
}

.balance-badge {
  background: rgba(16, 185, 129, 0.1);
  color: #34d399;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

/* --- Navigation Menu --- */
.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-menu a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  color: var(--text-muted);
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.nav-menu a .icon {
  font-size: 1.2rem;
  filter: grayscale(100%); /* Иконки серые неактивные */
  transition: filter 0.3s;
}

/* Hover State */
.nav-menu a:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
  transform: translateX(5px); /* Легкий сдвиг вправо */
}

.nav-menu a:hover .icon {
  filter: grayscale(0%);
}

/* Active State */
.nav-menu a.active {
  background: var(--primary);
  color: white;
  box-shadow: var(--glow);
  border-color: rgba(255, 255, 255, 0.1);
}

.nav-menu a.active .icon {
  filter: grayscale(0%);
}

/* --- Content Area --- */
.content {
  padding: 2rem;
  min-height: 500px; /* Чтобы футер не прилипал на пустых страницах */
}

/* Анимация перехода между вкладками внутри кабинета */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* --- Mobile Responsive --- */
@media (max-width: 768px) {
  .cabinet-layout {
    grid-template-columns: 1fr; /* Одна колонка */
    gap: 1.5rem;
  }

  .sidebar {
    position: static; /* Отключаем липкость на мобильных */
    flex-direction: row; /* Горизонтальная ориентация если нужно */
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
  }
  
  .profile-block {
    border-bottom: none;
    padding-bottom: 0;
    flex-direction: row;
    gap: 1rem;
    margin-bottom: 0;
  }
  
  .avatar-placeholder {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
    margin-bottom: 0;
  }

  .nav-menu {
    width: 100%;
    margin-top: 1rem;
    flex-direction: row;
    overflow-x: auto; /* Горизонтальный скролл меню */
    padding-bottom: 5px;
  }

  .nav-menu a {
    white-space: nowrap; /* Текст не переносится */
    padding: 0.6rem 1rem;
  }
  
  .nav-menu a:hover {
    transform: none;
  }
}
</style>