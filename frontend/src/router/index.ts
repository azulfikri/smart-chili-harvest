import { createRouter, createWebHistory } from 'vue-router'
import SplashView from '../views/SplashView.vue'
import DashboardView from '../views/DashboardView.vue'
import DetectionView from '../views/DetectionView.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'splash',
      component: SplashView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/detection',
      name: 'detection',
      component: DetectionView
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    },
    {
      path: '/sessions/:id',
      name: 'session-detail',
      component: () => import('../views/SessionDetailView.vue')
    }
  ]
})

export default router
