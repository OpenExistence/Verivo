<template>
  <div class="claim">
    <div class="page-header">
      <h1>Claim votre NFT de vote</h1>
      <p class="subtitle">Obtenez votre droit de vote au sein de la DAO</p>
    </div>

    <div class="claim-card">
      <div class="nft-preview">
        <div class="nft-icon">🎫</div>
        <h2>Voting Right NFT</h2>
        <p class="nft-desc">Ce NFT vous donne le droit de voter sur les propositions de la DAO.</p>
      </div>

      <div v-if="!account" class="connect-prompt">
        <p>Connectez votre wallet pour claimer</p>
        <button @click="$emit('connect')" class="btn-connect">
          Connect Wallet
        </button>
      </div>

      <div v-else class="claim-action">
        <div v-if="hasNFT" class="has-nft">
          <span class="check">✓</span>
          <p>Vous possédez déjà le NFT de vote!</p>
        </div>
        
        <div v-else>
          <p class="claim-info">Cliquez pour mint votre NFT de vote</p>
          <button @click="claimNFT" class="btn-claim" :disabled="claiming">
            {{ claiming ? 'Transaction en cours...' : 'Claim NFT' }}
          </button>
        </div>

        <div v-if="txHash" class="tx-info">
          <p>Transaction envoyée:</p>
          <a :href="sepoliaUrl(txHash)" target="_blank" class="tx-link">
            {{ shortHash(txHash) }}
          </a>
        </div>

        <div v-if="error" class="error">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'

const account = inject('account')
const hasNFT = ref(false)
const claiming = ref(false)
const txHash = ref('')
const error = ref('')

// À configurer après déploiement
const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS || ''

const claimNFT = async () => {
  if (!account.value) return
  
  error.value = ''
  claiming.value = true
  
  try {
    // Ici on appellera le smart contract
    // Pour le MVP, on utilise l'API
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    
    const res = await fetch(`${API_URL}/voting/grant`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address: account.value })
    })
    
    if (res.ok) {
      hasNFT.value = true
    } else {
      const data = await res.json()
      error.value = data.detail || "Erreur"
    }
  } catch (err) {
    error.value = "Erreur de connexion"
  } finally {
    claiming.value = false
  }
}

const shortHash = (hash) => hash.slice(0, 10) + '...' + hash.slice(-8)

const sepoliaUrl = (hash) => `https://sepolia.etherscan.io/tx/${hash}`

// Checker si déjà possédé au mount
import { onMounted } from 'vue'
onMounted(() => {
  // TODO: Vérifier via le smart contract
})
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--text-muted);
}

.claim-card {
  max-width: 400px;
  margin: 0 auto;
  background: var(--card-bg);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255,255,255,0.05);
}

.nft-preview {
  text-align: center;
  margin-bottom: 2rem;
}

.nft-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.nft-preview h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.nft-desc {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.connect-prompt {
  text-align: center;
}

.connect-prompt p {
  margin-bottom: 1rem;
  color: var(--text-muted);
}

.btn-connect {
  background: var(#d4af37);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.claim-action {
  text-align: center;
}

.claim-info {
  margin-bottom: 1rem;
  color: var(--text-muted);
}

.btn-claim {
  background: linear-gradient(135deg, var(--accent), #3498db);
  color: #0a0a0a;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-claim:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(93, 173, 226, 0.3);
}

.btn-claim:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.has-nft {
  background: rgba(74, 222, 128, 0.1);
  padding: 1.5rem;
  border-radius: 12px;
}

.check {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

.has-nft p {
  color: var(--success);
}

.tx-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
  font-size: 0.875rem;
}

.tx-link {
  color: var(#d4af37);
  word-break: break-all;
}

.error {
  margin-top: 1rem;
  color: #ff6b6b;
  padding: 0.75rem;
  background: rgba(255,107,107,0.1);
  border-radius: 8px;
}
</style>
