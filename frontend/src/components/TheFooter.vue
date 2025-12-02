<template>
  <footer class="site-footer">
    <div class="container">
      
      <div class="footer-content">
        <div class="footer-brand">
          <h2 class="brand-title">ТВОЯ ИГРА</h2>
          <p class="brand-desc">
            Киберспортивное пространство нового поколения. 
            Топовое железо, комфорт и атмосфера победы.
          </p>
          <div class="socials">
            <a href="#" class="social-link">VK</a>
            <a href="#" class="social-link">TG</a>
            <a href="#" class="social-link">YT</a>
          </div>
        </div>

        <div class="footer-nav">
          <h3>Навигация</h3>
          <ul>
            <li><router-link to="/">Главная</router-link></li>
            <li><router-link to="/cabinet/bookings">Бронирование</router-link></li>
            <li><router-link to="/cabinet">Личный кабинет</router-link></li>
          </ul>
        </div>

        <div class="footer-contacts">
          <h3>Контакты</h3>
          <ul>
            <li class="contact-item">
              <span class="icon">📍</span>
              <span>г. Санкт-Петербург, ул. Киберспортивная, 13</span>
            </li>
            <li class="contact-item">
              <span class="icon">📞</span>
              <span>+7 (999) 000-00-00</span>
            </li>
            <li class="contact-item">
              <span class="icon">⏰</span>
              <span>Работаем 24/7</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2025 CyberClub. Все права защищены.</p>
        <p class="made-by">Balybin Anton</p>
      </div>

    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  background: rgba(15, 15, 20, 0.8); /* Темнее основного фона */
  border-top: 1px solid var(--border-glass);
  padding: 4rem 0 2rem;
  margin-top: auto; /* Прижимает футер вниз, если контента мало */
  backdrop-filter: blur(10px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.brand-title {
  font-size: 1.8rem;
  font-weight: 900;
  letter-spacing: -1px;
  margin-bottom: 1rem;
  background: linear-gradient(to right, #fff, var(--text-muted));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-desc {
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  max-width: 300px;
}

.socials {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-glass);
  border-radius: 50%;
  color: var(--text-muted);
  transition: all 0.3s ease;
  font-weight: bold;
  font-size: 0.8rem;
}

.social-link:hover {
  border-color: var(--primary);
  color: var(--primary);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
}

h3 {
  font-size: 1.2rem;
  color: white;
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 0.8rem;
}

a {
  color: var(--text-muted);
  transition: color 0.2s;
  text-decoration: none;
}

a:hover {
  color: var(--primary);
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-muted);
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 2rem;
  display: flex;
  justify-content: space-between;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.made-by {
  font-family: monospace;
  color: var(--primary);
  opacity: 0.7;
}

@media (max-width: 768px) {
  .footer-bottom {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  .footer-content {
    text-align: center;
  }
  .brand-desc {
    margin-left: auto;
    margin-right: auto;
  }
  .socials {
    justify-content: center;
  }
}
</style>