# Verivo - Feuille de Route

## Phase 1 : Fondations (Semaine 1-2)

### 1.1 Architecture Technique
- [ ] Choisir la blockchain (Ethereum L2, Polygon, StarkNet, Avalanche?)
- [ ] Définir stack technique frontend (React, Vue, Next.js?)
- [ ] Définir stack technique backend (Node.js, Python, Go?)
- [ ] Définir base de données (PostgreSQL, MongoDB?)
- [ ] Conception architecture API REST/GraphQL
- [ ] Schéma base de données final

### 1.2 Infrastructure
- [ ] Setup environnement dev
- [ ] Setup CI/CD
- [ ] Déploiement testnet blockchain
- [ ] Setup monitoring/logging

---

## Phase 2 : Authentification & Wallet (Semaine 3-4)

### 2.1 Smart Contract
- [ ] Déployer smart contract NFT "droit de vote"
- [ ] Implémenter mint/burn NFT
- [ ] Implémenter transfert quasi-soul-bound

### 2.2 Backend Auth
- [ ] API inscription/login
- [ ] Intégration wallet (WalletConnect)
- [ ] Génération wallet utilisateur
- [ ] Authentification MFA (optionnel)

### 2.3 Frontend
- [ ] Page inscription
- [ ] Page connexion
- [ ] Intégration wallet Metamask/WalletConnect
- [ ] Dashboard utilisateur

---

## Phase 3 : Gestion des Scrutins (Semaine 5-6)

### 3.1 Smart Contract Scrutin
- [ ] Smart contract scrutin (création, ouverture, clôture)
- [ ] Gestion des types de vote (pour/contre, uninominal)
- [ ] Vérification droit de vote (NFT holder)

### 3.2 Backend
- [ ] API création scrutin
- [ ] API gestion votants
- [ ] Hash registre votants on-chain
- [ ] Mint NFT pour chaque votant
- [ ] Système d'invitation email

### 3.3 Frontend - Organisateur
- [ ] Page création scrutin
- [ ] Formulaire paramétrage (titre, dates, type)
- [ ] Import/selection votants
- [ ] Dashboard organisateur

---

## Phase 4 : Processus de Vote (Semaine 7-8)

### 4.1 Smart Contract Vote
- [ ] Enregistrement vote on-chain
- [ ] Vérification unicité (1 vote par personne)
- [ ] Preuve de vote (transaction hash)
- [ ] Clôture automatique

### 4.2 Backend Vote
- [ ] API soumission vote
- [ ] Vérification droit de vote
- [ ] Envoi confirmation (hash + email)
- [ ] Calcul participation temps réel

### 4.3 Frontend Vote
- [ ] Page liste scrutins (votant)
- [ ] Page vote
- [ ] Confirmation vote
- [ ] Vérification vote personnel

---

## Phase 5 : Résultats & Audit (Semaine 9-10)

### 5.1 Résultats
- [ ] Calcul résultats (majorité simple)
- [ ] Publication résultats
- [ ] Gestion égalité
- [ ] Vérification quorum 50%

### 5.2 Audit
- [ ] Journal d'audit complet
- [ ] Vérification intégrité registre
- [ ] Export rapports PDF/CSV
- [ ] Page résultats publics

### 5.3 Notifications
- [ ] Email clôture scrutin
- [ ] Notification résultats publiés

---

## Phase 6 : Tests & Sécurité (Semaine 11)

### 6.1 Tests
- [ ] Tests unitaires smart contracts
- [ ] Tests d'intégration API
- [ ] Tests e2e frontend
- [ ] Audit code interne

### 6.2 Sécurité
- [ ] Audit sécurité externe (pentest)
- [ ] Bug bounty
- [ ] Documentation sécurité

---

## Phase 7 : Déploiement Production (Semaine 12)

### 7.1 Production
- [ ] Déploiement mainnet blockchain
- [ ] Déploiement backend production
- [ ] Déploiement frontend production
- [ ] SSL/HTTPS
- [ ] Backup & disaster recovery

### 7.2 Légal
- [ ] Mentions légales
- [ ] CGV/CGU
- [ ] Politique de confidentialité
- [ ] Conformité RGPD

---

## Fonctionnalités V2 (Post-MVP)

- [ ] Vote uninominal à 2 tours
- [ ] Jugement majoritaire
- [ ] Vote homomorphe
- [ ] Déchiffrement distribué MPC
- [ ] Multi-tours
- [ ] Vote pondéré
- [ ] PWA/Mobile natif
- [ ] Mode hors-ligne
- [ ] Multilingue

---

## Livrables

| Livrable | Description |
|----------|-------------|
| Smart Contracts | NFT + Scrutin + Vote |
| Backend API | REST/GraphQL complet |
| Frontend Web | Application responsive |
| Documentation | Technique + Utilisateur |
| Audit sécurité | Rapport pentest |

---

## Estimation Timeline

```
Phase 1-3 : 6 semaines
Phase 4-5 : 4 semaines  
Phase 6-7 : 2 semaines
─────────────────────
TOTAL MVP : ~12 semaines
```

---

*Feuille de route générée le 04-03-2026*
