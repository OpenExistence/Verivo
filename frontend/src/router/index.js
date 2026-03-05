import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Claim from './views/Claim.vue'
import Admin from './views/Admin.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/claim', name: 'Claim', component: Claim },
  { path: '/admin', name: 'Admin', component: Admin }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
