from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class EC2Extractor(BaseExtractor):
    resource_types = ["AWS::EC2::Instance"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        # ENIs, SGs, subnet, IAM instance profile
        for eni in props.get("NetworkInterfaces", []):
            for sg in eni.get("Groups", []):
                edges.append(Edge(
                    source_arn=arn,
                    target_arn=sg.get("GroupId", ""),
                    category="REDE",
                    mechanism="eni-security-group",
                    evidence={"eni": eni.get("NetworkInterfaceId")},
                    evidence_level="DECLARADA"
                ))
        return edges

class RDSExtractor(BaseExtractor):
    resource_types = ["AWS::RDS::DBInstance", "AWS::RDS::DBCluster"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        for sg in props.get("VpcSecurityGroups", []):
            edges.append(Edge(
                source_arn=arn,
                target_arn=sg.get("VpcSecurityGroupId", ""),
                category="REDE",
                mechanism="rds-security-group",
                evidence={"status": sg.get("Status")},
                evidence_level="DECLARADA"
            ))
        kms = props.get("KmsKeyId")
        if kms:
            edges.append(Edge(
                source_arn=arn,
                target_arn=kms,
                category="CRIPTOGRAFIA",
                mechanism="kms-encryption",
                evidence={"field": "KmsKeyId"},
                evidence_level="DECLARADA"
            ))
        return edges

class S3Extractor(BaseExtractor):
    resource_types = ["AWS::S3::Bucket"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        if not session:
            return edges
        arn = resource["arn"]
        bucket = arn.split(":::")[-1] if ":::" in arn else arn.split("/")[-1]
        try:
            s3 = session.client("s3")
            # GetBucketEncryption (metadata only)
            enc = s3.get_bucket_encryption(Bucket=bucket)
            for rule in enc.get("ServerSideEncryptionConfiguration", {}).get("Rules", []):
                kms = rule.get("ApplyServerSideEncryptionByDefault", {}).get("KMSMasterKeyID")
                if kms:
                    edges.append(Edge(
                        source_arn=arn,
                        target_arn=kms,
                        category="CRIPTOGRAFIA",
                        mechanism="s3-kms",
                        evidence={"source": "GetBucketEncryption"},
                        evidence_level="DECLARADA"
                    ))
        except Exception:
            pass
        # GetBucketPolicy (metadata) pode ser adicionado aqui
        return edges
