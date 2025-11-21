<template>
  <div class="admin-dashboard">
    <aside class="sidebar">
      <button 
        v-for="item in menu" 
        :key="item.key"
        :class="{ active: active === item.key }"
        @click="active = item.key"
      >
        {{ item.label }}
      </button>
    </aside>

    <section class="content">
      <AdminCrudTable
        v-if="active === 'pcs'"
        title="Компьютеры"
        apiPath="/api/admin/pcs"
        :columns="['cpu_id','gpu_id','os_id']"
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
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AdminCrudTable from '../components/AdminCrudTable.vue'

const menu = [
  { key: 'pcs', label: 'Компьютеры' },
  { key: 'tariffs', label: 'Тарифы' },
  { key: 'cpu', label: 'CPU' },
  { key: 'gpu', label: 'GPU' },
  { key: 'os', label: 'ОС' },
]

const active = ref('pcs')
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  height: calc(100vh - 60px);
}

.sidebar {
  width: 200px;
  background: #222;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar button {
  background: #333;
  border: 1px solid #444;
  padding: 10px;
  color: white;
  cursor: pointer;
  text-align: left;
}

.sidebar button.active {
  background: #555;
  border-left: 4px solid #00b4ff;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
