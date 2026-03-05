# Verivo

Système de vote décentralisé sécurisé sur blockchain Ethereum.

## Description

Verivo est une plateforme de vote DAO où chaque vote est enregistré sur la blockchain pour garantir transparence et intégrité.

## Fonctionnalités

- 🔐 Authentification utilisateur (email/mot de passe)
- 🔒 Votes sécurisés sur blockchain
- ⚖️ Multiple types de vote (majorité simple, qualifiée, unanimité)
- 👥 Gestion des votants par proposition
- 📊 Suivi des résultats en temps réel

## Installation

### Prérequis

- Node.js 18+
- Python 3.9+
- SQLite

### Backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python main.py
```

Le backend sera accessible sur `http://localhost:8000`

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer en développement
npm run dev
```

Le frontend sera accessible sur `http://localhost:5173`

## Configuration

### Backend (.env)

```env
# Pas de configuration nécessaire pour le développement local
```

### Frontend (.env)

Créez un fichier `.env` dans `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

## API Endpoints

### Auth

- `POST /api/register` - Inscription
- `POST /api/login` - Connexion
- `GET /api/me` - Profil utilisateur

### Propositions

- `GET /api/proposals` - Liste des propositions
- `POST /api/proposals` - Créer une proposition
- `POST /api/proposals/{id}/start` - Ouvrir le vote
- `POST /api/provotes/{id}/vote` - Voter

### Types de vote

- `GET /api/vote-types` - Liste des types de vote

## Blockchain

Les contrats intelligents sont développés en Solidity et déployés sur le réseau Sepolia (testnet).

### Déploiement

```bash
# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés

# Compiler les contrats
npx hardhat compile

# Déployer sur Sepolia
npx hardhat run scripts/deploy.js --network sepolia
```

## Tech Stack

- **Frontend**: Vue 3 + Vite
- **Backend**: FastAPI + Python
- **Database**: SQLite
- **Blockchain**: Solidity + Hardhat
- **Réseau**: Ethereum Sepolia (testnet)

## Licence

MIT
