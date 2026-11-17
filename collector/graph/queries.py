"""
Queries para modo Lite (PostgreSQL).
Vizinhos, caminho A→B e exposição básica.
"""
from typing import List, Dict, Optional

class LiteQueries:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def neighbors(self, arn: str, depth: int = 1) -> Dict:
        """
        Retorna inbound e outbound de um ARN.
        Em produção: executar via psycopg.
        """
        # SELECT * FROM edges WHERE source_arn = %s OR target_arn = %s
        return {
            "arn": arn,
            "inbound": [],
            "outbound": [],
            "depth": depth
        }

    def path(self, from_arn: str, to_arn: str, max_depth: int = 6) -> Dict:
        """
        Caminho simples A → B usando recursive CTE (Postgres).
        """
        # WITH RECURSIVE path AS (
        #   SELECT source_arn, target_arn, 1 AS depth, ARRAY[source_arn] AS visited
        #   FROM edges WHERE source_arn = %s
        #   UNION ALL
        #   SELECT e.source_arn, e.target_arn, p.depth + 1, p.visited || e.source_arn
        #   FROM edges e JOIN path p ON e.source_arn = p.target_arn
        #   WHERE p.depth < %s AND NOT e.target_arn = ANY(p.visited)
        # )
        # SELECT * FROM path WHERE target_arn = %s LIMIT 1;
        return {
            "from": from_arn,
            "to": to_arn,
            "path": [],
            "found": False
        }

    def exposure(self, account: Optional[str] = None) -> List[Dict]:
        """
        Recursos com SG aberto para 0.0.0.0/0 ou buckets públicos.
        """
        # SELECT DISTINCT source_arn FROM edges
        # WHERE mechanism = 'security-group-rule' AND evidence->>'cidr' = '0.0.0.0/0'
        return []
