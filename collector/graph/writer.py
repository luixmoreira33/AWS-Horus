"""
Abstracao do writer de grafo. Suporta Lite (Postgres) e Enterprise (Neptune).
"""
from abc import ABC, abstractmethod
from typing import List, Dict
from collector.collector import Edge

class GraphWriter(ABC):
    @abstractmethod
    def upsert_resources(self, resources: List[Dict]) -> None: ...

    @abstractmethod
    def upsert_edges(self, edges: List[Edge]) -> None: ...

class NoopWriter(GraphWriter):
    """Usado em testes e dry-run."""
    def upsert_resources(self, resources: List[Dict]) -> None:
        pass

    def upsert_edges(self, edges: List[Edge]) -> None:
        pass

class PostgresWriter(GraphWriter):
    def __init__(self, dsn: str):
        self.dsn = dsn
        # Em producao: psycopg + schema de nodes/edges

    def upsert_resources(self, resources: List[Dict]) -> None:
        # INSERT ... ON CONFLICT (arn) DO UPDATE
        pass

    def upsert_edges(self, edges: List[Edge]) -> None:
        pass

class NeptuneWriter(GraphWriter):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def upsert_resources(self, resources: List[Dict]) -> None:
        # openCypher MERGE
        pass

    def upsert_edges(self, edges: List[Edge]) -> None:
        pass

def get_writer(mode: str = "lite", **kwargs) -> GraphWriter:
    if mode == "enterprise":
        return NeptuneWriter(kwargs.get("endpoint", ""))
    if mode == "lite":
        return PostgresWriter(kwargs.get("dsn", ""))
    return NoopWriter()
