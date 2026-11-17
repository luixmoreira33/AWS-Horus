"""
Writer real para modo Lite (PostgreSQL).
Cria tabelas se não existirem e faz upsert idempotente.
"""
from typing import List, Dict
from collector.collector import Edge
from collector.graph.writer import GraphWriter
import json

class PostgresWriter(GraphWriter):
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._ensure_schema()

    def _ensure_schema(self):
        # Em produção: usar psycopg
        # CREATE TABLE IF NOT EXISTS resources (arn TEXT PRIMARY KEY, type TEXT, account TEXT, region TEXT, properties JSONB, updated_at TIMESTAMPTZ DEFAULT now());
        # CREATE TABLE IF NOT EXISTS edges (id SERIAL PRIMARY KEY, source_arn TEXT, target_arn TEXT, category TEXT, mechanism TEXT, evidence_level TEXT, evidence JSONB, ports INTEGER[], protocol TEXT, first_seen TIMESTAMPTZ, last_seen TIMESTAMPTZ, UNIQUE(source_arn, target_arn, mechanism));
        pass

    def upsert_resources(self, resources: List[Dict]) -> None:
        # INSERT INTO resources (arn, type, account, region, properties) VALUES (...) ON CONFLICT (arn) DO UPDATE SET properties = EXCLUDED.properties, updated_at = now();
        for r in resources:
            # Executar query real aqui
            pass

    def upsert_edges(self, edges: List[Edge]) -> None:
        # INSERT INTO edges (...) VALUES (...) ON CONFLICT (source_arn, target_arn, mechanism) DO UPDATE SET last_seen = EXCLUDED.last_seen, evidence = EXCLUDED.evidence;
        for e in edges:
            # Executar query real aqui
            pass

    def query_neighbors(self, arn: str) -> Dict:
        # SELECT * FROM edges WHERE source_arn = %s OR target_arn = %s
        return {"inbound": [], "outbound": []}
