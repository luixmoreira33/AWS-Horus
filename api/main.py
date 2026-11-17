from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from collector.graph.queries import LiteQueries

app = FastAPI(title="AWS-Horus API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

dsn = os.getenv("DATABASE_URL", "postgresql://localhost/horus")
queries = LiteQueries(dsn)

class PathRequest(BaseModel):
    from_arn: str
    to_arn: str
    max_depth: int = 6

@app.get("/health")
def health():
    return {"status": "ok", "mode": "lite"}

@app.get("/resources/{arn:path}/neighbors")
def neighbors(arn: str, depth: int = 1):
    return queries.neighbors(arn, depth)

@app.post("/path")
def path(req: PathRequest):
    result = queries.path(req.from_arn, req.to_arn, req.max_depth)
    if not result.get("found"):
        raise HTTPException(404, "No path found")
    return result

@app.get("/exposure")
def exposure(account: Optional[str] = None):
    return queries.exposure(account)

@app.get("/search")
def search(q: str = Query(..., min_length=2)):
    # Em produção: SELECT arn, type FROM resources WHERE arn ILIKE %s OR type ILIKE %s LIMIT 50
    return {"query": q, "results": []}
