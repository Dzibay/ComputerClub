<template>
  <div class="crud-container">

    <div class="crud-header">
      <h2 class="section-title">{{ title }}</h2>
      <button class="btn-primary create-btn" @click="createNew">
        <span>+</span> Добавить
      </button>
    </div>

    <div class="table-responsive">
      <table class="crud-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col">{{ formatColName(col) }}</th>
            <th class="actions-col">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td v-for="col in columns" :key="col">
              {{ row[col] !== null ? row[col] : '—' }}
            </td>
            <td class="actions-cell">
              <button class="action-btn edit" @click="editRow(row)" title="Редактировать">
                ✎
              </button>
              <button class="action-btn delete" @click="deleteRow(row.id)" title="Удалить">
                🗑
              </button>
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td :colspan="columns.length + 1" class="empty-row">
              Нет данных для отображения
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="editing" class="modal-backdrop fade-in" @click.self="editing = null">
      <div class="modal-content glass-card">
        
        <div class="modal-header">
          <h3>{{ editing.id ? "Редактирование" : "Создание" }}</h3>
          <button class="close-btn" @click="editing = null">×</button>
        </div>

        <PCEditor
          v-if="props.apiPath === '/api/admin/pcs'"
          :modelValue="editing"
          @save="savePC"
          @cancel="editing = null"
        />

        <div v-else class="generic-form">
          <div v-for="col in columns" :key="col" class="form-group">
            <label>{{ formatColName(col) }}</label>
            <input v-model="editing[col]" :placeholder="'Введите ' + col" />
          </div>

          <div class="modal-actions">
            <button class="btn-outline" @click="editing = null">Отмена</button>
            <button class="btn-primary" @click="save">Сохранить</button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/axios'
import PCEditor from './PCEditor.vue'

const props = defineProps({
  apiPath: String,
  title: String,
  columns: Array
})

const rows = ref([])
const editing = ref(null)

// Форматирование названий колонок (убираем _id, делаем красивее)
function formatColName(col) {
  if (col === 'price_per_hour') return 'Цена/час'
  if (col === 'hours_number') return 'Часы'
  if (col.endsWith('_id')) return col.replace('_id', '').toUpperCase()
  return col.charAt(0).toUpperCase() + col.slice(1)
}

async function load() {
  try {
    rows.value = (await api.get(props.apiPath)).data
  } catch (e) {
    console.error("Ошибка загрузки:", e)
  }
}

function createNew() {
  const obj = {}
  for (const col of props.columns) {
    if (col.endsWith("_id")) {
      obj[col] = null
    } else {
      obj[col] = ""
    }
  }
  editing.value = obj
}

function editRow(row) {
  editing.value = { ...row }
}

async function deleteRow(id) {
  if(!confirm('Вы уверены, что хотите удалить эту запись?')) return
  await api.delete(`${props.apiPath}/${id}`)
  load()
}

async function save() {
  try {
    if (editing.value.id) {
      await api.put(`${props.apiPath}/${editing.value.id}`, editing.value)
    } else {
      await api.post(props.apiPath, editing.value)
    }
    editing.value = null
    load()
  } catch (e) {
    alert('Ошибка сохранения: ' + (e.response?.data?.error || e.message))
  }
}

async function savePC(pc) {
  try {
    if (pc.id) {
      await api.put(`${props.apiPath}/${pc.id}`, pc)
    } else {
      await api.post(props.apiPath, pc)
    }
    editing.value = null
    load()
  } catch (e) {
    alert('Ошибка сохранения ПК: ' + (e.response?.data?.error || e.message))
  }
}

onMounted(load)
</script>

<style scoped>
.crud-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.crud-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.create-btn {
  padding: 0.5rem 1.2rem;
  font-size: 0.9rem;
  gap: 0.5rem;
}

/* --- Table Styles --- */
.table-responsive {
  overflow-x: auto;
}

.crud-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.crud-table th {
  text-align: left;
  padding: 1rem;
  color: var(--text-muted);
  font-weight: 500;
  border-bottom: 1px solid var(--border-glass);
  white-space: nowrap;
}

.crud-table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  color: var(--text-main);
}

.crud-table tr:hover td {
  background: rgba(255,255,255,0.02);
}

.actions-col {
  text-align: right;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: var(--transition);
}

.action-btn.edit {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary);
}
.action-btn.edit:hover { background: var(--primary); color: white; }

.action-btn.delete {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}
.action-btn.delete:hover { background: var(--danger); color: white; }

.empty-row {
  text-align: center;
  padding: 2rem;
  color: var(--text-muted);
  font-style: italic;
}

/* --- Modal Overlay --- */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  background: #1e2230;
  border: 1px solid var(--border-glass);
  padding: 2rem;
  border-radius: var(--radius);
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.5rem;
  cursor: pointer;
}
.close-btn:hover { color: white; }

.generic-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1.2rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
</style>