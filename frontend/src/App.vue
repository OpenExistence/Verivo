<template>
  <div class="app">
    <header class="header">
      <div class="logo">
        <img src="/logo.jpg" alt="DAO Voting" />
        <span>DAO Voting</span>
      </div>
      <nav class="nav">
        <router-link to="/">Propositions</router-link>
        <router-link to="/claim">Claim NFT</router-link>
        <button v-if="!account" @click="connectWallet" class="btn-connect">
          Connect Wallet
        </button>
        <div v-else class="wallet-info">
          {{ shortAddress(account) }}
        </div>
      </nav>
    </header>

    <main class="main">
      <router-view />
    </main>

    <footer class="footer">
      <p>DAO Voting © 2026</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import { ethers } from 'ethers'

const account = ref(null)
provide('account', account)

const connectWallet = async () => {
  if (window.ethereum) {
    try {
      const provider = new ethers.BrowserProvider(window.ethereum)
      const accounts = await provider.send("eth_requestAccounts", [])
      account.value = accounts[0]
    } catch (err) {
      console.error("Erreur connexion:", err)
    }
  } else {
    alert("Veuillez installer MetaMask!")
  }
}

const shortAddress = (addr) => {
  return addr.slice(0, 6) + '...' + addr.slice(-4)
}

onMounted(() => {
  if (window.ethereum) {
    window.ethereum.on('accountsChanged', (accounts) => {
      account.value = accounts[0] || null
    })
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #1a1a2e;
  --secondary: #16213e;
  --accent: #e94560;
  --text: #eaeaea;
  --text-muted: #a0a0a0;
  --card-bg: #1f1f3a;
  --success: #4ade80;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: var(--secondary);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo img {
  height: 40px;
  border-radius: 8px;
}

.logo span {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
}

.nav {
  display: flex;
  align-items: center;
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

.btn-connect {
  background: var(--accent);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.btn-connect:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

.wallet-info {
  background: var(--card-bg);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-family: monospace;
  font-size: 0.875rem;
}

.main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  text-align: center;
  padding: 1.5rem;
  color: var(--text-muted);
  font-size: 0.875rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  
  .nav {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .main {
    padding: 1rem;
  }
}
</style>
