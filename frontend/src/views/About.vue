<template>
  <div class="about">
    <div class="page-header">
      <h1>Comment ça marche ?</h1>
      <p class="subtitle">Un système de vote sécurisé et transparent</p>
    </div>

    <div class="steps">
      <div class="step">
        <div class="step-icon">🔗</div>
        <h2>1. Connexion</h2>
        <p>Connectez votre portefeuille numérique (comme MetaMask) pour sécuriser votre identité.</p>
      </div>

      <div class="step">
        <div class="step-icon">📋</div>
        <h2>2. Consultez les propositions</h2>
        <p>Découvrez les propositions en cours de vote et leurs détails.</p>
      </div>

      <div class="step">
        <div class="step-icon">🗳️</div>
        <h2>3. Votez</h2>
        <p>Cliquez sur "Voter" pour enregistrer votre choix. Une fois voted, c'est définitif.</p>
      </div>

      <div class="step">
        <div class="step-icon">🔒</div>
        <h2>4. Sécurité</h2>
        <p>Votre vote est sécurisé par la blockchain. Personne ne peut le modifier ou le supprimer.</p>
      </div>
    </div>

    <div class="faq">
      <h2>Questions fréquentes</h2>
      
      <div class="faq-item">
        <h3>Qu'est-ce que la blockchain ?</h3>
        <p>C'est une technologie qui permet d'enregistrer des données de manière sécurisée et transparente. Vos votes sont protégés cryptographiquement.</p>
      </div>

      <div class="faq-item">
        <h3>Pourquoi connecter mon portefeuille ?</h3>
        <p>Votre portefeuille numérique certifie votre identité sans révéler vos informations personnelles. C'est comme une pièce d'identité numérique.</p>
      </div>

      <div class="faq-item">
        <h3>Puis-je changer mon vote ?</h3>
        <p>Non, une fois vote, c'est définitif. C'est le principe de la blockchain - tout est permanent et transparent.</p>
      </div>

      <div class="faq-item">
        <h3>Qui peut voter ?</h3>
        <p>Seuls les membres autorisés par l'administrateur peuvent voter sur chaque proposition.</p>
      </div>
    </div>

    <div class="cta">
      <router-link to="/" class="btn-primary">
        Voir les propositions
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--text-muted);
  font-size: 1.1rem;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.step {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(255,255,255,0.05);
}

.step-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.step h2 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--accent);
}

.step p {
  color: var(--text-muted);
  font-size: 0.9rem;
  line-height: 1.5;
}

.faq {
  margin-bottom: 3rem;
}

.faq h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.faq-item {
  background: var(--card-bg);
  padding: 1.25rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  border: 1px solid rgba(255,255,255,0.05);
}

.faq-item h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.faq-item p {
  color: var(--text-muted);
  font-size: 0.9rem;
  line-height: 1.5;
}

.cta {
  text-align: center;
}

.btn-primary {
  display: inline-block;
  background: var(--accent);
  color: #0a0a0a;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}
</style>
