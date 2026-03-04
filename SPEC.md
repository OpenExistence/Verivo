# Verivo - Spécifications Techniques

## 1. Objectif du Projet

### 1.1 Vision
Créer une plateforme de vote électronique sécurisée permettant aux entreprises, associations et institutions d'organiser des scrutins démocratiques, transparents et inviolables.

### 1.2 Caractéristiques Cibles

| Caractéristique | Description |
|-----------------|-------------|
| **Inviolabilité** | Aucun vote ne peut être modifié ou supprimé après emission |
| **Audibilité** | Tout électeur peut vérifier que son vote a été comptabilisé |
| **Anonymat** | Impossible de relier un vote à un électeur spécifique |
| **Accessibilité** | Interface simple, intuitive, accessible à tous |

---

## 2. Architecture Fonctionnelle

### 2.1 Pages de l'Application

1. **Page d'accueil** - Landing + connexion
2. **Page d'inscription** - Création de compte + wallet
3. **Page création de scrutin** - Paramétrage + sélection des votants
4. **Page vote** - Vote pour les électeurs
5. **Page consultation scrutin** - Résultats (v2)

### 2.2 Flux Utilisateur

```
[Inscription] → [Création compte + Wallet]
       ↓
[Connexion] → [Dashboard]
       ↓
[Création scrutin] → [Sélection votants] → [Hash registre on-chain]
       ↓
[Invitation votants] → [Email]
       ↓
[Voting] → [Vote] → [Hash transaction envoyé au votant]
       ↓
[Clôture] → [Résultats]
```

---

## 3. Modèle de Données

### 3.1 Tables

```sql
-- Utilisateurs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    wallet_address VARCHAR(42) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Associations / Organisations
CREATE TABLE associations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rôles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    association_id INTEGER REFERENCES associations(id),
    role VARCHAR(50) CHECK (role IN ('admin', 'organisateur', 'votant')),
    UNIQUE(user_id, association_id)
);

-- Scrutins
CREATE TABLE scrutins (
    id SERIAL PRIMARY KEY,
    association_id INTEGER REFERENCES associations(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'closed', 'finished')),
    voting_system VARCHAR(50) DEFAULT 'majority',
    registry_hash VARCHAR(66),  -- Hash du registre des votants on-chain
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registre des votants par scrutin
CREATE TABLE votants_scrutin (
    id SERIAL PRIMARY KEY,
    scrutin_id INTEGER REFERENCES scrutins(id),
    user_id INTEGER REFERENCES users(id),
    wallet_address VARCHAR(42),
    email VARCHAR(255),
    nft_hash VARCHAR(66),  -- Hash de la transaction NFT
    has_voted BOOLEAN DEFAULT FALSE,
    vote_hash VARCHAR(66),  -- Hash de la transaction de vote
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scrutin_id, user_id)
);

-- Votes (étape 1 : en clair)
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    scrutin_id INTEGER REFERENCES scrutins(id),
    user_id INTEGER REFERENCES users(id),
    choice VARCHAR(255) NOT NULL,
    transaction_hash VARCHAR(66),
    voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scrutin_id, user_id)
);
```

---

## 4. Matrice de Priorisation - User Stories

### User Stories

| # | Persona | Titre | Détail | Priorité | MVP |
|---|---------|-------|--------|----------|-----|
| 01 | Utilisateur | Inscription utilisateur | Créer un compte avec génération automatique d'un wallet associé | Haute | Oui |
| 02 | Organisateur | Inscription organisateur | S'inscrire afin de pouvoir créer et administrer des votes | Haute | Oui |
| 03 | Votant | Inscription votant | S'inscrire afin de participer aux votes autorisés | Haute | Oui |
| 04 | Organisateur | Créer vote uninominal à deux tours | Créer un scrutin uninominal à deux tours | Moyenne | Non |
| 05 | Votant | Voter uninominal à deux tours | Participer à un scrutin à deux tours | Moyenne | Non |
| 06 | Votant | Voter pour/contre | Voter pour ou contre une résolution en Assemblée Générale | Haute | Oui |
| 07 | Organisateur | Créer vote pour/contre | Créer un vote pour ou contre une résolution | Haute | Oui |
| 08 | Organisateur | Créer vote uninominal 1 tour | Créer un scrutin majoritaire à un tour | Haute | Oui |
| 09 | Votant | Voter uninominal 1 tour | Voter pour un candidat | Haute | Oui |
| 10 | Organisateur | Score participation | Visualiser et valoriser la participation des votants | Moyenne | Oui |
| 11 | Organisateur | Consulter résultats | Consulter les résultats détaillés du vote | Haute | Oui |
| 12 | Votant | Consulter résultats | Consulter le résultat du vote | Haute | Oui |
| 13 | Auditeur | Consulter résultats avec preuves | Vérifier l'intégrité et la conformité du vote | Moyenne | Oui |
| 14 | Organisateur | Publier résultats | Publier officiellement les résultats du vote | Haute | Oui |
| 15 | Organisateur | Sélectionner votants | Définir la liste des votants autorisés | Haute | Oui |
| 16 | Système | Hasher registre votants | Générer un hash du registre et l'inscrire sur la blockchain | Haute | Oui |
| 17 | Système | Émettre NFT droit de vote | Émettre un NFT par votant pour matérialiser son droit de vote | Haute | Oui |
| 18 | Votant | Recevoir invitation | Recevoir une notification d'ouverture du vote | Haute | Oui |
| 19 | Votant | Vote unique | Ne pouvoir voter qu'une seule fois et empêcher toute modification | Haute | Oui |
| 20 | Système | Preuve de vote | Envoyer le hash de transaction et le lien explorateur | Moyenne | Oui |
| 21 | Système | Clôture automatique | Clôturer le vote automatiquement à échéance ou 100% participation | Haute | Oui |
| 22 | Organisateur | Définir durée | Paramétrer date de début et date de fin | Haute | Oui |
| 23 | Organisateur | Visualiser taux participation | Voir en temps réel le taux de participation | Haute | Oui |
| 24 | Système | Vérifier quorum 50% | Calcul automatique du respect du seuil réglementaire | Haute | Oui |
| 25 | Auditeur | Vérifier intégrité registre | Comparer le hash en base avec celui inscrit sur la blockchain | Moyenne | Oui |
| 26 | Organisateur | Gérer égalité | Définir la règle applicable en cas d'égalité | Moyenne | Non |
| 28 | Système | Vote homomorphe | Chiffrement des votes pour dépouillement sécurisé | Basse | Non |
| 29 | Organisateur | Dépouillement sécurisé | Déclencher le calcul cryptographique du résultat | Basse | Non |

---

## 5. EPICs

### EPIC 1 – Authentification & Wallet
**US :** 01, 02, 03
- Inscription utilisateur avec génération wallet
- Inscription organisateur
- Inscription votant

### EPIC 2 – Paramétrage & Création du vote
**US :** 07, 08, 15, 22
- Créer vote pour/contre
- Créer vote uninominal 1 tour
- Sélectionner votants
- Définir durée

### EPIC 3 – Sécurisation Blockchain & NFT (MVP)
**US :** 16, 17, 19, 20, 25
- Hasher registre votants (on-chain)
- Émettre NFT droit de vote
- Vote unique (irrevocable)
- Preuve de vote (hash transaction)
- Vérifier intégrité registre

### EPIC 4 – Processus de vote
**US :** 06, 09, 18, 21
- Voter pour/contre
- Voter uninominal 1 tour
- Recevoir invitation
- Clôture automatique

### EPIC 5 – Résultats & Conformité réglementaire
**US :** 10, 11, 12, 14, 23, 24
- Score participation
- Consulter résultats (organisateur)
- Consulter résultats (votant)
- Publier résultats
- Visualiser taux participation
- Vérifier quorum 50%

### EPIC 6 – Scrutins avancés
**US :** 04, 05, 26
- Créer vote uninominal à deux tours
- Voter uninominal à deux tours
- Gérer égalité

### EPIC 7 – Vote confidentiel avancé (V2)
**US :** 28, 29
- Vote homomorphe
- Dépouillement sécurisé

---

## 6. Spécifications Fonctionnelles

### 6.1 Inscription & Wallet

1. **Création de compte**
   - Email + mot de passe
   - Génération wallet automatique

2. **Association wallet**
   - Wallet lié au compte utilisateur

### 6.2 Création de Scrutin

1. **Paramétrage**
   - Titre + description
   - Date de début / fin
   - Système de vote

2. **Sélection des votants**
   - Import liste emails / wallets
   - OU sélection manuelle

3. **Publication**
   - Hash du registre des votants on-chain
   - Mint NFT pour chaque votant
   - Envoi des invitations

### 6.3 Processus de Vote

1. **Accès**
   - Seuls les personnes avec NFT peuvent voir le scrutin

2. **Vote**
   - Sélection de l'option
   - Transaction on-chain

3. **Confirmation**
   - Hash de transaction envoyé au votant
   - Lien vers block explorer

### 6.4 Clôture & Résultats

1. **Triggers de clôture**
   - Durée écoulée
   - OU 100% des votants ont votés

2. **Résultats**
   - Publication sur la page

### 6.5 Règles de Scrutin

| Règle | Détail |
|-------|--------|
| Type | Majorité simple à 1 tour |
| Égalité | À définir (US 26) |
| Durée | Au choix de l'organisateur |
| Clôture auto | Quand tout le monde a votés OU fin du délai |
| Irrévocable | On ne peut pas modifier son vote |

---

## 7. Spécifications Blockchain (Étapes)

### Étape 1 : Vote stocké en clair (MVP)
- Vote on-chain
- Vérifiable par hash de transaction

### Étape 2 : Vote homomorphe (V2)
- Chiffrement homomorphe
- Décryptage collaboratif

---

## 8. Business Model

### Opportunité

**Loi française** : Les fédérations sportives doivent avoir **50% de participation minimum** aux scrutins, vérifiable sur blockchain.

= **Grosse demande potentielle**

---

## 9. Prochaines Étapes

1. [ ] Valider les règles en cas d'égalité (US 26)
2. [ ] Mapper les US sur le diagramme d'architecture
3. [ ] POC technique
4. [ ] Architecture technique détaillée

---

*Document généré le 04-03-2026*
*Version : 0.3*
