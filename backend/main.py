"""
Verivo Backend - FastAPI + SQLite
With authentication
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
import sqlite3
from datetime import datetime, timedelta
import hashlib
import secrets
from functools import wraps

app = FastAPI(title="Verivo API", description="Système de vote DAO")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "verivo.db"

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

# === DATABASE ===

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'voter',
            wallet_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Sessions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Vote types
    c.execute("""
        CREATE TABLE IF NOT EXISTS vote_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            required_percentage INTEGER DEFAULT 50
        )
    """)
    
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
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vote_type_id) REFERENCES vote_types(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)
    
    # Proposal voters
    c.execute("""
        CREATE TABLE IF NOT EXISTS proposal_voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            voter_id INTEGER NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id),
            FOREIGN KEY (voter_id) REFERENCES users(id),
            UNIQUE(proposal_id, voter_id)
        )
    """)
    
    # Votes
    c.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            voter_id INTEGER NOT NULL,
            vote BOOLEAN NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id),
            FOREIGN KEY (voter_id) REFERENCES users(id),
            UNIQUE(proposal_id, voter_id)
        )
    """)
    
    conn.commit()
    conn.close()

# === MODELS ===

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    wallet_address: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    role: str
    wallet_address: Optional[str]
    created_at: str

class TokenResponse(BaseModel):
    token: str
    user: UserResponse

class VoteTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    required_percentage: int

class ProposalCreate(BaseModel):
    title: str
    description: str
    vote_type: VoteTypeEnum = VoteTypeEnum.SIMPLE_MAJORITY

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
    vote: bool

# === AUTH HELPERS ===

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token() -> str:
    return secrets.token_urlsafe(32)

def get_user_from_token(token: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT u.* FROM users u
        JOIN sessions s ON u.id = s.user_id
        WHERE s.token = ? AND s.expires_at > datetime('now')
    """, (token,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def require_auth(token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Non connecté")
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Session expirée")
    return user

# === ROUTES ===

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# === AUTH ===

@app.post("/api/register", response_model=TokenResponse)
def register(user: UserCreate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if email exists
    c.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    # Create user
    c.execute("""
        INSERT INTO users (email, password_hash, name, wallet_address)
        VALUES (?, ?, ?, ?)
    """, (user.email, hash_password(user.password), user.name, user.wallet_address))
    
    user_id = c.lastrowid
    
    # Create session
    token = generate_token()
    expires = datetime.now() + timedelta(days=7)
    c.execute("INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)",
              (user_id, token, expires))
    
    conn.commit()
    
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    c.row_factory = sqlite3.Row
    row = c.fetchone()
    conn.close()
    
    user_data = {"id": row["id"], "email": row["email"], "name": row["name"], "role": row["role"], "wallet_address": row["wallet_address"], "created_at": row["created_at"]}
    return {
        "token": token,
        "user": {
            "id": user_data["id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "role": user_data["role"],
            "wallet_address": user_data["wallet_address"],
            "created_at": user_data["created_at"]
        }
    }

@app.post("/api/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE email = ?", (credentials.email,))
    user = c.fetchone()
    
    if not user or user["password_hash"] != hash_password(credentials.password):
        conn.close()
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    user_id = user["id"]
    
    # Create session
    token = generate_token()
    expires = datetime.now() + timedelta(days=7)
    c.execute("INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)",
              (user_id, token, expires))
    
    conn.commit()
    conn.close()
    
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "wallet_address": user["wallet_address"],
            "created_at": user["created_at"]
        }
    }

@app.post("/api/logout")
def logout(token: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return {"status": "logged_out"}

@app.get("/api/me", response_model=UserResponse)
def get_me(authorization: str = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Non connecté")
    
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Session invalide")
    
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
        "wallet_address": user["wallet_address"],
        "created_at": user["created_at"]
    }

# === VOTE TYPES ===

@app.get("/api/vote-types", response_model=List[VoteTypeResponse])
def get_vote_types():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM vote_types")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# === PROPOSALS ===

@app.get("/api/proposals", response_model=List[ProposalResponse])
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

@app.post("/api/proposals", response_model=ProposalResponse)
def create_proposal(proposal: ProposalCreate, authorization: str = None):
    user = require_auth(authorization)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT id FROM vote_types WHERE name = ?", (proposal.vote_type,))
    vt = c.fetchone()
    vote_type_id = vt[0] if vt else 1
    
    c.execute("""
        INSERT INTO proposals (title, description, vote_type_id, created_by)
        VALUES (?, ?, ?, ?)
    """, (proposal.title, proposal.description, vote_type_id, user["id"]))
    
    proposal_id = c.lastrowid
    
    # Add creator as voter
    c.execute("""
        INSERT INTO proposal_voters (proposal_id, voter_id)
        VALUES (?, ?)
    """, (proposal_id, user["id"]))
    
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

@app.get("/api/proposals/{proposal_id}", response_model=ProposalResponse)
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

@app.post("/api/proposals/{proposal_id}/start")
def start_voting(proposal_id: int, authorization: str = None):
    user = require_auth(authorization)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT voting_open, status, created_by FROM proposals WHERE id = ?", (proposal_id,))
    prop = c.fetchone()
    
    if not prop:
        conn.close()
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if prop[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Voting already open")
    
    if user["role"] != "admin":
        conn.close()
        raise HTTPException(status_code=403, detail="Only admins can start voting")
    
    c.execute("UPDATE proposals SET voting_open = TRUE WHERE id = ?", (proposal_id,))
    conn.commit()
    conn.close()
    
    return {"status": "voting_open", "proposal_id": proposal_id}

@app.post("/api/proposals/{proposal_id}/vote")
def vote_proposal(proposal_id: int, vote: VoteRequest, authorization: str = None):
    user = require_auth(authorization)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT voting_open, status FROM proposals WHERE id = ?", (proposal_id,))
    prop = c.fetchone()
    
    if not prop:
        conn.close()
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    if not prop[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Voting not open")
    
    # Check if user is voter
    c.execute("""
        SELECT has_voted FROM proposal_voters 
        WHERE proposal_id = ? AND voter_id = ?
    """, (proposal_id, user["id"]))
    voter = c.fetchone()
    
    if not voter:
        conn.close()
        raise HTTPException(status_code=400, detail="Vous n'êtes pas autorisé à voter")
    
    if voter[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Déjà voted")
    
    # Record vote
    c.execute("""
        INSERT INTO votes (proposal_id, voter_id, vote) VALUES (?, ?, ?)
    """, (proposal_id, user["id"], vote.vote))
    
    c.execute("UPDATE proposal_voters SET has_voted = TRUE WHERE proposal_id = ? AND voter_id = ?",
              (proposal_id, user["id"]))
    
    c.execute("UPDATE proposals SET vote_count = vote_count + 1 WHERE id = ?", (proposal_id,))
    
    conn.commit()
    conn.close()
    
    return {"status": "voted", "proposal_id": proposal_id}

# === VOTES ===

@app.get("/api/proposals/{proposal_id}/votes")
def get_proposal_votes(proposal_id: int, authorization: str = None):
    user = require_auth(authorization)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT u.name, u.email, v.vote, v.voted_at
        FROM votes v
        JOIN users u ON v.voter_id = u.id
        WHERE v.proposal_id = ?
    """, (proposal_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
