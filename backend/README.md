# Backend DAO Voting - FastAPI + SQLite

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn main:app --reload
```

## Endpoints

### Proposals

- `GET /proposals` - Liste toutes les propositions
- `POST /proposals` - Crée une proposition
- `GET /proposals/{id}` - Détails d'une proposition
- `POST /proposals/{id}/vote` - Voter (via contrat blockchain)

### Voting Rights

- `POST /voting/grant` - Grant un NFT de vote
- `GET /voting/check/{address}` - Vérifie si une adresse peut voter

### Health

- `GET /health` - Status de l'API
