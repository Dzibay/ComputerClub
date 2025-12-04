<template>
  <div class="admin-dashboard fade-in">
    
    <aside class="sidebar glass-panel">
      <div class="sidebar-header">
        <h3>Admin Panel</h3>
      </div>

      <div class="menu-list">
        <button 
          v-for="item in menu" 
          :key="item.key"
          class="nav-btn"
          :class="{ active: active === item.key }"
          @click="active = item.key"
        >
          <span class="indicator"></span>
          {{ item.label }}
        </button>
      </div>
    </aside>

    <section class="content glass-card">
      <transition name="fade" mode="out-in">
        <div :key="active" class="table-wrapper">
          <AdminCrudTable
            v-if="active === 'pcs'"
            title="Компьютеры"
            apiPath="/api/admin/pcs"
            :columns="['id', 'cpu_name', 'gpu_name', 'os_name']" 
            :hasSoftwareSelect="true" 
          />
          <AdminCrudTable
            v-if="active === 'tariffs'"
            title="Тарифы"
            apiPath="/api/admin/tariffs"
            :columns="['name','price_per_hour','hours_number','description']"
          />

          <AdminCrudTable
            v-if="active === 'cpu'"
            title="CPU"
            apiPath="/api/admin/cpus"
            :columns="['name']"
          />

          <AdminCrudTable
            v-if="active === 'gpu'"
            title="GPU"
            apiPath="/api/admin/gpus"
            :columns="['name']"
          />

          <AdminCrudTable
            v-if="active === 'os'"
            title="Операционные системы"
            apiPath="/api/admin/oses"
            :columns="['name']"
          />

          <AdminCrudTable
            v-if="active === 'software'"
            title="Программное обеспечение"
            apiPath="/api/admin/software"
            :columns="['name']"
          />
        </div>
      </transition>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminCrudTable from '../components/AdminCrudTable.vue'

const menu = [
  { key: 'pcs', label: 'Компьютеры' },
  { key: 'tariffs', label: 'Тарифы' },
  { key: 'cpu', label: 'Процессоры' },
  { key: 'gpu', label: 'Видеокарты' },
  { key: 'os', label: 'ОС' },
  { key: 'software', label: 'Игры и ПО' },
]

const active = ref('pcs')
</script>

<style scoped>
.sidebar-header {
  padding: 0 1rem 1.5rem 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-glass);
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 1rem 1.2rem;
  border: none;
  background: transparent;
  color: var(--text-muted);
  text-align: left;
  cursor: pointer;
  font-size: 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-main);
  padding-left: 1.5rem;
}

.nav-btn.active {
  background: var(--primary);
  color: white;
  box-shadow: var(--glow);
}

.indicator {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  margin-right: 10px;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
}

.nav-btn.active .indicator {
  opacity: 1;
  transform: scale(1);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>