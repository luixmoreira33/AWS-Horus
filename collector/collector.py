"""
AWS-Horus Collector - Inventário universal multi-conta e relações genéricas.
Somente leitura. Modelo de aresta universal.
"""
import boto3
import json
import logging
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("atlas.collector")

@dataclass
class Edge:
    source_arn: str
    target_arn: str
    direction: str = "out"
    category: str = "IAM/AUTORIZAÇÃO"  # REDE | EVENTO/INTEGRAÇÃO | ...
    mechanism: str = "generic-arn-reference"
    ports: Optional[List[int]] = None
    protocol: Optional[str] = None
    evidence: Dict = None
    evidence_level: str = "DECLARADA"  # DECLARADA | PERMITIDA | OBSERVADA
    risk: str = "none"
    first_seen: str = None
    last_seen: str = None

    def __post_init__(self):
        now = datetime.utcnow().isoformat()
        if not self.first_seen:
            self.first_seen = now
        if not self.last_seen:
            self.last_seen = now
        if self.evidence is None:
            self.evidence = {}

class AtlasCollector:
    def __init__(self, central_role_arn: str = None, external_id: str = None):
        self.external_id = external_id
        self.session = boto3.Session()
        self.failures: List[Dict] = []

    def assume_role(self, account_id: str, region: str = "us-east-1") -> boto3.Session:
        """Assume AtlasReadOnly in member account."""
        sts = self.session.client("sts")
        role_arn = f"arn:aws:iam::{account_id}:role/AtlasReadOnly"
        creds = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName="AtlasCollector",
            ExternalId=self.external_id,
            DurationSeconds=3600,
        )["Credentials"]
        return boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
            region_name=region,
        )

    def list_accounts(self) -> List[Dict]:
        org = self.session.client("organizations")
        paginator = org.get_paginator("list_accounts")
        accounts = []
        for page in paginator.paginate():
            accounts.extend(page["Accounts"])
        return [a for a in accounts if a["Status"] == "ACTIVE"]

    def inventory_resource_explorer(self, session: boto3.Session, account_id: str, region: str) -> List[Dict]:
        """Camada 2: Resource Explorer search (quando índice existe)."""
        try:
            re = session.client("resource-explorer-2", region_name=region)
            paginator = re.get_paginator("search")
            resources = []
            for page in paginator.paginate(QueryString="*", MaxResults=1000):
                resources.extend(page.get("Resources", []))
            return [{"arn": r["Arn"], "type": r.get("ResourceType"), "account": account_id, "region": region, "properties": r} for r in resources]
        except Exception as e:
            self.failures.append({"account": account_id, "region": region, "source": "resource-explorer", "error": str(e)})
            return []

    def generic_relations_from_config(self, resource: Dict) -> List[Edge]:
        """Relações genéricas: ARN/ID references, ENI, SG, role, KMS, etc."""
        edges = []
        # Expand with real parsing of Role, KMS, SG, Subnet, VPC, ENI RequesterId, etc.
        return edges

    def collect_account_region(self, account_id: str, region: str) -> Dict:
        try:
            session = self.assume_role(account_id, region)
            resources = self.inventory_resource_explorer(session, account_id, region)
            edges = []
            for r in resources:
                edges.extend(self.generic_relations_from_config(r))
            return {"account": account_id, "region": region, "resources": resources, "edges": [asdict(e) for e in edges]}
        except Exception as e:
            self.failures.append({"account": account_id, "region": region, "error": str(e)})
            return {"account": account_id, "region": region, "resources": [], "edges": [], "error": str(e)}

    def full_scan(self, max_workers: int = 10) -> Dict:
        accounts = self.list_accounts()
        regions = ["us-east-1", "sa-east-1", "eu-west-1"]  # expand dynamically
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {
                ex.submit(self.collect_account_region, a["Id"], r): (a["Id"], r)
                for a in accounts for r in regions
            }
            for fut in as_completed(futures):
                results.append(fut.result())
        return {"results": results, "failures": self.failures}

class BaseExtractor:
    resource_types: List[str] = []
    edge_types: List[str] = []

    def discover(self, session, account, region) -> List[Dict]:
        raise NotImplementedError

    def relations(self, resource: Dict) -> List[Edge]:
        raise NotImplementedError

    def health(self) -> Dict:
        return {"status": "ok"}

class LambdaExtractor(BaseExtractor):
    resource_types = ["AWS::Lambda::Function"]
    edge_types = ["iam-role", "vpc-eni", "event-source", "kms"]

    def relations(self, resource: Dict) -> List[Edge]:
        edges = []
        role = resource.get("properties", {}).get("Role")
        if role:
            edges.append(Edge(
                source_arn=resource["arn"],
                target_arn=role,
                category="IAM/AUTORIZAÇÃO",
                mechanism="iam-role-attachment",
                evidence={"role": role},
                evidence_level="DECLARADA"
            ))
        return edges

if __name__ == "__main__":
    print("AWS-Horus Collector skeleton ready. Configure ExternalId and run full_scan().")
