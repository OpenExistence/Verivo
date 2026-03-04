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
4. **Page vote** - Vote pour les lecteurs
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
    registry_hash VARCHAR(66),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registre des votants par scrutin
CREATE TABLE votants_scrutin (
    id SERIAL PRIMARY KEY,
    scrutin_id INTEGER REFERENCES scrutins(id),
    user_id INTEGER REFERENCES users(id),
    wallet_address VARCHAR(42),
    email VARCHAR(255),
    nft_hash VARCHAR(66),
    has_voted BOOLEAN DEFAULT FALSE,
    vote_hash VARCHAR(66),
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

### EPIC 2 – Paramétrage & Création du vote
**US :** 07, 08, 15, 22

### EPIC 3 – Sécurisation Blockchain & NFT (MVP)
**US :** 16, 17, 19, 20, 25

### EPIC 4 – Processus de vote
**US :** 06, 09, 18, 21

### EPIC 5 – Résultats & Conformité réglementaire
**US :** 10, 11, 12, 14, 23, 24

### EPIC 6 – Scrutins avancés
**US :** 04, 05, 26

### EPIC 7 – Vote confidentiel avancé (V2)
**US :** 28, 29

---

## 6. Spécifications Détaillées

### 6.1 Gestion des Identités et Authentification

| Fonctionnalité | Description |
|----------------|-------------|
| **Inscription / Vérification d'identité** | Enregistrement des électeurs avec vérification et/ou validation par l'organisation |
| **Authentification forte** | MFA (Multi-Factor Authentication), certificats numériques ou clés cryptographiques |
| **Séparation identité / vote** | Mécanisme de "blind signature" ou ZKP pour garantir l'anonymat tout en prouvant l'éligibilité |

#### Flux d'authentification
```
Utilisateur → Inscription → Vérification email
                       ↓
              Vérification identité (KYC optionnel)
                       ↓
              Génération wallet automatique
                       ↓
              MFA activé (optionnel)
```

### 6.2 Gestion des Scrutins

| Fonctionnalité | Description |
|----------------|-------------|
| **Création de scrutin** | Définir le type (majorité simple, proportionnel, pondéré…), la durée, les candidats/options |
| **Paramétrage des droits** | Qui peut voter, quorum minimum, poids des votes si applicable |
| **Cycle de vie** | Brouillon → Ouvert → Clos → Dépouillé → Archivé |
| **Multi-tours** | Support de scrutins à plusieurs tours si nécessaire |

#### Cycle de vie d'un scrutin
```
[Brouillon] → [Ouvert] → [Clos] → [Dépouillé] → [Archivé]
     ↑            ↓          ↓           ↓            ↓
     └────────────┴───────────┴───────────┴────────────┘
```

### 6.3 Processus de Vote

| Fonctionnalité | Description |
|----------------|-------------|
| **Chiffrement bout-en-bout** | Le vote est chiffré côté client avant envoi |
| **Non-répudiation** | Preuve que le vote a été enregistré (reçu cryptographique) |
| **Unicité** | Un électeur = un vote (empêcher le double vote) |
| **Modification contrôlée** | Possibilité (ou non) de modifier son vote tant que le scrutin est ouvert |
| **Vote blanc / abstention** | Support explicite |

#### Flux de vote
```
[Votant se connecte] → [Vérification droit de vote]
                           ↓
              [Prépare vote (chiffré client)]
                           ↓
              [Soumet vote + preuve ZKP]
                           ↓
              [Reçu cryptographique]
                           ↓
              [Hash envoyé au votant]
```

### 6.4 Dépouillement et Résultats

| Fonctionnalité | Description |
|----------------|-------------|
| **Déchiffrement distribué** | Clé de déchiffrement partagée / aucun acteur seul ne peut déchiffrer |
| **Calcul vérifiable** | Le résultat peut être recalculé indépendamment par tout auditeur |
| **Publication** | Résultats accessibles avec preuve cryptographique d'intégrité |

### 6.5 Auditabilité

| Fonctionnalité | Description |
|----------------|-------------|
| **Journal d'audit** | Traçabilité complète des événements (création, ouverture, votes chiffrés, clôture, dépouillement) |
| **Vérification individuelle** | Chaque électeur peut vérifier que son vote a été comptabilisé |
| **Vérification universelle** | Tout observateur peut vérifier l'intégrité globale du scrutin |
| **Export de preuves** | Génération de rapports d'audit téléchargeables |

#### Événements audités
- Création du scrutin
- Modification des paramètres
- Ouverture du vote
- Votes reçus (commitments)
- Clôture du scrutin
- Dépouillement
- Publication des résultats

### 6.6 Accessibilité et UX

| Fonctionnalité | Description |
|----------------|-------------|
| **Multi-plateforme** | Web responsive, mobile (PWA ou natif) |
| **Accessibilité WCAG 2.1 AA** | Lecteurs d'écran, navigation clavier, contrastes |
| **Multilingue** | i18n dès la conception |
| **Mode hors-ligne partiel** | Possibilité de préparer son vote hors-ligne puis de le soumettre |

### 6.7 Administration et Gouvernance

| Rôle | Permissions |
|------|-------------|
| **Super-admin** | Gestion globale de la plateforme |
| **Organisateur** | Créer et gérer les scrutins de son organisation |
| **Auditeur** | Vérifier l'intégrité des scrutins |
| **Électeur** | Voter dans les scrutins autorisés |

#### Tableaux de bord
- Suivi en temps réel de la participation (sans révéler les votes)
- Gestion des organisations
- Export de données

### 6.8 Sécurité

| Fonctionnalité | Description |
|----------------|-------------|
| **Protection contre les attaques** | Anti-DDoS, rate limiting, anti-replay |
| **Chiffrement au repos et en transit** | Chiffrement des données stockées |
| **Audit de sécurité** | Code auditable, pentests réguliers |
| **RGPD** | Droit à l'oubli compatible avec l'immuabilité (données personnelles hors-chaîne) |

---

## 7. Règles de Scrutin

| Règle | Détail |
|-------|--------|
| Type | Majorité simple à 1 tour (MVP) |
| Égalité | À définir (US 26) |
| Durée | Au choix de l'organisateur |
| Clôture auto | Quand tout le monde a votés OU fin du délai |
| Irrévocable | On ne peut pas modifier son vote |

---

## 8. Spécifications Blockchain

### Étape 1 : Vote stocké en clair (MVP)
- Vote on-chain
- Vérifiable par hash de transaction
- NFT de droit de vote

### Étape 2 : Vote homomorphe (V2)
- Chiffrement homomorphe
- Décryptage distribué (MPC)
- Preuves ZKP

---

## 9. Business Model

**Loi française** : Les fédérations sportives doivent avoir **50% de participation minimum** aux scrutins, vérifiable sur blockchain.

= **Grosse demande potentielle**

---

## 10. Prochaines Étapes

1. [ ] Mapper les US sur le diagramme d'architecture
2. [ ] POC technique
3. [ ] Architecture technique détaillée

---

*Document généré le 04-03-2026*
*Version : 0.4*
