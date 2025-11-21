<template>
  <div>
    <h2>Бронирование ПК</h2>

    <PcFilters @apply="loadPcs" />
    <PcList :pcs="pcs" @select="selectedPc = $event" />

    <BookingForm v-if="selectedPc" :pc="selectedPc" @created="refresh" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/axios'
import PcFilters from '../components/PcFilters.vue'
import PcList from '../components/PcList.vue'
import BookingForm from '../components/BookingForm.vue'

const pcs = ref([])
const selectedPc = ref(null)

async function loadPcs(filters = {}) {
  const { data } = await api.get('/api/bookings/pcs', { params: filters })
  pcs.value = data
}

function refresh() {
  selectedPc.value = null
}

onMounted(() => {
  loadPcs({})
})
</script>

