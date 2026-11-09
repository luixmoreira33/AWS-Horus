"""
AWS-Horus API - FastAPI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="AWS-Horus", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NeighborQuery(BaseModel):
    arn: str
    depth: int = 1
    categories: Optional[List[str]] = None
    evidence_levels: Optional[List[str]] = None

class PathQuery(BaseModel):
    from_arn: str
    to_arn: str

@app.get("/health")
def health():
    return {"status": "ok", "graph": "neptune", "timestamp": datetime.utcnow().isoformat()}

@app.get("/accounts")
def list_accounts():
    return {"accounts": []}

@app.get("/resources")
def list_resources(
    account: Optional[str] = None,
    region: Optional[str] = None,
    type: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 100
):
    return {"resources": [], "count": 0}

@app.post("/neighbors")
def get_neighbors(q: NeighborQuery):
    """Todos os vizinhos de entrada e saída com modelo completo de aresta."""
    return {
        "arn": q.arn,
        "inbound": [],
        "outbound": [],
        "coverage": "DEDICADO",
        "last_updated": datetime.utcnow().isoformat()
    }

@app.post("/path")
def path(q: PathQuery):
    """Como A chega em B? Caminho completo (SG, rota, TGW, policy...)."""
    return {
        "from": q.from_arn,
        "to": q.to_arn,
        "path": [],
        "evidence_levels": [],
        "approximate": False
    }

@app.get("/coverage")
def coverage_matrix():
    return {
        "types": [],
        "gaps": [],
        "last_scan": None
    }

@app.get("/changes")
def changes(since: str = "1h", account: Optional[str] = None):
    return {"diffs": [], "since": since}

@app.get("/export/{format}")
def export(format: str, account: Optional[str] = None, vpc: Optional[str] = None):
    if format not in ["json", "mermaid", "svg"]:
        raise HTTPException(400, "format must be json|mermaid|svg")
    return {"format": format, "data": ""}
