from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class TemplateExtractor(BaseExtractor):
    """
    Template para novo extrator.
    Copie este arquivo, renomeie a classe e implemente discover() e relations().
    Registrar no collector principal não exige alterar motor, schema nem UI.
    """
    resource_types = ["AWS::Service::ResourceType"]
    edge_types = ["example-relation"]

    def discover(self, session: boto3.Session, account: str, region: str) -> List[Dict]:
        return []

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        # Implement specific relations here
        return edges
