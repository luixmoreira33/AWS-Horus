"""
Orquestra a coleta e grava no grafo (modo Lite ou Enterprise).
"""
import os
from collector.collector import HorusCollector
from collector.graph.writer import get_writer
from collector.extractors.network import SecurityGroupExtractor, VPCExtractor
from collector.extractors.compute_data import EC2Extractor, RDSExtractor, S3Extractor
from collector.extractors.dedicated import LambdaExtractor
from collector.extractors.integration import ELBExtractor, CloudFrontExtractor, APIGatewayExtractor, EKSExtractor

def run_full_scan(external_id: str, mode: str = "lite", dsn: str = None):
    collector = HorusCollector(external_id=external_id)

    for ext in [
        SecurityGroupExtractor(), VPCExtractor(),
        EC2Extractor(), RDSExtractor(), S3Extractor(), LambdaExtractor(),
        ELBExtractor(), CloudFrontExtractor(), APIGatewayExtractor(), EKSExtractor(),
    ]:
        collector.register_extractor(ext)

    result = collector.full_scan()

    writer = get_writer(mode=mode, dsn=dsn or os.getenv("DATABASE_URL", ""))
    all_resources = []
    all_edges = []
    for r in result.get("results", []):
        all_resources.extend(r.get("resources", []))
        all_edges.extend(r.get("edges", []))

    writer.upsert_resources(all_resources)
    writer.upsert_edges(all_edges)

    return {
        "resources": len(all_resources),
        "edges": len(all_edges),
        "failures": result.get("failures", [])
    }
