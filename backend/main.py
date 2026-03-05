"""
DAO Voting Backend - FastAPI + SQLite
Schéma complet avec persons, roles, types de votes, votes
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import sqlite3
from datetime import datetime

app = FastAPI(title="DAO Voting API")

DB_PATH = "dao_voting.db"

# === ENUMS ===
class RoleEnum(str, Enum):
    ADMIN = "admin"
    VOTER = "voter"
    OBSERVER = "observer"

class VoteStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"

class VoteTypeEnum(str, Enum):
    SIMPLE_MAJORITY = "simple_majority"
    QUALIFIED_MAJORITY = "qualified_majority"
    UNANIMOUS = "unanimous"
    BLOC_VOTE = "bloc_vote"

# === MODELS PYDANTIC ===

class PersonCreate(BaseModel):
    address: str
    name: Optional[str] = None
    email: Optional[str] = None
    role: RoleEnum = RoleEnum.VOTER

class PersonResponse(BaseModel):
    id: int
    address: str
    name: Optional[str]
    email: Optional[str]
    role: str
    created_at: str

class VoteTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    required_percentage: int = 50  # Pour majority qualifié

class VoteTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    required_percentage: int

class ProposalCreate(BaseModel):
    title: str
    description: str
    vote_type: VoteTypeEnum = VoteTypeEnum.SIMPLE_MAJORITY
    voters: Optional[List[str]] = []

class ProposalResponse(BaseModel):
    id: int
    title: str
    description: str
    vote_type: str
    vote_count: int
    status: str
    voting_open: bool
    created_at: str

class VoteRequest(BaseModel):
    voter_address: str

class VoteResponse(BaseModel):
    id: int
    proposal_id: int
    voter_address: str
    vote: bool
    status: str
    voted_at: str

# === DATABASE INIT ===

def init_db():
    """Initialize database with full schema"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Persons / Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE NOT NULL,
            name TEXT,
            email TEXT,
            role TEXT DEFAULT 'voter',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Vote Types
    c.execute("""
        CREATE TABLE IF NOT EXISTS vote_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            required_percentage INTEGER DEFAULT 50
        )
    """)
    
    # Insert default vote types
    default_types = [
        ('simple_majority', 'Majorité simple (50% + 1)', 50),
        ('qualified_majority', 'Majorité qualifié (66%+)', 66),
        ('unanimity', 'Unanimité (100%)', 100),
        ('bloc_vote', 'Vote par bloc', 50)
    ]
    c.executemany(
        "INSERT OR IGNORE INTO vote_types (name, description, required_percentage) VALUES (?, ?, ?)",
        default_types
    )
    
    # Proposals
    c.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            vote_type_id INTEGER,
            vote_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            voting_open BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vote_type_id) REFERENCES vote_types(id)
        )
    """)
    
    # Proposal Voters (who can vote)
    c.execute("""
        CREATE TABLE IF NOT EXISTS proposal_voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            voter_address TEXT NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id),
            UNIQUE(proposal_id, voter_address)
        )
    """)
    
    # Votes
    c.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            voter_address TEXT NOT NULL,
            vote BOOLEAN NOT NULL,
            status TEXT DEFAULT 'approved',
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id),
            UNIQUE(proposal_id, voter_address)
        )
    """)
    
    conn.commit()
    conn.close()

# === ROUTES ===

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# === PERSONS ===

@app.get("/persons", response_model=List[PersonResponse])
def get_persons():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM persons ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/persons", response_model=PersonResponse)
def create_person(person: PersonCreate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO persons (address, name, email, role) VALUES (?, ?, ?, ?)",
        (person.address, person.name, person.email, person.role)
    )
    person_id = c.lastrowid
    conn.commit()
    c.execute("SELECT * FROM persons WHERE id = ?", (person_id,))
    row = c.fetchone()
    conn.close()
    return dict(row)

@app.get("/persons/{address}", response_model=PersonResponse)
def get_person(address: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM persons WHERE address = ?", (address,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Person not found")
    return dict(row)

# === VOTE TYPES ===

@app.get("/vote-types", response_model=List[VoteTypeResponse])
def get_vote_types():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM vote_types")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/vote-types", response_model=VoteTypeResponse)
def create_vote_type(vote_type: VoteTypeCreate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO vote_types (name, description, required_percentage) VALUES (?, ?, ?)",
        (vote_type.name, vote_type.description, vote_type.required_percentage)
    )
    vt_id = c.lastrowid
    conn.commit()
    c.execute("SELECT * FROM vote_types WHERE id = ?", (vt_id,))
    row = c.fetchone()
    conn.close()
    return dict(row)

# === PROPOSALS ===

@app.get("/proposals", response_model=List[ProposalResponse])
def get_proposals():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT p.*, vt.name as vote_type 
        FROM proposals p 
        LEFT JOIN vote_types vt ON p.vote_type_id = vt.id 
        ORDER BY p.id DESC
    """)
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "vote_type": row["vote_type"],
            "vote_count": row["vote_count"],
            "status": row["status"],
            "voting_open": bool(row["voting_open"]),
            "created_at": row["created_at"]
        }
        for row in rows
    ]

@app.post("/proposals", response_model=ProposalResponse)
def create_proposal(proposal: ProposalCreate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get vote_type_id
    c.execute("SELECT id FROM vote_types WHERE name = ?", (proposal.vote_type,))
    vt = c.fetchone()
    vote_type_id = vt[0] if vt else 1
    
    c.execute(
        "INSERT INTO proposals (title, description, vote_type_id) VALUES (?, ?, ?)",
        (proposal.title, proposal.description, vote_type_id)
    )
    proposal_id = c.lastrowid
    
    # Add voters
    for voter in (proposal.voters or []):
        c.execute(
            "INSERT OR IGNORE INTO proposal_voters (proposal_id, voter_address) VALUES (?, ?)",
            (proposal_id, voter)
        )
    
    conn.commit()
    conn.close()
    
    return {
        "id": proposal_id,
        "title": proposal.title,
        "description": proposal.description,
        "vote_type": proposal.vote_type,
        "vote_count": 0,
        "status": "pending",
        "voting_open": False,
        "created_at": datetime.now().isoformat()
    }

@app.get("/proposals/{proposal_id}", response_model=ProposalResponse)
def get_proposal(proposal_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT p.*, vt.name as vote_type 
        FROM proposals p 
        LEFT JOIN vote_types vt ON p.vote_type_id = vt.id 
        WHERE p.id = ?
    """, (proposal_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "vote_type": row["vote_type"],
        "vote_count": row["vote_count"],
        "status": row["status"],
        "voting_open": bool(row["voting_open"]),
        "created_at": row["created_at"]
    }

@app.post("/proposals/{proposal_id}/start")
def start_voting(proposal_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT voting_open, status FROM proposals WHERE id = ?", (proposal_id,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if row[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Voting already open")
    
    c.execute("UPDATE proposals SET voting_open = TRUE WHERE id = ?", (proposal_id,))
    conn.commit()
    conn.close()
    
    return {"status": "voting_open", "proposal_id": proposal_id}

@app.post("/proposals/{proposal_id}/vote")
def vote_proposal(proposal_id: int, vote: VoteRequest):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check proposal
    c.execute("SELECT voting_open, status FROM proposals WHERE id = ?", (proposal_id,))
    prop = c.fetchone()
    
    if not prop:
        conn.close()
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if not prop[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Voting not open")
    
    # Check voter is allowed
    c.execute(
        "SELECT has_voted FROM proposal_voters WHERE proposal_id = ? AND voter_address = ?",
        (proposal_id, vote.voter_address)
    )
    voter = c.fetchone()
    
    if not voter or voter[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Cannot vote")
    
    # Record vote
    c.execute(
        "INSERT INTO votes (proposal_id, voter_address, vote) VALUES (?, ?, ?)",
        (proposal_id, vote.voter_address, True)
    )
    c.execute("UPDATE proposal_voters SET has_voted = TRUE WHERE proposal_id = ? AND voter_address = ?",
              (proposal_id, vote.voter_address))
    c.execute("UPDATE proposals SET vote_count = vote_count + 1 WHERE id = ?", (proposal_id,))
    
    conn.commit()
    conn.close()
    
    return {"status": "voted", "proposal_id": proposal_id, "voter": vote.voter_address}

# === VOTES ===

@app.get("/proposals/{proposal_id}/votes", response_model=List[VoteResponse])
def get_proposal_votes(proposal_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM votes WHERE proposal_id = ?", (proposal_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/votes/{vote_id}", response_model=VoteResponse)
def get_vote(vote_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM votes WHERE id = ?", (vote_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Vote not found")
    return dict(row)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
