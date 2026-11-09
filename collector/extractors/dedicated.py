from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class LambdaExtractor(BaseExtractor):
    resource_types = ["AWS::Lambda::Function"]
    edge_types = ["iam-role", "vpc-eni", "event-source", "kms", "log-group"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        conf = props.get("Configuration") or props

        role = conf.get("Role") or conf.get("RoleArn")
        if role:
            edges.append(Edge(
                source_arn=arn,
                target_arn=role,
                category="IAM/AUTORIZAÇÃO",
                mechanism="iam-role-attachment",
                evidence={"field": "Role"},
                evidence_level="DECLARADA"
            ))

        vpc = conf.get("VpcConfig") or {}
        for sg in vpc.get("SecurityGroupIds", []):
            edges.append(Edge(
                source_arn=arn,
                target_arn=f"arn:aws:ec2:{resource.get('region','us-east-1')}:{resource.get('account')}:security-group/{sg}",
                category="REDE",
                mechanism="security-group-attachment",
                evidence={"sg_id": sg},
                evidence_level="DECLARADA"
            ))
        for subnet in vpc.get("SubnetIds", []):
            edges.append(Edge(
                source_arn=arn,
                target_arn=f"arn:aws:ec2:{resource.get('region','us-east-1')}:{resource.get('account')}:subnet/{subnet}",
                category="REDE",
                mechanism="subnet-attachment",
                evidence={"subnet_id": subnet},
                evidence_level="DECLARADA"
            ))

        kms = conf.get("KMSKeyArn") or conf.get("KmsKeyArn")
        if kms:
            edges.append(Edge(
                source_arn=arn,
                target_arn=kms,
                category="CRIPTOGRAFIA",
                mechanism="kms-encryption",
                evidence={"field": "KMSKeyArn"},
                evidence_level="DECLARADA"
            ))
        return edges

class S3Extractor(BaseExtractor):
    resource_types = ["AWS::S3::Bucket"]
    edge_types = ["resource-policy", "kms", "event-notification"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        # Resource policy and KMS via session.s3 GetBucketPolicy / GetBucketEncryption (metadata only)
        return edges

class RDSExtractor(BaseExtractor):
    resource_types = ["AWS::RDS::DBInstance", "AWS::RDS::DBCluster"]
    edge_types = ["security-group", "subnet-group", "kms", "role"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        return edges

class EC2Extractor(BaseExtractor):
    resource_types = ["AWS::EC2::Instance"]
    edge_types = ["eni", "security-group", "subnet", "iam-role", "kms"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        return edges
