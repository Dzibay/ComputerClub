<template>
  <div class="pc-list-container fade-in">
    <div v-if="pcs.length === 0" class="empty-state glass-card">
      <div class="icon">🔍</div>
      <h3>Нет свободных ПК</h3>
      <p>Попробуйте изменить время или фильтры.</p>
    </div>

    <div class="pc-grid">
      <div 
        v-for="pc in pcs" 
        :key="pc.id" 
        class="pc-card glass-card"
      >
        <div class="pc-header">
          <div class="pc-title">
            <span class="pc-icon">🖥</span>
            <span class="pc-number">Station {{ pc.id }}</span>
          </div>
          <span class="status-badge">Available</span>
        </div>

        <div class="pc-specs">
          <div class="spec-row">
            <span class="label">CPU</span>
            <span class="val">{{ pc.cpu?.name }}</span>
          </div>

          <div class="spec-row highlight-row">
            <span class="label">GPU</span>
            <span class="val gpu-text">{{ pc.gpu?.name }}</span>
          </div>

          <div class="spec-row">
            <span class="label">OS</span>
            <span class="val">{{ pc.os?.name }}</span>
          </div>
        </div>

        <div class="pc-software" v-if="pc.pc_software && pc.pc_software.length > 0">
          <div class="sw-divider"></div>
          <span class="sw-label">Установлено:</span>
          <div class="sw-tags">
            <span 
              v-for="link in pc.pc_software" 
              :key="link.id" 
              class="sw-tag"
            >
              {{ link.software.name }}
            </span>
          </div>
        </div>

        <button class="btn-primary book-btn" @click="$emit('select', pc)">
          Выбрать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ pcs: Array })
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}
.empty-state .icon { font-size: 3rem; margin-bottom: 1rem; }

.pc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.pc-card {
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}
.pc-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.pc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid var(--border-glass);
}

.pc-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.status-badge {
  font-size: 0.7rem;
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  padding: 2px 8px;
  border-radius: 10px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.spec-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.6rem;
  font-size: 0.9rem;
}

.label { color: var(--text-muted); }
.val { font-weight: 500; }

.highlight-row .val {
  color: var(--primary);
  text-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

/* --- Стили для блока программ --- */
.pc-software {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  flex-grow: 1; /* Чтобы кнопки всегда были внизу, если карточки разной высоты */
}

.sw-divider {
  height: 1px;
  background: var(--border-glass);
  margin-bottom: 0.8rem;
}

.sw-label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.sw-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.sw-tag {
  font-size: 0.75rem;
  background: rgba(99, 102, 241, 0.1); /* Прозрачный фиолетовый */
  color: #c084fc;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  white-space: nowrap;
}

.book-btn {
  width: 100%;
  margin-top: auto; /* Прижимает кнопку к низу */
}
</style>