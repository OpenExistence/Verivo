<template>
  <div class="admin">
    <div class="page-header">
      <h1>Admin - Créer une proposition</h1>
      <p class="subtitle">Soumettez une nouvelle proposition au vote</p>
    </div>

    <div class="admin-card">
      <form @submit.prevent="createProposal" class="proposal-form">
        <div class="form-group">
          <label for="description">Description de la proposition</label>
          <textarea 
            id="description" 
            v-model="description" 
            placeholder="Décrivez votre proposition..."
            rows="4"
            required
          ></textarea>
        </div>

        <button type="submit" class="btn-submit" :disabled="submitting">
          {{ submitting ? 'Création en cours...' : 'Créer la proposition' }}
        </button>
      </form>

      <div v-if="success" class="success">
        <span>✓</span> Proposition créée avec succès! (#{{ proposalId }})
      </div>

      <div v-if="error" class="error">{{ error }}</div>
    </div>

    <div class="section-header">
      <h2>Propositions existantes</h2>
    </div>

    <div v-if="loading" class="loading">Chargement...</div>

    <div v-else class="proposals-list">
      <div v-for="proposal in proposals" :key="proposal.id" class="proposal-item">
        <div class="proposal-info">
          <span class="proposal-id">#{{ proposal.id }}</span>
          <p class="proposal-desc">{{ proposal.description }}</p>
        </div>
        
        <div class="proposal-actions">
          <span class="vote-count">{{ proposal.vote_count }} votes</span>
          
          <button 
            v-if="!proposal.executed"
            @click="executeProposal(proposal.id)" 
            class="btn-execute"
            :disabled="executing"
          >
            Exécuter
          </button>
          
          <span v-else class="executed-badge">Exécutée</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const description = ref('')
const proposals = ref([])
const loading = ref(true)
const submitting = ref(false)
const executing = ref(false)
const success = ref(false)
const error = ref('')
const proposalId = ref(null)

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

const createProposal = async () => {
  if (!description.value.trim()) return
  
  error.value = ''
  success.value = false
  submitting.value = true
  
  try {
    const res = await fetch(`${API_URL}/proposals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description.value })
    })
    
    if (res.ok) {
      const data = await res.json()
      proposalId.value = data.id
      success.value = true
      description.value = ''
      await fetchProposals()
    } else {
      const data = await res.json()
      error.value = data.detail || "Erreur lors de la création"
    }
  } catch (err) {
    error.value = "Erreur de connexion"
  } finally {
    submitting.value = false
  }
}

const executeProposal = async (id) => {
  executing.value = true
  try {
    // TODO: Appeler le smart contract pour exécuter
    await fetchProposals()
  } catch (err) {
    error.value = "Erreur lors de l'exécution"
  } finally {
    executing.value = false
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

.admin-card {
  max-width: 600px;
  margin: 0 auto;
  background: var(--card-bg);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255,255,255,0.05);
  margin-bottom: 3rem;
}

.proposal-form .form-group {
  margin-bottom: 1.5rem;
}

.proposal-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.proposal-form textarea {
  width: 100%;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.05);
  color: var(--text);
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
}

.proposal-form textarea:focus {
  outline: none;
  border-color: var(--accent);
}

.btn-submit {
  width: 100%;
  background: var(--accent);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.success {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 8px;
  color: var(--success);
  text-align: center;
}

.success span {
  font-size: 1.25rem;
  margin-right: 0.5rem;
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
  align-items: center;
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.05);
}

.proposal-info {
  flex: 1;
}

.proposal-id {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.proposal-desc {
  margin-top: 0.25rem;
}

.proposal-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.vote-count {
  color: var(--accent);
  font-weight: 600;
}

.btn-execute {
  background: var(--success);
  color: #000;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-execute:hover:not(:disabled) {
  opacity: 0.8;
}

.btn-execute:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.executed-badge {
  color: var(--success);
  font-weight: 500;
}

@media (max-width: 768px) {
  .proposal-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .proposal-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
