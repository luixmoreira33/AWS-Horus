from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class SecurityGroupExtractor(BaseExtractor):
    resource_types = ["AWS::EC2::SecurityGroup"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        # Regras de entrada/saida com referencias a outros SGs ou CIDRs
        for rule in props.get("IpPermissions", []):
            for pair in rule.get("UserIdGroupPairs", []):
                target = pair.get("GroupId")
                if target:
                    edges.append(Edge(
                        source_arn=arn,
                        target_arn=f"arn:aws:ec2:{resource.get('region')}:{resource.get('account')}:security-group/{target}",
                        category="REDE",
                        mechanism="security-group-rule",
                        ports=[rule.get("FromPort")] if rule.get("FromPort") else None,
                        protocol=rule.get("IpProtocol"),
                        evidence={"direction": "ingress", "group_id": target},
                        evidence_level="PERMITIDA"
                    ))
        return edges

class VPCExtractor(BaseExtractor):
    resource_types = ["AWS::EC2::VPC", "AWS::EC2::Subnet", "AWS::EC2::RouteTable"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        # Peering, TGW, endpoints, rotas para IGW/NAT
        return edges
