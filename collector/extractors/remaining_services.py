from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class MWAAExtractor(BaseExtractor):
    resource_types = ["AWS::MWAA::Environment"]
    edge_types = ["vpc", "subnet", "security-group", "role", "s3"]

    def relations(self, resource: Dict, session=None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        # Execution role, network config, source bucket
        return edges

class GlueExtractor(BaseExtractor):
    resource_types = ["AWS::Glue::Job", "AWS::Glue::Crawler", "AWS::Glue::Database"]
    edge_types = ["role", "s3", "catalog"]

    def relations(self, resource: Dict, session=None) -> List[Edge]:
        return []

class DMSExtractor(BaseExtractor):
    resource_types = ["AWS::DMS::ReplicationInstance", "AWS::DMS::Endpoint", "AWS::DMS::ReplicationTask"]
    edge_types = ["subnet", "security-group", "role", "source", "target"]

    def relations(self, resource: Dict, session=None) -> List[Edge]:
        return []

class MQExtractor(BaseExtractor):
    resource_types = ["AWS::AmazonMQ::Broker"]
    edge_types = ["subnet", "security-group", "kms"]

    def relations(self, resource: Dict, session=None) -> List[Edge]:
        return []

class WAFExtractor(BaseExtractor):
    resource_types = ["AWS::WAFv2::WebACL"]
    edge_types = ["association", "rule"]

    def relations(self, resource: Dict, session=None) -> List[Edge]:
        # Associações com ALB, API Gateway, CloudFront
        return []

class EFSExtractor(BaseExtractor):
    resource_types = ["AWS::EFS::FileSystem"]
    edge_types = ["mount-target", "security-group", "kms"]

    def relations(self, resource: Dict, session=None) -> List[Edge]:
        return []
