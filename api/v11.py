from fastapi import APIRouter
from collector.graph.neptune_writer import NeptuneWriter
from collector.graph.queries import LiteQueries
import os

router = APIRouter(prefix="/v1.1")

@router.get("/blast-radius/{arn:path}")
def blast_radius(arn: str, depth: int = 3):
    mode = os.getenv("DEPLOY_MODE", "lite")
    if mode == "enterprise":
        writer = NeptuneWriter(os.getenv("NEPTUNE_ENDPOINT", ""))
        return writer.blast_radius(arn, depth)
    # Lite fallback
    return {"arn": arn, "affected": [], "note": "Use Enterprise mode for full blast radius"}

@router.get("/diff")
def diff(since: str = "yesterday"):
    # Compara snapshot atual vs anterior
    return {
        "since": since,
        "added": [],
        "removed": [],
        "changed": []
    }

@router.get("/health/metrics")
def metrics():
    return {
        "collector": {"last_run": None, "failures": 0, "resources": 0},
        "graph": {"nodes": 0, "edges": 0},
        "mode": os.getenv("DEPLOY_MODE", "lite")
    }
