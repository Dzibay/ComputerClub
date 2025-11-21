<template>
  <div>

    <h2>{{ title }}</h2>

    <button @click="createNew">Добавить</button>

    <table class="crud-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col">{{ col }}</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td v-for="col in columns" :key="col">{{ row[col] }}</td>
          <td>
            <button @click="editRow(row)">✎</button>
            <button @click="deleteRow(row.id)">🗑</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма редактирования -->
    <div v-if="editing" class="modal">

    <!-- Индивидуальный редактор ПК -->
    <PCEditor
        v-if="props.apiPath === '/api/admin/pcs'"
        :modelValue="editing"
        @save="savePC"
        @cancel="editing = null"
    />

    <!-- Универсальный редактор -->
    <div v-else>
        <h3>{{ editing.id ? "Изменить" : "Создать" }}</h3>

        <div v-for="col in columns" :key="col">
        <label>{{ col }}</label>
        <input v-model="editing[col]" />
        </div>

        <button @click="save">Сохранить</button>
        <button @click="editing=null">Отмена</button>
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

async function load() {
  rows.value = (await api.get(props.apiPath)).data
}

function createNew() {
  const obj = {}

  for (const col of props.columns) {
    if (col.endsWith("_id")) {
      obj[col] = null         // для полей id
    } else {
      obj[col] = ""           // для текстовых полей
    }
  }

  editing.value = obj
}



function editRow(row) {
  editing.value = { ...row }
}

async function deleteRow(id) {
  await api.delete(`${props.apiPath}/${id}`)
  load()
}

async function save() {
  if (editing.value.id) {
    await api.put(`${props.apiPath}/${editing.value.id}`, editing.value)
  } else {
    await api.post(props.apiPath, editing.value)
  }
  editing.value = null
  load()
}

async function savePC(pc) {
  if (pc.id) {
    await api.put(`${props.apiPath}/${pc.id}`, pc)
  } else {
    await api.post(props.apiPath, pc)
  }
  editing.value = null
  load()
}


onMounted(load)
</script>

<style scoped>
.crud-table {
  border-collapse: collapse;
}

.crud-table td,
.crud-table th {
  padding: 8px;
  border: 1px solid #ccc;
}

.modal {
  position: fixed;
  background: white;
  padding: 20px;
  top: 20%;
  left: 40%;
  border: 1px solid #999;
}
</style>
