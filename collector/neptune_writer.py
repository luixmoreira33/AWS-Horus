"""
Escrita de nós e arestas no Amazon Neptune (openCypher via bolt ou HTTP).
Use com IAM auth em produção.
"""
from typing import List, Dict
from collector.collector import Edge

class NeptuneWriter:
    def __init__(self, endpoint: str, port: int = 8182, use_iam: bool = True):
        self.endpoint = endpoint
        self.port = port
        # Em produção: use boto3 + signed requests ou neo4j driver com IAM

    def upsert_node(self, arn: str, properties: Dict):
        # MERGE (n:Resource {arn: $arn}) SET n += $props
        pass

    def upsert_edge(self, edge: Edge):
        # MATCH (a {arn: $src}), (b {arn: $dst})
        # MERGE (a)-[r:CONNECTED {mechanism: $mech}]->(b)
        # SET r += $props
        pass

    def bulk_write(self, resources: List[Dict], edges: List[Edge]):
        for r in resources:
            self.upsert_node(r["arn"], r)
        for e in edges:
            self.upsert_edge(e)
