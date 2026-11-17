"""
Matriz de cobertura gerada automaticamente a partir dos extratores registrados.
"""
from typing import List, Dict

COVERAGE = [
    {"service": "EC2", "type": "AWS::EC2::Instance", "extractor": "EC2Extractor", "status": "complete"},
    {"service": "RDS", "type": "AWS::RDS::DBInstance", "extractor": "RDSExtractor", "status": "complete"},
    {"service": "S3", "type": "AWS::S3::Bucket", "extractor": "S3Extractor", "status": "complete"},
    {"service": "Lambda", "type": "AWS::Lambda::Function", "extractor": "LambdaExtractor", "status": "complete"},
    {"service": "VPC / SG", "type": "AWS::EC2::SecurityGroup", "extractor": "SecurityGroupExtractor", "status": "complete"},
    {"service": "ELB", "type": "AWS::ElasticLoadBalancingV2::LoadBalancer", "extractor": "ELBExtractor", "status": "complete"},
    {"service": "CloudFront", "type": "AWS::CloudFront::Distribution", "extractor": "CloudFrontExtractor", "status": "complete"},
    {"service": "API Gateway", "type": "AWS::ApiGateway::RestApi", "extractor": "APIGatewayExtractor", "status": "complete"},
    {"service": "EKS", "type": "AWS::EKS::Cluster", "extractor": "EKSExtractor", "status": "complete"},
    {"service": "Route 53", "type": "AWS::Route53::HostedZone", "extractor": "Route53Extractor", "status": "complete"},
    {"service": "ECR", "type": "AWS::ECR::Repository", "extractor": "ECRExtractor", "status": "complete"},
    {"service": "Backup", "type": "AWS::Backup::BackupVault", "extractor": "BackupExtractor", "status": "complete"},
    {"service": "MQ", "type": "AWS::AmazonMQ::Broker", "extractor": "MQExtractor", "status": "complete"},
    {"service": "OpenSearch", "type": "AWS::OpenSearchService::Domain", "extractor": "OpenSearchExtractor", "status": "complete"},
    {"service": "EFS", "type": "AWS::EFS::FileSystem", "extractor": "EFSExtractor", "status": "complete"},
    {"service": "WAF", "type": "AWS::WAFv2::WebACL", "extractor": "WAFExtractor", "status": "complete"},
    {"service": "Glue", "type": "AWS::Glue::Job", "extractor": "GlueExtractor", "status": "complete"},
    {"service": "MWAA", "type": "AWS::MWAA::Environment", "extractor": "MWAAExtractor", "status": "complete"},
    {"service": "DMS", "type": "AWS::DMS::ReplicationInstance", "extractor": "DMSExtractor", "status": "complete"},
]

def get_coverage_matrix() -> List[Dict]:
    return COVERAGE
