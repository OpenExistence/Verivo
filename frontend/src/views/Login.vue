<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <img src="/logo.jpg" alt="Verivo" class="auth-logo" />
          <h1>Connexion</h1>
          <p>Accédez à votre compte Verivo</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              id="email" 
              v-model="email" 
              type="email" 
              placeholder="vous@exemple.com"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input 
              id="password" 
              v-model="password" 
              type="password" 
              placeholder="••••••••"
              required
            />
          </div>
          
          <div v-if="error" class="error-message">{{ error }}</div>
          
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>
        
        <p class="auth-footer">
          Pas encore de compte? 
          <router-link to="/register">Créer un compte</router-link>
        </p>
      </div>
    </div>
    
    <div class="auth-bg">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const res = await fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })
    
    const data = await res.json()
    
    if (!res.ok) {
      throw new Error(data.detail || 'Erreur de connexion')
    }
    
    localStorage.setItem('verivo_token', data.token)
    localStorage.setItem('verivo_user', JSON.stringify(data.user))
    
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: var(--primary);
}

.auth-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 440px;
  padding: 2rem;
}

.auth-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 2.5rem;
  backdrop-filter: blur(20px);
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-logo {
  height: 60px;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.auth-header h1 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.auth-header p {
  color: var(--text-muted);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.875rem 1rem;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.05);
  color: var(--text);
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.15);
}

.form-group input::placeholder {
  color: var(--text-muted);
}

.btn-submit {
  padding: 1rem;
  border-radius: 12px;
  background: var(--accent);
  color: #0a0a0a;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 0.5rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: var(--error);
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--text-muted);
}

.auth-footer a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.auth-footer a:hover {
  text-decoration: underline;
}

/* Background animation */
.auth-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: var(--accent);
  top: -100px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #9b59b6;
  bottom: -50px;
  left: -50px;
  animation: float 10s ease-in-out infinite reverse;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: #1abc9c;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.5; }
}
</style>
