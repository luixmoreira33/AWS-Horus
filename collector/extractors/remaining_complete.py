from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class Route53Extractor(BaseExtractor):
    resource_types = ["AWS::Route53::HostedZone", "AWS::Route53::RecordSet"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        # Record → Alias target (ALB, CloudFront, S3)
        alias = props.get("AliasTarget") or props.get("aliasTarget")
        if alias and alias.get("DNSName"):
            edges.append(Edge(
                source_arn=arn,
                target_arn=f"arn:aws:route53:::alias/{alias['DNSName']}",
                category="REDE",
                mechanism="route53-alias",
                evidence={"dns_name": alias["DNSName"]},
                evidence_level="DECLARADA"
            ))
        return edges

class ACMExtractor(BaseExtractor):
    resource_types = ["AWS::ACM::Certificate"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        # Certificado é alvo de CloudFront, ALB, API Gateway (já coberto nos outros extratores)
        return []

class ECRExtractor(BaseExtractor):
    resource_types = ["AWS::ECR::Repository"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        # Lifecycle / encryption
        kms = props.get("encryptionConfiguration", {}).get("kmsKey")
        if kms:
            edges.append(Edge(
                source_arn=arn,
                target_arn=kms,
                category="CRIPTOGRAFIA",
                mechanism="ecr-kms",
                evidence_level="DECLARADA"
            ))
        return edges

class BackupExtractor(BaseExtractor):
    resource_types = ["AWS::Backup::BackupVault", "AWS::Backup::BackupPlan"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        # Vault → recursos protegidos (via seleção)
        for selection in props.get("BackupSelections", []):
            for resource_arn in selection.get("Resources", []):
                edges.append(Edge(
                    source_arn=arn,
                    target_arn=resource_arn,
                    category="DADOS",
                    mechanism="backup-selection",
                    evidence_level="DECLARADA"
                ))
        return edges

class ConfigExtractor(BaseExtractor):
    resource_types = ["AWS::Config::ConfigRule", "AWS::Config::ConfigurationRecorder"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        return []  # Config é fonte de inventário, não gera aresta direta

class MQExtractor(BaseExtractor):
    resource_types = ["AWS::AmazonMQ::Broker"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        for sg in props.get("SecurityGroups", []):
            edges.append(Edge(
                source_arn=arn,
                target_arn=sg,
                category="REDE",
                mechanism="mq-security-group",
                evidence_level="DECLARADA"
            ))
        return edges
