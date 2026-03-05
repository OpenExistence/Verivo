"""
DAO Voting Backend - FastAPI + SQLite
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from datetime import datetime

app = FastAPI(title="DAO Voting API")

# Configuration DB
DB_PATH = "dao_voting.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Table des propositions
    c.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            vote_count INTEGER DEFAULT 0,
            executed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table des votes
    c.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            voter_address TEXT NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id),
            UNIQUE(proposal_id, voter_address)
        )
    """)
    
    # Table des droits de vote (synchro blockchain)
    c.execute("""
        CREATE TABLE IF NOT EXISTS voting_rights (
            address TEXT PRIMARY KEY,
            has_nft BOOLEAN DEFAULT FALSE,
            granted_at TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Modèles Pydantic
class ProposalCreate(BaseModel):
    description: str

class ProposalResponse(BaseModel):
    id: int
    description: str
    vote_count: int
    executed: bool
    created_at: str

class VoteRequest(BaseModel):
    voter_address: str
    signature: Optional[str] = None  # Pour future authentification

class GrantVotingRightRequest(BaseModel):
    address: str

# Initialiser DB au démarrage
@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# === PROPOSALS ===

@app.get("/proposals", response_model=List[ProposalResponse])
def get_proposals():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proposals ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "description": row["description"],
            "vote_count": row["vote_count"],
            "executed": bool(row["executed"]),
            "created_at": row["created_at"]
        }
        for row in rows
    ]

@app.post("/proposals", response_model=ProposalResponse)
def create_proposal(proposal: ProposalCreate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO proposals (description) VALUES (?)",
        (proposal.description,)
    )
    proposal_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": proposal_id,
        "description": proposal.description,
        "vote_count": 0,
        "executed": False,
        "created_at": datetime.now().isoformat()
    }

@app.get("/proposals/{proposal_id}", response_model=ProposalResponse)
def get_proposal(proposal_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return {
        "id": row["id"],
        "description": row["description"],
        "vote_count": row["vote_count"],
        "executed": bool(row["executed"]),
        "created_at": row["created_at"]
    }

@app.post("/proposals/{proposal_id}/vote")
def vote_proposal(proposal_id: int, vote: VoteRequest):
    # Note: La vérification NFT se fait côté smart contract
    # Ici on enregistre juste le vote en local pour l'historique
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Vérifier que la proposition existe
    c.execute("SELECT executed FROM proposals WHERE id = ?", (proposal_id,))
    proposal = c.fetchone()
    
    if not proposal:
        conn.close()
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if proposal[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Proposal already executed")
    
    try:
        c.execute(
            "INSERT INTO votes (proposal_id, voter_address) VALUES (?, ?)",
            (proposal_id, vote.voter_address)
        )
        c.execute(
            "UPDATE proposals SET vote_count = vote_count + 1 WHERE id = ?",
            (proposal_id,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Already voted")
    
    conn.close()
    return {"status": "voted", "proposal_id": proposal_id, "voter": vote.voter_address}

# === VOTING RIGHTS ===

@app.post("/voting/grant")
def grant_voting_right(request: GrantVotingRightRequest):
    """Enregistre un droit de vote (sync avec blockchain)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO voting_rights (address, has_nft, granted_at) VALUES (?, TRUE, ?)",
        (request.address, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    
    return {"status": "granted", "address": request.address}

@app.get("/voting/check/{address}")
def check_voting_right(address: str):
    """Vérifie si une adresse peut voter"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT has_nft, granted_at FROM voting_rights WHERE address = ?", (address,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {"address": address, "can_vote": bool(row[0]), "granted_at": row[1]}
    
    return {"address": address, "can_vote": False, "granted_at": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
