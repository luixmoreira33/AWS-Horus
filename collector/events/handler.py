"""
Handler de eventos EventBridge para atualização incremental.
Processa CloudTrail / Config events e atualiza apenas o recurso afetado.
"""
import json
import boto3
from collector.collector import HorusCollector, Edge
from collector.graph.writer import get_writer
from collector.extractors.network import SecurityGroupExtractor
from collector.extractors.compute_data import EC2Extractor, RDSExtractor, S3Extractor
from collector.extractors.dedicated import LambdaExtractor
from collector.extractors.integration import ELBExtractor, CloudFrontExtractor, APIGatewayExtractor, EKSExtractor
from collector.extractors.remaining_services import MWAAExtractor, GlueExtractor, DMSExtractor, MQExtractor, WAFExtractor, EFSExtractor
from collector.extractors.priority_services import OpenSearchExtractor

def process_event(event: dict, external_id: str, mode: str = "lite", dsn: str = None):
    detail = event.get("detail", {})
    account = detail.get("account") or event.get("account")
    region = detail.get("region") or event.get("region")
    event_name = detail.get("eventName", "")

    if not account:
        return {"skipped": True}

    collector = HorusCollector(external_id=external_id)
    for ext in [
        SecurityGroupExtractor(), EC2Extractor(), RDSExtractor(), S3Extractor(),
        LambdaExtractor(), ELBExtractor(), CloudFrontExtractor(),
        APIGatewayExtractor(), EKSExtractor(), OpenSearchExtractor(),
        MWAAExtractor(), GlueExtractor(), DMSExtractor(), MQExtractor(),
        WAFExtractor(), EFSExtractor(),
    ]:
        collector.register_extractor(ext)

    # Coleta apenas a região/conta afetada
    result = collector.collect_account_region(account, region or "us-east-1")
    writer = get_writer(mode=mode, dsn=dsn)
    writer.upsert_resources(result.get("resources", []))
    writer.upsert_edges(result.get("edges", []))

    return {
        "account": account,
        "region": region,
        "event": event_name,
        "resources": len(result.get("resources", [])),
        "edges": len(result.get("edges", []))
    }
