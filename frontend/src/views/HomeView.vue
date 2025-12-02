<template>
  <div class="home-page fade-in">

    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          ТВОЯ ИГРА <br>
          <span class="highlight">НОВОГО УРОВНЯ</span>
        </h1>
        <p class="hero-desc">
          Топовое железо RTX 40-й серии, мониторы 360Hz и атмосфера, 
          которая заставляет побеждать.
        </p>
        
        <div class="hero-actions">
          <template v-if="auth.isAuthenticated">
             <router-link to="/cabinet/bookings" class="btn-primary hero-btn">
               Забронировать ПК
             </router-link>
             <router-link to="/cabinet" class="btn-outline hero-btn">
               В кабинет
             </router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="btn-primary hero-btn">
              Войти в систему
            </router-link>
            <router-link to="/register" class="btn-outline hero-btn">
              Создать аккаунт
            </router-link>
          </template>
        </div>
      </div>
      <div class="hero-glow"></div>
    </section>

    <section class="specs-section container" v-if="!isLoading">
      <h2 class="section-title center">Наш Арсенал</h2>
      <p class="section-subtitle center">Только проверенное и мощное оборудование</p>

      <div class="specs-grid">
        <div class="glass-card spec-card">
          <div class="spec-icon">🎮</div>
          <h3>Видеокарты</h3>
          <ul class="hardware-list">
            <li v-for="gpu in hardware.gpus" :key="gpu.id">{{ gpu.name }}</li>
          </ul>
        </div>
        <div class="glass-card spec-card">
          <div class="spec-icon">⚡</div>
          <h3>Процессоры</h3>
          <ul class="hardware-list">
            <li v-for="cpu in hardware.cpus" :key="cpu.id">{{ cpu.name }}</li>
          </ul>
        </div>
        
        <div class="glass-card spec-card">
          <div class="spec-icon">🕹️</div>
          <h3>Игры и ПО</h3>
          <div class="tags-container scrollable-tags">
            <span v-for="sw in hardware.software" :key="sw.id" class="tech-tag software-tag">
              {{ sw.name }}
            </span>
          </div>
        </div>

        <div class="glass-card spec-card">
          <div class="spec-icon">💿</div>
          <h3>Платформы</h3>
          <div class="tags-container">
            <span v-for="os in hardware.oses" :key="os.id" class="tech-tag">
              {{ os.name }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <section class="features container">
      <div class="glass-card feature-card">
        <div class="icon">🚀</div>
        <h3>Максимальный FPS</h3>
        <p>Наши сборки оптимизированы для киберспортивных дисциплин.</p>
      </div>
      <div class="glass-card feature-card">
        <div class="icon">🖥️</div>
        <h3>360Hz Экраны</h3>
        <p>Плавная картинка без задержек. Увидь противника раньше.</p>
      </div>
      <div class="glass-card feature-card">
        <div class="icon">🛋️</div>
        <h3>Комфорт 24/7</h3>
        <p>Профессиональные кресла, климат-контроль и бар с напитками.</p>
      </div>
    </section>

    <section class="tariffs container">
      <h2 class="section-title center">Тарифные планы</h2>
      
      <div v-if="isLoading" class="loading-state">
        Загрузка данных...
      </div>

      <div v-else class="tariffs-grid">
        <div 
          v-for="tariff in tariffs" 
          :key="tariff.id"
          class="glass-card tariff-card"
          :class="{ 'vip': isVip(tariff.name) }"
        >
          <div v-if="isVip(tariff.name)" class="badge">TOP TIER</div>
          <div class="tariff-header">
            <h3>{{ tariff.name }}</h3>
            <span class="price">{{ tariff.price_per_hour }}₽ <small>/ час</small></span>
          </div>
          <div class="tariff-body">
            <p class="hours-badge" v-if="tariff.hours_number > 0">
              Пакет: {{ tariff.hours_number }} ч.
            </p>
            <p class="description">{{ tariff.description }}</p>
          </div>
          <router-link to="/cabinet/bookings" class="btn-outline full-width">
            Выбрать
          </router-link>
        </div>
      </div>
    </section>

    <TheFooter />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import api from '../api/axios'
import TheFooter from '../components/TheFooter.vue'

const auth = useAuthStore()
const isLoading = ref(true)

const tariffs = ref([])
// Добавили поле software
const hardware = ref({ cpus: [], gpus: [], oses: [], software: [] })

const isVip = (name) => {
  return name && (name.toLowerCase().includes('vip') || name.toLowerCase().includes('premium'))
}

const fetchData = async () => {
  try {
    isLoading.value = true
    // Добавлен запрос software
    const [resTariffs, resCpus, resGpus, resOses, resSoftware] = await Promise.all([
      api.get('/api/admin/tariffs'),
      api.get('/api/admin/cpus'),
      api.get('/api/admin/gpus'),
      api.get('/api/admin/oses'),
      api.get('/api/admin/software') 
    ])
    tariffs.value = resTariffs.data
    hardware.value.cpus = resCpus.data
    hardware.value.gpus = resGpus.data
    hardware.value.oses = resOses.data
    hardware.value.software = resSoftware.data
  } catch (error) {
    console.error('Data load error:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* Основные стили остались прежними, добавлены детали для software */
.container { max-width: 1200px; margin: 0 auto; padding: 0 1rem; }
.section-title.center { text-align: center; margin-bottom: 1rem; font-size: 2.5rem; font-weight: 800; text-transform: uppercase; }
.section-subtitle.center { text-align: center; color: var(--text-muted); margin-bottom: 3rem; font-size: 1.1rem; }

.hero { position: relative; height: 80vh; min-height: 600px; display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden; margin-bottom: 4rem; }
.hero-content { position: relative; z-index: 2; max-width: 800px; padding: 0 1rem; }
.hero-title { font-size: 4rem; line-height: 1.1; font-weight: 900; letter-spacing: -2px; margin-bottom: 1.5rem; }
.highlight { background: linear-gradient(to right, var(--primary), #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 30px rgba(99, 102, 241, 0.5); }
.hero-desc { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto; }
.hero-actions { display: flex; gap: 1.5rem; justify-content: center; }
.hero-btn { padding: 1rem 2.5rem; font-size: 1.1rem; }
.hero-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 600px; height: 600px; background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, rgba(0,0,0,0) 70%); z-index: 1; pointer-events: none; }

.specs-section { margin-bottom: 6rem; }
.specs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.spec-card { padding: 2rem; display: flex; flex-direction: column; align-items: center; text-align: center; border: 1px solid var(--border-glass); }
.spec-icon { font-size: 2.5rem; margin-bottom: 1rem; background: rgba(255,255,255,0.05); width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
.spec-card h3 { margin-bottom: 1.5rem; font-size: 1.4rem; color: var(--primary); }
.hardware-list { list-style: none; padding: 0; width: 100%; }
.hardware-list li { padding: 0.8rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--text-main); font-weight: 500; }
.hardware-list li:last-child { border-bottom: none; }
.tags-container { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }

/* Доп. стили для блока с софтом, чтобы ограничить высоту если игр много */
.scrollable-tags {
  max-height: 150px;
  overflow-y: auto;
  padding-right: 5px;
}
.scrollable-tags::-webkit-scrollbar { width: 4px; }
.scrollable-tags::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }

.tech-tag { background: rgba(99, 102, 241, 0.1); color: var(--primary); padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.9rem; border: 1px solid rgba(99, 102, 241, 0.2); }
.software-tag { border-color: rgba(168, 85, 247, 0.3); color: #c084fc; background: rgba(168, 85, 247, 0.1); }

.features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 6rem; }
.feature-card { padding: 2rem; text-align: center; transition: transform 0.3s ease; }
.feature-card:hover { transform: translateY(-10px); border-color: var(--primary); }
.icon { font-size: 3rem; margin-bottom: 1rem; display: inline-block; }
.feature-card h3 { font-size: 1.4rem; margin-bottom: 0.5rem; }
.feature-card p { color: var(--text-muted); font-size: 0.95rem; }

.tariffs { margin-bottom: 6rem; }
.loading-state { text-align: center; padding: 2rem; color: var(--text-muted); }
.tariffs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; align-items: stretch; }
.tariff-card { padding: 2rem; position: relative; display: flex; flex-direction: column; transition: all 0.3s ease; }
.tariff-card:hover { transform: translateY(-5px); border-color: rgba(255, 255, 255, 0.2); }
.tariff-header { margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-glass); padding-bottom: 1rem; }
.tariff-header h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
.tariff-header .price { font-size: 1.4rem; color: white; font-weight: bold; }
.tariff-header .price small { font-size: 0.9rem; color: var(--text-muted); font-weight: normal; }
.tariff-body { flex-grow: 1; margin-bottom: 1.5rem; }
.description { color: var(--text-muted); line-height: 1.5; }
.hours-badge { display: inline-block; background: rgba(255, 255, 255, 0.1); padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.85rem; margin-bottom: 1rem; color: var(--text-main); }
.full-width { width: 100%; text-align: center; }

.tariff-card.vip { border: 1px solid var(--primary); box-shadow: 0 0 30px rgba(99, 102, 241, 0.1); background: linear-gradient(145deg, rgba(30, 34, 48, 0.9), rgba(20, 20, 30, 0.95)); }
.badge { position: absolute; top: -12px; right: 20px; background: var(--primary); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }

@media (max-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .hero-actions { flex-direction: column; }
}
</style>