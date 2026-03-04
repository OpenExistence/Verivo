# Verivo - Spécifications Techniques

## 1. Objectif du Projet

### 1.1 Vision
Créer une plateforme de vote électronique sécurisée permettant aux entreprises, associations et institutions d'organiser des scrutins démocratiques, transparents et inviolables.

### 1.2 Caractéristiques Cibles

| Caractéristique | Description |
|-----------------|-------------|
| **Inviolabilité** | Aucun vote ne peut être modifié ou supprimé après émission |
| **Audibilité** | Tout électeur peut vérifier que son vote a été comptabilisé |
| **Anonymat** | Impossible de relier un vote à un électeur spécifique |
| **Accessibilité** | Interface simple, intuitive, accessible à tous |
| **Anti-coercition** | Vote non réutilisable, imposible de prouver comment on a vote |
| **Rapidité** | Résultats disponibles rapidement après la fin du scrutin |

---

## 2. Architecture Fonctionnelle

### 2.1 Vue d'Ensemble

```
┌──────────────────────────────────────────────────────────────────┐
│                           UTILISATEURS                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐       │
│  │   Électeur │      │Organisateur │      │   Auditeur   │       │
│  │  (Mobile)  │      │   (Web)     │      │  (Optionnel) │       │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘       │
│         │                    │                     │              │
│         └────────────────────┼─────────────────────┘              │
│                              ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                      BACKEND API                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │ │
│  │  │Auth      │  │Scrutin   │  │Vote      │  │Results   │   │ │
│  │  │Service   │  │Service   │  │Service   │  │Service   │   │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                    │
│         ┌────────────────────┼────────────────────┐              │
│         ▼                    ▼                    ▼              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      │
│  │   Wallet    │      │  Blockchain │      │   Storage   │      │
│  │   Service   │      │  Network    │      │  (IPFS)     │      │
│  └─────────────┘      └─────────────┘      └─────────────┘      │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Trois Blocs Technologiques

#### Bloc 1 : Blockchain & Backend

**Objectif** : Garantir l'inviolabilité et l'audibilité

**Technologies candidates** :
- Blockchain : Ethereum L2, Polygon, StarkNet, zkSync, Avalanche
- Smart Contracts : Solidity, Cairo
- Cryptographie : ZKP (Zero-Knowledge Proof), MPC (Multi-Party Computation), Chiffrement Homomorphe

**Fonctionnalités** :
1. **Identification des votants**
   - NFT quasi-soul-bound (transférable une fois sous conditions)
   - Vérification KYC/AML

2. **Anonymat du vote**
   - Preuves à connaissance nulle (ZKP)
   - Calcul multipartite sécurisé (MPC)
   - Chiffrement homomorphe

3. **Systèmes de scrutin**
   - Vote uninominal (1, 2 tours)
   - Vote plurinominal
   - Jugement majoritaire
   - Approval voting
   - Score voting

4. **Transactions invisibles**
   - Gasless transactions
   - Account abstraction

#### Bloc 2 : Wallet Mobile

**Objectif** : Interface grand public pour les électeurs

**Technologies candidates** :
- Framework : React Native, Flutter, Swift/Kotlin natif
- Wallet : WalletConnect, RainbowKit, wagmi
- Security : Secure Enclave (iOS), TEE (Android)

**Fonctionnalités** :
1. **Gestion de wallet**
   - Wallet non-custodial
   - Stockage sécurisé des clés (Secure Enclave)
   - Recovery seed phrase

2. **Parcours utilisateur**
   - Vérification d'identité (KYC)
   - Liste des scrutins accessibles
   - Vote (sélection, confirmation)
   - Consultation des résultats
   - Audit de son propre vote

3. **Notifications**
   - Rappel de vote
   - Résultats publiés

#### Bloc 3 : Interface Organisateur (Web)

**Objectif** : Outil de gestion des scrutins pour les organisations

**Technologies candidates** :
- Frontend : Vue.js, React, Next.js
- Backend API : Node.js, Python, Go

**Fonctionnalités** :
1. **Authentification**
   - Login par wallet mobile (WalletConnect)
   - OAuth (optionnel)

2. **Gestion des scrutins**
   - Création de scrutin
   - Paramétrage (type, dates, participants)
   - Import des électeurs
   - Définition des options de vote

3. **Administration**
   - Ouverture/fermeture du scrutin
   - Compilation homomorphe
   - Décryptage MPC

4. **Résultats**
   - Consultation en temps réel
   - Export PDF/CSV
   - Certificat de résultats

---

## 3. Spécifications Techniques Détaillées

### 3.1 Smart Contract - Structure

```solidity
// Pseudo-code structure Smart Contract

contract Verivo {
    // Enregistrement des organisations
    struct Organization {
        address owner;
        string name;
        bool isActive;
    }
    
    // Définition d'un scrutin
    struct Scrutin {
        uint256 id;
        address organization;
        string title;
        uint8 votingSystem;  // 0: uninominal, 1: plurinominal, 2: judgment, etc.
        uint256 startTime;
        uint256 endTime;
        bool isActive;
        bytes32 merkleRoot;  // Racine de l'arbre de Merkle des voters
    }
    
    // Vote encrypté
    struct EncryptedVote {
        bytes32 commitment;  // Commitment ZKP
        bytes ciphertext;    // Vote encrypté
        bytes proof;         // Preuve ZKP
    }
    
    // Événements
    event ScrutinCreated(uint256 indexed scrutinId);
    event VoteCast(uint256 indexed scrutinId, bytes32 commitment);
    event ScrutinClosed(uint256 indexed scrutinId);
    event ResultsPublished(uint256 indexed scrutinId);
}
```

### 3.2 Protocole de Vote Anonyme

```
1. INSCRIPTION
   Électeur → Wallet → Vérification identité → Mint NFT votant
   
2. CRÉATION SCRUTIN
   Organisateur → Définit paramètres → Déploie smart contract
   + Distribue Merkle tree des électeurs autorisés
   
3. VOTE
   Électeur → Génère clé temporaire (rotation)
   → Chiffre vote avec clé publique du scrutin
   → Génère ZKP (vote valide, droit de vote)
   → Soumet transaction avec commitment + proof
   
4. COMPILATION
   Smart Contract → Vérifie ZKP
   → Stocke commitment (pas le vote!)
   → Met à jour compteur
   
5. DÉPOUILLEMENT
   Organisateur → Initie MPC (N participants)
   → Décryptage collaboratif
   → Publication résultats + preuve de décryptage
   
6. AUDIT
   Électeur → Vérifie commitment dans la chaîne
   → Vérifie preuve ZKP
   → Confirme que son vote est inclus
```

### 3.3 Comparatif Systèmes de Vote

| Système | Avantages | Inconvénients |
|---------|-----------|---------------|
| Uninominal 1 tour | Simple, connu | Risque vote utile |
| Uninominal 2 tours | Choix définitif | Durée |
| Plurinominal | Multiples choix | Stratégie de vote |
| Jugement majoritaire | Expression nuancée | Calcul complexe |
| Approval | Simple | Pas de gradation |
| Score | Expression riche | Manipulation possible |

---

## 4. Périmètre MVP (À définir)

Pour respecter les contraintes de certification Alyra, un périmètre réduit est nécessaire.

### 4.1 Fonctionnalités MVP

- [ ] Authentification wallet
- [ ] Création de scrutin (type basique)
- [ ] Vote simple (uninominal)
- [ ] Résultats basiques

### 4.2 Blockchain MVP

- [ ] Déploiement sur testnet
- [ ] Smart contract vote basique
- [ ] Intégration WalletConnect

---

## 5. Risques et Contraintes

### 5.1 Risques Techniques

1. **Complexité cryptographique**
   - ZKP/MPC : expertise rare
   - Chiffrement homomorphe : performant?

2. **Scalabilité**
   - Thousands d'utilisateurs simultanés
   - Coût gas sur L1

3. **UX**
   - Complexité technique cachée à l'utilisateur
   - Onboarding non-crypto

### 5.2 Contraintes Réglementaires

- Certification needed?
- RGPD compatible?
- LOI n° 2016-1321 pour les élections professionnelles

---

## 6. Prochaines Étapes

1. [ ] Valider le périmètre MVP avec l'équipe
2. [ ] Choisir la blockchain
3. [ ] POC technique (vote simple sur testnet)
4. [ ] Définition architecture détaillée
5. [ ] Répartition des tâches

---

*Document généré le 04-03-2026*
*Version : 0.1*
