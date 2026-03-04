# Verivo

**Solution de vote sécurisée pour entreprises, associations et institutions**

---

## Résumé Projet

Verivo est une solution de vote électronique sécurisée visant à garantir :
- ✅ **Inviolabilité** : Impossibilité de falsifier les votes
- ✅ **Audibilité** : Traçabilité complète vérifiable
- ✅ **Anonymat** : Impossibilité de relier un vote à un électeur
- ✅ **Accessibilité** : Interface intuitive grand public

## Solution Technologique

### Trois Blocs Technologiques

#### 1. Blockchain & Backend
- Smart-contracts et NFT pour l'identification des votants (quasi soul-bound)
- ZKP + MPC + Chiffrement homomorphe pour l'anonymat du vote
- Rotation de wallet pour casser le lien entre les votes d'une même personne
- Smart-contracts pour différents systèmes de scrutins (uninominal à x tours, jugement majoritaire...)
- Transactions sans frais (blockchain invisible pour l'utilisateur)

#### 2. Wallet Mobile
- Application mobile personnalisée
- Wallets non custodiaux avec enclaves sécurisées natives (Secure Enclave)
- Parcours de vérification d'identité
- Parcours des scrutins accessibles
- Parcours de scrutin
- Consultations des résultats
- Vérifications du résultat d'un scrutin (audit utilisateur)

#### 3. Interface Organisateur
- Application web pour organiser et paramétrer un scrutin
- Authentification par le wallet mobile
- Paramétrage et création d'un nouveau scrutin
- Action d'administration d'un scrutin (MPC, compilation homomorphe...)
- Consultation des scrutins ultérieurs

---

## Équipe

| Rôle | Nom |
|------|-----|
| Lead Blockchain | Etienne Wallet |
| Lead UX/UI | Solène Mallié |
| Lead Développeur | Arnaud Calvo |
| Développeur | Clément Conand |
| Lead Produit | Philippe Mbongue |

---

## Informations Projet

- **Date de début** : 23-02-2026
- **Statut** : En cours de définition du périmètre
- **Certification** : En perspective avec Alyra

---

## Périmètre Initial (À définir)

> ⚠️ Solution large - définition d'un premier périmètre plus raisonnable nécessaire pour les contraintes de certification Alyra

---

## Architecture (À définir)

```
┌─────────────────────────────────────────────────────────┐
│                     BLOCKCHAIN                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Smart      │  │  NFT        │  │  ZKP/MPC    │  │
│  │  Contracts  │  │  Identity   │  │  Encryption │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────┘
         ▲                ▲                ▲
         │                │                │
    ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
    │ Backend │     │ Backend │     │ Backend │
    └────┬────┘     └────┬────┘     └────┬────┘
         │                │                │
┌────────┴───────┐ ┌────┴───────┐ ┌────┴───────┐
│  Wallet Mobile │ │  Interface │ │  API       │
│               │ │  Web       │ │  Externe   │
└───────────────┘ └────────────┘ └────────────┘
```

---

## Choix Technologiques (À définir)

- [ ] **Blockchain** : ?
- [ ] **Frontend Mobile** : ?
- [ ] **Frontend Web** : ?
- [ ] **Backend** : ?
- [ ] **Base de données** : ?

---

## License

À définir...
