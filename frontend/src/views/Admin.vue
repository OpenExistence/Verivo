<template>
  <div class="admin">
    <div class="page-header">
      <h1>Admin</h1>
      <p class="subtitle">Gérez les propositions et les votants</p>
    </div>

    <div class="admin-card">
      <h2>Nouvelle proposition</h2>
      <form @submit.prevent="createProposal" class="proposal-form">
        <div class="form-group">
          <label for="title">Titre</label>
          <input 
            id="title" 
            v-model="title" 
            type="text"
            placeholder="Titre de la proposition"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            id="description" 
            v-model="description" 
            placeholder="Décrivez votre proposition..."
            rows="4"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="voteType">Type de vote</label>
          <select id="voteType" v-model="voteType">
            <option v-for="vt in voteTypes" :key="vt.name" :value="vt.name">
              {{ vt.description || vt.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="voters">Votants (adresses séparées par virgule)</label>
          <textarea 
            id="voters" 
            v-model="votersInput" 
            placeholder="0x..., 0x..., 0x..."
            rows="2"
          ></textarea>
        </div>

        <button type="submit" class="btn-submit" :disabled="submitting">
          {{ submitting ? 'Création...' : 'Créer la proposition' }}
        </button>
      </form>

      <div v-if="success" class="success">
        <span>✓</span> Proposition créée! (#{{ proposalId }})
      </div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>

    <div class="section-header">
      <h2>Propositions</h2>
    </div>

    <div v-if="loading" class="loading">Chargement...</div>

    <div v-else class="proposals-list">
      <div v-for="proposal in proposals" :key="proposal.id" class="proposal-item">
        <div class="proposal-info">
          <div class="proposal-header">
            <span class="proposal-id">#{{ proposal.id }}</span>
            <span class="vote-type-badge">{{ proposal.vote_type }}</span>
          </div>
          <h3 class="proposal-title">{{ proposal.title }}</h3>
          <p class="proposal-desc">{{ proposal.description }}</p>
          <div class="proposal-meta">
            <span class="status" :class="proposal.status">{{ proposal.status }}</span>
            <span class="status" :class="{ open: proposal.voting_open }">
              {{ proposal.voting_open ? 'Vote ouvert' : 'Vote fermé' }}
            </span>
          </div>
        </div>
        
        <div class="proposal-actions">
          <span class="vote-count">{{ proposal.vote_count }} votes</span>
          
          <div v-if="!proposal.voting_open && proposal.status === 'pending'" class="start-voting">
            <button @click="startVoting(proposal.id)" class="btn-start">
              Ouvrir le vote
            </button>
          </div>
          
          <button 
            v-if="proposal.voting_open && proposal.status !== 'executed'"
            @click="executeProposal(proposal.id)" 
            class="btn-execute"
            :disabled="executing"
          >
            Exécuter
          </button>
          
          <span v-if="proposal.status === 'executed'" class="executed-badge">Exécutée</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const title = ref('')
const description = ref('')
const voteType = ref('simple_majority')
const votersInput = ref('')
const voteTypes = ref([])
const proposals = ref([])
const loading = ref(true)
const submitting = ref(false)
const executing = ref(false)
const success = ref(false)
const error = ref('')
const proposalId = ref(null)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const fetchVoteTypes = async () => {
  try {
    const res = await fetch(`${API_URL}/vote-types`)
    voteTypes.value = await res.json()
  } catch (err) {
    console.error("Erreur vote types:", err)
  }
}

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

const createProposal = async () => {
  if (!title.value.trim() || !description.value.trim()) return
  
  error.value = ''
  success.value = false
  submitting.value = true
  
  try {
    const res = await fetch(`${API_URL}/proposals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        title: title.value,
        description: description.value,
        vote_type: voteType.value,
        voters: votersInput.value ? votersInput.value.split(',').map(a => a.trim()) : []
      })
    })
    
    if (res.ok) {
      const data = await res.json()
      proposalId.value = data.id
      success.value = true
      title.value = ''
      description.value = ''
      votersInput.value = ''
      await fetchProposals()
    } else {
      const data = await res.json()
      error.value = data.detail || "Erreur"
    }
  } catch (err) {
    error.value = "Erreur de connexion"
  } finally {
    submitting.value = false
  }
}

const startVoting = async (proposalId) => {
  try {
    const res = await fetch(`${API_URL}/proposals/${proposalId}/start`, { method: 'POST' })
    if (res.ok) await fetchProposals()
  } catch (err) {
    alert("Erreur")
  }
}

const executeProposal = async (id) => {
  executing.value = true
  try {
    await fetchProposals()
  } finally {
    executing.value = false
  }
}

onMounted(() => {
  fetchVoteTypes()
  fetchProposals()
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

.admin-card {
  max-width: 700px;
  margin: 0 auto;
  background: var(--card-bg);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255,255,255,0.05);
  margin-bottom: 3rem;
}

.admin-card h2 {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.proposal-form .form-group {
  margin-bottom: 1.25rem;
}

.proposal-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.proposal-form input,
.proposal-form textarea,
.proposal-form select {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.05);
  color: var(--text);
  font-size: 1rem;
  font-family: inherit;
}

.proposal-form select {
  cursor: pointer;
}

.proposal-form textarea {
  resize: vertical;
}

.proposal-form input:focus,
.proposal-form textarea:focus,
.proposal-form select:focus {
  outline: none;
  border-color: var(--accent);
}

.btn-submit {
  width: 100%;
  background: var(--accent);
  color: #0a0a0a;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.success {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 8px;
  color: var(--success);
}

.error {
  margin-top: 1rem;
  color: #ff6b6b;
  padding: 0.75rem;
  background: rgba(255,107,107,0.1);
  border-radius: 8px;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--text-muted);
}

.proposals-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.proposal-item {
  display: flex;
  justify-content: space-between;
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.05);
}

.proposal-info {
  flex: 1;
}

.proposal-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.proposal-id {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.vote-type-badge {
  background: rgba(52, 152, 219, 0.2);
  color: var(--accent);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  text-transform: uppercase;
}

.proposal-title {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.proposal-desc {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.proposal-meta {
  display: flex;
  gap: 0.5rem;
}

.status {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  text-transform: uppercase;
}

.status.pending { background: rgba(255,255,255,0.1); }
.status.approved { background: rgba(74,222,128,0.2); color: var(--success); }
.status.rejected { background: rgba(255,107,107,0.2); color: #ff6b6b; }
.status.open { background: rgba(52,152,219,0.2); color: var(--accent); }

.proposal-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.vote-count {
  color: var(--accent);
  font-weight: 600;
}

.btn-start {
  background: var(--accent);
  color: #0a0a0a;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-execute {
  background: var(--success);
  color: #0a0a0a;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.executed-badge {
  color: var(--success);
  font-weight: 500;
}

@media (max-width: 768px) {
  .proposal-item {
    flex-direction: column;
  }
  .proposal-actions {
    width: 100%;
    align-items: stretch;
    margin-top: 1rem;
  }
}
</style>
