import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Proposals from '../views/Proposals.vue'
import About from '../views/About.vue'
import Admin from '../views/Admin.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/proposals', name: 'Proposals', component: Proposals },
  { path: '/about', name: 'About', component: About },
  { path: '/admin', name: 'Admin', component: Admin, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
