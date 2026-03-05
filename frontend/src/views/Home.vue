<template>
  <div class="home">
    <div class="page-header">
      <h1>Propositions</h1>
      <p class="subtitle">Votez pour l'avenir de la DAO</p>
    </div>

    <div v-if="loading" class="loading">Chargement...</div>
    
    <div v-else-if="proposals.length === 0" class="empty">
      <p>Aucune proposition pour le moment.</p>
    </div>

    <div v-else class="proposals-grid">
      <div 
        v-for="proposal in proposals" 
        :key="proposal.id" 
        class="proposal-card"
        :class="{ executed: proposal.executed }"
      >
        <div class="proposal-header">
          <span class="proposal-id">#{{ proposal.id }}</span>
          <span v-if="proposal.executed" class="badge-executed">Exécutée</span>
          <span v-else-if="proposal.voting_open" class="badge-open">Vote ouvert</span>
          <span v-else class="badge-closed">Vote fermé</span>
        </div>
        
        <p class="proposal-desc">{{ proposal.description }}</p>
        
        <div class="proposal-stats">
          <div class="stat">
            <span class="stat-value">{{ proposal.vote_count }}</span>
            <span class="stat-label">votes</span>
          </div>
        </div>
        
        <div v-if="proposal.voting_open && !proposal.executed">
          <button 
            v-if="!hasVoted(proposal.id)"
            @click="claimAndVote(proposal.id)" 
            class="btn-vote"
            :disabled="claiming"
          >
            {{ claiming ? 'Transaction en cours...' : 'Claim & Voter' }}
          </button>
          <div v-else class="voted">
            ✓ Vote enregistré
          </div>
        </div>
        
        <div v-else-if="proposal.executed" class="closed">
          ✓ Vote clos
        </div>
        <div v-else class="no-voting">
          Vote pas encore ouvert
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'

const proposals = ref([])
const loading = ref(true)
const claiming = ref(false)
const votedProposals = ref([])
const account = inject('account')

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const fetchProposals = async () => {
  try {
    const res = await fetch(`${API_URL}/proposals`)
    proposals.value = await res.json()
  } catch (err) {
    console.error("Erreur:", err)
  } finally {
    loading.value = false
  }
}

const hasVoted = (proposalId) => {
  return votedProposals.value.includes(proposalId)
}

const claimAndVote = async (proposalId) => {
  if (!account.value) {
    alert("Connectez votre wallet!")
    return
  }
  
  claiming.value = true
  try {
    // Ici on appellera le smart contract pour mint + voter
    // Pour le MVP, on utilise l'API
    const res = await fetch(`${API_URL}/proposals/${proposalId}/vote`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voter_address: account.value })
    })
    
    if (res.ok) {
      votedProposals.value.push(proposalId)
      await fetchProposals()
    } else {
      const data = await res.json()
      alert(data.detail || "Erreur lors du vote")
    }
  } catch (err) {
    alert("Erreur de connexion")
  } finally {
    claiming.value = false
  }
}

onMounted(fetchProposals)
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

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}

.proposals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.proposal-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255,255,255,0.05);
  transition: transform 0.2s, border-color 0.2s;
}

.proposal-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
}

.proposal-card.executed {
  opacity: 0.7;
}

.proposal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.proposal-id {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.badge-executed, .badge-open, .badge-closed {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-executed {
  background: var(--success);
  color: #0a0a0a;
}

.badge-open {
  background: rgba(52, 152, 219, 0.2);
  color: var(--accent);
}

.badge-closed {
  background: rgba(255,255,255,0.1);
  color: var(--text-muted);
}

.proposal-desc {
  margin-bottom: 1rem;
  line-height: 1.5;
}

.proposal-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent);
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.btn-vote {
  width: 100%;
  background: var(--accent);
  color: #0a0a0a;
  border: none;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-vote:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-vote:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.voted, .no-voting, .closed {
  text-align: center;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
}

.voted {
  background: rgba(74, 222, 128, 0.1);
  color: var(--success);
}

.no-voting, .closed {
  background: rgba(255,255,255,0.05);
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .proposals-grid {
    grid-template-columns: 1fr;
  }
}
</style>
