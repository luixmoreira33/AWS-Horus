from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class EKSExtractor(BaseExtractor):
    resource_types = ["AWS::EKS::Cluster"]
    edge_types = ["iam-role", "vpc", "subnet", "security-group", "kms"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        conf = props.get("Configuration") or props
        role = conf.get("RoleArn")
        if role:
            edges.append(Edge(source_arn=arn, target_arn=role, category="IAM/AUTORIZAÇÃO", mechanism="cluster-role", evidence={"field": "RoleArn"}, evidence_level="DECLARADA"))
        # VPC config, subnets, SGs, KMS similarly
        return edges

class CloudFrontExtractor(BaseExtractor):
    resource_types = ["AWS::CloudFront::Distribution"]
    edge_types = ["origin", "certificate", "waf", "s3-bucket"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        # Origins (S3 or custom), ACM cert, WAF WebACL
        return edges

class VPCExtractor(BaseExtractor):
    resource_types = ["AWS::EC2::VPC", "AWS::EC2::Subnet", "AWS::EC2::SecurityGroup", "AWS::EC2::RouteTable"]
    edge_types = ["peering", "tgw", "endpoint", "nacl", "route"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        # Peering, TGW attachments, VPC endpoints, NACL associations, routes
        return edges

class APIGatewayExtractor(BaseExtractor):
    resource_types = ["AWS::ApiGateway::RestApi", "AWS::ApiGatewayV2::Api"]
    edge_types = ["integration", "authorizer", "vpc-link", "lambda"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        # Integrations to Lambda, HTTP, VPC Link, authorizers
        return edges

class OpenSearchExtractor(BaseExtractor):
    resource_types = ["AWS::OpenSearchService::Domain"]
    edge_types = ["security-group", "subnet", "kms", "role", "vpc"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        return edges
