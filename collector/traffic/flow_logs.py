"""
Ingestão de VPC Flow Logs para marcar arestas como OBSERVADA.
Lê logs do CloudWatch Logs ou S3 e atualiza evidence_level.
"""
from typing import List, Dict
from collector.collector import Edge
from datetime import datetime, timezone

def parse_flow_log_line(line: str) -> Dict:
    # Formato padrão VPC Flow Log (v5)
    parts = line.split()
    if len(parts) < 14:
        return {}
    return {
        "srcaddr": parts[3],
        "dstaddr": parts[4],
        "srcport": int(parts[5]) if parts[5].isdigit() else None,
        "dstport": int(parts[6]) if parts[6].isdigit() else None,
        "protocol": parts[7],
        "action": parts[12],
    }

def flow_to_edges(logs: List[str], resource_map: Dict[str, str]) -> List[Edge]:
    """
    resource_map: IP/ENI → ARN do recurso.
    Gera arestas OBSERVADA quando há tráfego real.
    """
    edges = []
    seen = set()
    for line in logs:
        flow = parse_flow_log_line(line)
        if not flow or flow.get("action") != "ACCEPT":
            continue
        src = resource_map.get(flow["srcaddr"])
        dst = resource_map.get(flow["dstaddr"])
        if not src or not dst or src == dst:
            continue
        key = (src, dst, flow["dstport"])
        if key in seen:
            continue
        seen.add(key)
        edges.append(Edge(
            source_arn=src,
            target_arn=dst,
            category="REDE",
            mechanism="vpc-flow-log",
            ports=[flow["dstport"]] if flow["dstport"] else None,
            protocol=flow["protocol"],
            evidence={"flow": flow, "observed_at": datetime.now(timezone.utc).isoformat()},
            evidence_level="OBSERVADA"
        ))
    return edges
