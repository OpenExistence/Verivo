# Verivo

MVP pour un système de vote basé sur NFT (ERC-721) sur Sepolia.

## Stack

- **Blockchain:** Solidity (ERC-721), réseau Sepolia
- **Backend:** FastAPI + SQLite
- **Frontend:** Vue 3 + Vite
- **Testnet:** Sepolia

## Structure

```
dao-voting-mvp/
├── contracts/         # Smart contracts Solidity
├── backend/           # API REST Python
├── frontend/          # Vue 3 app
└── tests/             # Tests
```

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Variables d'environnement

Copiez `.env.example` en `.env` et configurez:

- `VITE_API_URL` - URL du backend
- `VITE_CONTRACT_ADDRESS` - Adresse du contrat déployé
- `VITE_INFURA_PROJECT_ID` - ID projet Infura

## Fonctionnalités MVP

1. **Claim NFT** - Mint du NFT "droit de vote"
2. **Propositions** - Liste et création de propositions
3. **Vote** - Vote sur les propositions (via NFT)
4. **Execution** - Exécution des propositions validées
