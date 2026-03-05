<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <router-link to="/" class="logo">
          <img src="/logo.jpg" alt="Verivo" />
          <span>Verivo</span>
        </router-link>
        
        <nav class="nav">
          <router-link to="/">Accueil</router-link>
          <router-link to="/proposals">Propositions</router-link>
          <router-link to="/about">À propos</router-link>
        </nav>
        
        <div class="auth-buttons" v-if="!user">
          <router-link to="/login" class="btn btn-ghost">Connexion</router-link>
          <router-link to="/register" class="btn btn-primary">Inscription</router-link>
        </div>
        
        <div class="user-menu" v-else>
          <span class="user-name">{{ user.name || user.email }}</span>
          <router-link v-if="user.role === 'admin'" to="/admin" class="btn btn-ghost">Admin</router-link>
          <button @click="logout" class="btn btn-ghost">Déconnexion</button>
        </div>
      </div>
    </header>

    <main class="main">
      <router-view @auth="onAuth" />
    </main>

    <footer class="footer">
      <p>© 2026 Verivo - Système de vote décentralisé</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)

const onAuth = () => {
  checkAuth()
}

const checkAuth = async () => {
  const token = localStorage.getItem('verivo_token')
  if (!token) return
  
  try {
    const res = await fetch('http://localhost:8000/api/me', {
      headers: { 'Authorization': token }
    })
    if (res.ok) {
      user.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

const logout = () => {
  localStorage.removeItem('verivo_token')
  user.value = null
  router.push('/')
}

onMounted(checkAuth)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #0a0a0a;
  --secondary: #141414;
  --accent: #3498db;
  --accent-hover: #2980b9;
  --text: #f5f5dc;
  --text-muted: #a8a8a8;
  --card-bg: #1a1a1a;
  --success: #4ade80;
  --error: #ff6b6b;
  --border: rgba(255,255,255,0.1);
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--primary);
  color: var(--text);
  min-height: 100vh;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background: var(--secondary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.logo img {
  height: 36px;
  border-radius: 8px;
}

.logo span {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent);
}

.nav {
  display: flex;
  gap: 1.5rem;
}

.nav a {
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav a:hover,
.nav a.router-link-active {
  color: var(--accent);
}

.auth-buttons {
  display: flex;
  gap: 0.75rem;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-name {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--accent);
  color: #0a0a0a;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-ghost {
  background: transparent;
  color: var(--text);
}

.btn-ghost:hover {
  background: rgba(255,255,255,0.1);
}

.main {
  flex: 1;
  padding: 0;
}

.footer {
  text-align: center;
  padding: 2rem;
  color: var(--text-muted);
  font-size: 0.875rem;
  border-top: 1px solid var(--border);
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    padding: 1rem;
  }
  
  .nav {
    order: 3;
    width: 100%;
    justify-content: center;
    margin-top: 1rem;
  }
}
</style>
