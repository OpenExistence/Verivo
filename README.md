# DAO Voting MVP

MVP pour un système de vote basé sur NFT (ERC-721) sur Sepolia.

## Stack

- **Blockchain:** Solidity (ERC-721), réseau Sepolia
- **Backend:** FastAPI + SQLite
- **Testnet:** Sepolia

## Structure

```
dao-voting-mvp/
├── contracts/         # Smart contracts Solidity
├── backend/           # API REST Python
└── tests/            # Tests
```

## Fonctionnalités MVP

1. Mint du NFT "droit de vote" → 1 adresse = 1 NFT
2. Vérification du droit de vote via le contrat
3. API pour soumettre et voter des propositions
