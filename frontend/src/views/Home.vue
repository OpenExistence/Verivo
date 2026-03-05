<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          Le vote <span class="accent">décentralisé</span><br />
          pour tous
        </h1>
        <p class="hero-subtitle">
          Verivo est une plateforme de vote sécurisée et transparente. 
          Chaque vote est enregistré sur la blockchain pour une intégrité absolue.
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="btn btn-primary">
            Commencer
          </router-link>
          <router-link to="/about" class="btn btn-outline">
            En savoir plus
          </router-link>
        </div>
      </div>
      <div class="hero-visual">
        <div class="floating-card card-1">
          <span class="card-icon">🔒</span>
          <span>Sécurisé</span>
        </div>
        <div class="floating-card card-2">
          <span class="card-icon">⚡</span>
          <span>Rapide</span>
        </div>
        <div class="floating-card card-3">
          <span class="card-icon">🌍</span>
          <span>Décentralisé</span>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features">
      <h2>Pourquoi Verivo?</h2>
      <div class="features-grid">
        <div class="feature">
          <div class="feature-icon">🔐</div>
          <h3>Sécurité blockchain</h3>
          <p>Vos votes sont chiffrés et immuables sur la blockchain Ethereum.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">⚖️</div>
          <h3>Transparence</h3>
          <p>Tout le monde peut vérifier les résultats. Aucune manipulation possible.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">📱</div>
          <h3>Accessible</h3>
          <p>Interface simple et intuitive. Votez depuis n'importe où.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">🎯</div>
          <h3>Multi-types de vote</h3>
          <p>Majorité simple, qualifiée, unanimité ou vote par bloc.</p>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats">
      <div class="stat-item">
        <span class="stat-number">100%</span>
        <span class="stat-label">Transparent</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">0</span>
        <span class="stat-label">Censure</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">24/7</span>
        <span class="stat-label">Disponible</span>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <h2>Prêt à voter?</h2>
      <p>Rejoignez la communauté Verivo et participez aux décisions.</p>
      <router-link to="/register" class="btn btn-primary">
        Créer un compte
      </router-link>
    </section>
  </div>
</template>

<style scoped>
.home {
  overflow-x: hidden;
}

/* Hero */
.hero {
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  gap: 4rem;
}

.hero-content {
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 3.5rem;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.hero-title .accent {
  color: var(--accent);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  display: inline-block;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--accent);
  color: #0a0a0a;
}

.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.btn-outline {
  border: 2px solid var(--border);
  color: var(--text);
}

.btn-outline:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.hero-visual {
  position: relative;
  width: 400px;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: var(--card-bg);
  border: 1px solid var(--border);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
  animation: float 4s ease-in-out infinite;
}

.card-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 45%;
  right: 5%;
  animation-delay: 1s;
}

.card-3 {
  bottom: 15%;
  left: 25%;
  animation-delay: 2s;
}

.card-icon {
  font-size: 1.5rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

/* Features */
.features {
  padding: 6rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.features h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: transform 0.2s;
}

.feature:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature h3 {
  margin-bottom: 0.5rem;
}

.feature p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* Stats */
.stats {
  display: flex;
  justify-content: center;
  gap: 4rem;
  padding: 4rem 2rem;
  background: var(--secondary);
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 3rem;
  font-weight: 700;
  color: var(--accent);
}

.stat-label {
  color: var(--text-muted);
}

/* CTA */
.cta {
  text-align: center;
  padding: 6rem 2rem;
}

.cta h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.cta p {
  color: var(--text-muted);
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

/* Responsive */
@media (max-width: 900px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 2rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .hero-visual {
    width: 100%;
    height: 300px;
  }
  
  .stats {
    flex-wrap: wrap;
    gap: 2rem;
  }
}
</style>
