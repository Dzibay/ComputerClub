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

    <section class="features container">
      <div class="glass-card feature-card">
        <div class="icon">🚀</div>
        <h3>Мощное железо</h3>
        <p>NVIDIA RTX 4090 и Intel Core i9 во всех VIP залах для максимального FPS.</p>
      </div>

      <div class="glass-card feature-card">
        <div class="icon">🖥️</div>
        <h3>360Hz Экраны</h3>
        <p>Плавная картинка без задержек. Увидь противника раньше, чем он тебя.</p>
      </div>

      <div class="glass-card feature-card">
        <div class="icon">🛋️</div>
        <h3>Комфорт</h3>
        <p>Профессиональные кресла, климат-контроль и бар с напитками 24/7.</p>
      </div>
    </section>

    <section class="tariffs container">
      <h2 class="section-title center">Наши зоны</h2>
      
      <div class="tariffs-grid">
        <div class="glass-card tariff-card">
          <div class="tariff-header">
            <h3>Standard</h3>
            <span class="price">от 100₽/час</span>
          </div>
          <ul class="specs-list">
            <li>RTX 3060 Ti</li>
            <li>Monitor 144Hz</li>
            <li>Периферия HyperX</li>
          </ul>
        </div>

        <div class="glass-card tariff-card vip">
          <div class="badge">POPULAR</div>
          <div class="tariff-header">
            <h3>VIP</h3>
            <span class="price">от 200₽/час</span>
          </div>
          <ul class="specs-list">
            <li>RTX 4080</li>
            <li>Monitor 240Hz</li>
            <li>Отдельная комната</li>
          </ul>
        </div>

        <div class="glass-card tariff-card">
          <div class="tariff-header">
            <h3>Bootcamp</h3>
            <span class="price">от 1500₽/пакет</span>
          </div>
          <ul class="specs-list">
            <li>Для команд 5x5</li>
            <li>Шумоизоляция</li>
            <li>RTX 4070 Super</li>
          </ul>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
</script>

<style scoped>
/* --- General Layout --- */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.section-title.center {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2rem;
}

/* --- Hero Section --- */
.hero {
  position: relative;
  height: 80vh; /* Почти на весь экран */
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  margin-bottom: 4rem;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
  padding: 0 1rem;
}

.hero-title {
  font-size: 4rem;
  line-height: 1.1;
  font-weight: 900;
  letter-spacing: -2px;
  margin-bottom: 1.5rem;
}

.highlight {
  background: linear-gradient(to right, var(--primary), #a855f7); /* Индиго -> Фиолетовый */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
}

.hero-desc {
  font-size: 1.2rem;
  color: var(--text-muted);
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.hero-btn {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

/* Эффект свечения на фоне */
.hero-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, rgba(0,0,0,0) 70%);
  z-index: 1;
  pointer-events: none;
}

/* --- Features Section --- */
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 6rem;
}

.feature-card {
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  border-color: var(--primary);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: inline-block;
}

.feature-card h3 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: var(--text-muted);
  font-size: 0.95rem;
}

/* --- Tariffs Section --- */
.tariffs {
  margin-bottom: 6rem;
}

.tariffs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  align-items: center; /* Чтобы VIP карточка могла быть выше */
}

.tariff-card {
  padding: 2rem;
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.tariff-header {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-glass);
  padding-bottom: 1rem;
}

.tariff-header h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.tariff-header .price {
  font-size: 1.1rem;
  color: var(--primary);
  font-weight: bold;
}

.specs-list li {
  margin-bottom: 0.8rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
}

.specs-list li::before {
  content: '✓';
  color: var(--primary);
  margin-right: 10px;
  font-weight: bold;
}

/* VIP Card Special Styles */
.tariff-card.vip {
  border: 1px solid var(--primary);
  box-shadow: 0 0 40px rgba(99, 102, 241, 0.15);
  transform: scale(1.05); /* Чуть больше остальных */
  z-index: 2;
  background: rgba(30, 34, 48, 0.8);
}

.badge {
  position: absolute;
  top: -12px;
  right: 20px;
  background: var(--primary);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* --- Responsive Text --- */
@media (max-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .hero-actions { flex-direction: column; }
  .tariff-card.vip { transform: none; margin: 1rem 0; }
}
</style>