<template>
  <div class="booking-form glass-card fade-in">

    <h3 class="title">Бронирование ПК #{{ pc.id }}</h3>

    <!-- Тариф -->
    <div class="form-group">
      <label>Тариф</label>
      <select v-model="tariff">
        <option value="" disabled>Выбери тариф</option>
        <option v-for="t in tariffs" :key="t.id" :value="t">
          {{ t.name }} — {{ t.price_per_hour }}₽/час
        </option>
      </select>
    </div>

    <!-- Дата -->
    <div class="form-group">
      <label>Дата бронирования</label>
      <input type="date" v-model="date" @change="resetSelection" />
    </div>

    <!-- Часовые слоты -->
    <div class="form-group">
      <label>Выберите время</label>

      <div class="slots-grid">
        <div
          v-for="slot in timeSlots"
          :key="slot.id"
          class="slot"
          :class="{
            disabled: slot.disabled,
            selected: slotSelected(slot.id),
            start: slot.id === startHour,
            end: slot.id === endHour - 1
          }"
          @click="selectSlot(slot)"
        >
          {{ slot.label }}
        </div>
      </div>
    </div>

    <button class="btn-primary submit-btn" @click="book">
      Забронировать
    </button>

    <p v-if="msg" class="msg success glass-card">{{ msg }}</p>
    <p v-if="err" class="msg error glass-card">{{ err }}</p>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/axios'
import { useCabinetStore } from '../store/cabinet'

const props = defineProps({ pc: Object })
const emit = defineEmits(['created'])

const cabinetStore = useCabinetStore()

const tariffs = ref([])
const tariff = ref(null)

const date = ref("")
const startHour = ref(null)
const endHour = ref(null)

const msg = ref("")
const err = ref("")

async function loadTariffs() {
  try {
    const { data } = await api.get('/api/admin/tariffs')
    tariffs.value = data
  } catch (e) {
    console.error("Ошибка загрузки тарифов", e)
  }
}

// ------------------- ВРЕМЕННЫЕ СЛОТЫ --------------------
const timeSlots = computed(() => {
  if (!date.value) return []

  const slots = []
  const baseDate = new Date(date.value + "T00:00:00")

  for (let i = 0; i < 24; i++) {
    const d = new Date(baseDate.getTime() + i * 3600000)
    const label = `${String(d.getHours()).padStart(2, "0")}:00`

    slots.push({
      id: i,
      ts: d.getTime(),
      label,
      disabled: slotBusy(d)
    })
  }
  return slots
})

function slotBusy(slotDate) {
  if (!props.pc.busy) return false
  const slotStart = slotDate.getTime()
  const slotEnd = slotStart + 3600000
  return props.pc.busy.some(u => {
    const busyStart = new Date(u.start).getTime()
    const busyEnd = new Date(u.end).getTime()
    return slotStart < busyEnd && slotEnd > busyStart
  })
}

// ------------------- ЛОГИКА ВЫБОРА --------------------
function resetSelection() {
  startHour.value = null
  endHour.value = null
}

function slotSelected(id) {
  return (
    startHour.value !== null &&
    endHour.value !== null &&
    id >= startHour.value &&
    id < endHour.value
  )
}

function selectSlot(slot) {
  if (slot.disabled) return
  if (startHour.value === null) {
    startHour.value = slot.id
    endHour.value = slot.id + 1
    return
  }
  if (endHour.value === startHour.value + 1) {
    if (slot.id > startHour.value) {
      endHour.value = slot.id + 1
      return
    }
  }
  startHour.value = slot.id
  endHour.value = slot.id + 1
}

// ------------------- СОЗДАНИЕ БРОНИ --------------------
async function book() {
  msg.value = ""
  err.value = ""

  if (!tariff.value) {
    err.value = "Выберите тариф!"
    return
  }
  if (!date.value || startHour.value === null || endHour.value === null) {
    err.value = "Выберите дату и время!"
    return
  }

  const duration = endHour.value - startHour.value
  const totalPrice = tariff.value.price_per_hour * duration
  
  if (cabinetStore.user && cabinetStore.user.balance < totalPrice) {
     err.value = "Недостаточно средств на балансе"
     return
  }

  const start = new Date(date.value + "T00:00:00")
  const startTime = new Date(start.getTime() + startHour.value * 3600000)
  const isoStart = `${date.value}T${String(startTime.getHours()).padStart(2, '0')}:00`

  try {
    const { data } = await api.post("/api/bookings", {
      pc_id: props.pc.id,
      tariff_id: tariff.value.id,
      start_time: isoStart,
      duration_hours: duration
    })

    cabinetStore.updateAfterBooking(totalPrice, data.usage)
    msg.value = "Бронь успешно создана!"
    emit("created") 
    
  } catch (e) {
    err.value = e.response?.data?.error || "Ошибка бронирования"
  }
}

onMounted(loadTariffs)
</script>

<style scoped>
.slots-grid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 6px;
}

.slot {
  padding: 8px;
  text-align: center;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 6px;
  cursor: pointer;
  transition: 0.15s;
}

.slot.disabled {
  opacity: 0.25;
  cursor: not-allowed;
}

.slot.selected {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.slot.start {
  border-left: 3px solid #fff;
}

.slot.end {
  border-right: 3px solid #fff;
}
</style>
