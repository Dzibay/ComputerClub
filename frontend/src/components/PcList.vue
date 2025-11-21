<template>
  <div>
    <h3>Доступные ПК</h3>

    <div v-if="pcs.length === 0">
      Ничего не найдено.
    </div>

    <ul class="pc-list">
      <li v-for="pc in pcs" :key="pc.id" class="pc-item">
        <div>
          <b>ПК #{{ pc.id }}</b><br />
          CPU: {{ pc.cpu?.name }}<br />
          GPU: {{ pc.gpu?.name }}<br />
          OS: {{ pc.os?.name }}
        </div>

        <button @click="$emit('select', pc)">
          Забронировать
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  pcs: Array
})
</script>

<style scoped>
.pc-list {
  margin-top: 15px;
  list-style: none;
  padding: 0;
}
.pc-item {
  display: flex;
  justify-content: space-between;
  border: 1px solid #ddd;
  padding: 8px;
  margin-bottom: 10px;
}
</style>
