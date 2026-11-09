"""
AWS-Horus Collector - Inventário universal multi-conta e relações.
Somente leitura. Modelo de aresta universal + extratores dedicados.
"""
import boto3
import json
import logging
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("horus.collector")

@dataclass
class Edge:
    source_arn: str
    target_arn: str
    direction: str = "out"
    category: str = "IAM/AUTORIZAÇÃO"
    mechanism: str = "generic-arn-reference"
    ports: Optional[List[int]] = None
    protocol: Optional[str] = None
    evidence: Dict = field(default_factory=dict)
    evidence_level: str = "DECLARADA"
    risk: str = "none"
    first_seen: str = None
    last_seen: str = None

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()
        if not self.first_seen:
            self.first_seen = now
        if not self.last_seen:
            self.last_seen = now

class BaseExtractor:
    resource_types: List[str] = []
    edge_types: List[str] = []

    def discover(self, session: boto3.Session, account: str, region: str) -> List[Dict]:
        raise NotImplementedError

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        raise NotImplementedError

    def health(self) -> Dict:
        return {"status": "ok", "types": self.resource_types}

class HorusCollector:
    def __init__(self, external_id: str, central_account_id: str = None):
        self.external_id = external_id
        self.session = boto3.Session()
        self.failures: List[Dict] = []
        self.extractors: List[BaseExtractor] = []

    def register_extractor(self, extractor: BaseExtractor):
        self.extractors.append(extractor)

    def assume_role(self, account_id: str, region: str = "us-east-1") -> boto3.Session:
        sts = self.session.client("sts")
        role_arn = f"arn:aws:iam::{account_id}:role/AtlasReadOnly"
        for attempt in range(3):
            try:
                creds = sts.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName=f"HorusCollector-{int(time.time())}",
                    ExternalId=self.external_id,
                    DurationSeconds=3600,
                )["Credentials"]
                return boto3.Session(
                    aws_access_key_id=creds["AccessKeyId"],
                    aws_secret_access_key=creds["SecretAccessKey"],
                    aws_session_token=creds["SessionToken"],
                    region_name=region,
                )
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep((2 ** attempt) + random.random())
        raise RuntimeError("AssumeRole failed")

    def list_accounts(self) -> List[Dict]:
        org = self.session.client("organizations")
        paginator = org.get_paginator("list_accounts")
        accounts = []
        for page in paginator.paginate():
            accounts.extend(page["Accounts"])
        return [a for a in accounts if a["Status"] == "ACTIVE"]

    def list_regions(self, session: boto3.Session) -> List[str]:
        try:
            ec2 = session.client("ec2", region_name="us-east-1")
            resp = ec2.describe_regions(AllRegions=False)
            return [r["RegionName"] for r in resp["Regions"]]
        except Exception:
            return ["us-east-1", "sa-east-1", "eu-west-1", "us-west-2"]

    def inventory_resource_explorer(self, session: boto3.Session, account_id: str, region: str) -> List[Dict]:
        try:
            re = session.client("resource-explorer-2", region_name=region)
            paginator = re.get_paginator("search")
            resources = []
            for page in paginator.paginate(QueryString="*", MaxResults=1000):
                resources.extend(page.get("Resources", []))
            return [{
                "arn": r["Arn"],
                "type": r.get("ResourceType"),
                "account": account_id,
                "region": region,
                "properties": r
            } for r in resources]
        except Exception as e:
            self.failures.append({"account": account_id, "region": region, "source": "resource-explorer", "error": str(e)})
            return []

    def generic_relations(self, resource: Dict) -> List[Edge]:
        edges = []
        # ARN/ID references, ENI, SG, role, KMS, resource-policy, tags
        # Expandido em produção com parsing real
        return edges

    def collect_account_region(self, account_id: str, region: str) -> Dict:
        try:
            session = self.assume_role(account_id, region)
            resources = self.inventory_resource_explorer(session, account_id, region)
            edges = []
            for r in resources:
                edges.extend(self.generic_relations(r))
                for ext in self.extractors:
                    if r.get("type") in ext.resource_types:
                        edges.extend(ext.relations(r, session))
            return {
                "account": account_id,
                "region": region,
                "resources": resources,
                "edges": [asdict(e) for e in edges]
            }
        except Exception as e:
            self.failures.append({"account": account_id, "region": region, "error": str(e)})
            return {"account": account_id, "region": region, "resources": [], "edges": [], "error": str(e)}

    def full_scan(self, max_workers: int = 8) -> Dict:
        accounts = self.list_accounts()
        sample_session = self.assume_role(accounts[0]["Id"]) if accounts else self.session
        regions = self.list_regions(sample_session)
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {
                ex.submit(self.collect_account_region, a["Id"], r): (a["Id"], r)
                for a in accounts for r in regions
            }
            for fut in as_completed(futures):
                results.append(fut.result())
        return {"results": results, "failures": self.failures, "timestamp": datetime.now(timezone.utc).isoformat()}

if __name__ == "__main__":
    print("AWS-Horus Collector ready. Configure ExternalId and register extractors.")
