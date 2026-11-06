"""
AWS-Horus API - FastAPI skeleton
Endpoints: inventory, neighbors, path query, coverage matrix
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AWS-Horus", version="0.1.0")

class NeighborQuery(BaseModel):
    arn: str
    depth: int = 1
    categories: Optional[List[str]] = None
    evidence_levels: Optional[List[str]] = None

@app.get("/health")
def health():
    return {"status": "ok", "graph": "neptune"}

@app.get("/accounts")
def list_accounts():
    return {"accounts": []}

@app.get("/resources")
def list_resources(account: Optional[str] = None, region: Optional[str] = None, type: Optional[str] = None):
    return {"resources": []}

@app.post("/neighbors")
def get_neighbors(q: NeighborQuery):
    """Return all in/out neighbors with full edge model."""
    return {
        "arn": q.arn,
        "inbound": [],
        "outbound": [],
        "coverage": "DEDICADO|GENÉRICO|SEM COBERTURA"
    }

@app.get("/path")
def path(from_arn: str, to_arn: str):
    """Como A chega em B? Caminho completo (SG, rota, policy...)."""
    return {"path": [], "evidence_levels": []}

@app.get("/coverage")
def coverage_matrix():
    return {"types": [], "gaps": []}

@app.get("/changes")
def changes(since: str = "1h"):
    return {"diffs": []}
