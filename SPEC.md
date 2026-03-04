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

### 3.2 Schéma Relationnel

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   users    │       │ associations │       │   scrutins  │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ id          │       │ id           │       │ id          │
│ email       │       │ name         │       │ title       │
│ wallet_addr │◄──────│ created_at   │       │ start_date  │
│ created_at  │       └──────────────┘       │ end_date    │
└─────────────┘              │               │ status      │
        │                    │               └──────┬──────┘
        │                    │                      │
        ▼                    ▼                      ▼
┌─────────────────────────────────────────────────────────┐
│                    votants_scrutin                      │
├─────────────────────────────────────────────────────────┤
│ scrutin_id │ user_id │ wallet │ nft_hash │ has_voted │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                    ┌─────────┐
                    │  votes  │
                    ├─────────┤
                    │ choice  │
                    │ tx_hash │
                    └─────────┘
```

---

## 4. Spécifications Fonctionnelles

### 4.1 Inscription & Wallet

1. **Création de compte**
   - Email + mot de passe
   - Génération wallet (ou import)

2. **Association wallet**
   - Wallet lié au compte utilisateur
   - Stockage sécurisé

### 4.2 Création de Scrutin

1. **Paramétrage**
   - Titre + description
   - Date de début / fin
   - Système de vote

2. **Sélection des votants**
   - Import liste emails / wallets
   - OU sélection manuelle depuis la liste des membres

3. **Publication**
   - Hash du registre des votants
   - Mint NFT pour chaque votant
   - Envoi des invitations

### 4.3 Processus de Vote

1. **Accès**
   - Seuls les personnes avec NFT peuvent voir le scrutin
   - Lien dans l'email d'invitation

2. **Vote**
   - Sélection de l'option
   - Confirmation
   - Transaction on-chain

3. **Confirmation**
   - Hash de transaction envoyé au votant
   - Lien vers block explorer
   - Lien vers page de vérification

### 4.4 Clôture & Résultats

1. **Triggers de clôture**
   - Durée écoulée
   - OU 100% des votants ont voted

2. **Résultats**
   - Calcul automatique
   - Publication sur la page

### 4.5 Règles de Scrutin

| Règle | Détail |
|-------|--------|
| Type | Majorité simple à 1 tour |
| Égalité | À définir (reculer ? nouveau vote ?) |
| Durée | Au choix de l'organisateur |
| Clôture auto | Quand tout le monde a voted OU fin du délai |
| Irrévocable | On ne peut pas modifier son vote |

---

## 5. Spécifications Blockchain (Étapes)

### Étape 1 : Vote stocké en clair
- Vote on-chain
- Vérifiable par hash de transaction

### Étape 2 : Vote homomorphe
- Chiffrement homomorphe
- Compteur sans révéler les votes
- Décryptage collaboratif

### Éléments on-chain
- Hash du registre des votants
- NFT de droit de vote (quasi soul-bound)
- Transactions de vote
- Résultats hashés

---

## 6. Vocabulaire

À définir et mettre à disposition des utilisateurs :

- Scrutin / Vote / Élection
- Votant / Électeur / Participant
- Organisateur / Administrateur
- Bulletins / Choix / Option
- Majorité / Quorum
- etc.

---

## 7. Business Model

### Opportunité

**Loi française** : Les fédérations sportives doivent avoir **50% de participation minimum** aux scrutins, vérifiable sur blockchain.

= **Grosse demande potentielle**

---

## 8. Prochaines Étapes

1. [ ] Valider les règles en cas d'égalité
2. [ ] Définir le vocabulaire
3. [ ] POC technique
4. [ ] Architecture technique détaillée

---

*Document généré le 04-03-2026*
*Version : 0.2*
