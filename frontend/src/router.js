import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './store/auth'

import CabinetLayout from './layoutes/CabinetLayout.vue'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import BookingView from './views/BookingView.vue'
import CabinetView from './views/CabinetView.vue'
import AdminDashboard from './views/AdminDashboard.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },

  {
  path: '/cabinet',
  component: CabinetLayout,
  meta: { requiresAuth: true },
  children: [
    { path: '', component: CabinetView },
    { path: 'bookings', component: BookingView }
  ]
  },
  {
  path: '/admin',
  name: 'admin-dashboard',
  component: AdminDashboard,
  meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.requiresAdmin && auth.user?.role !== 'Admin') {
    return next('/')
  }

  next()
})

export default router
