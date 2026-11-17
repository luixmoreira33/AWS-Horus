from collector.collector import BaseExtractor, Edge
from typing import Dict, List, Optional
import boto3

class ELBExtractor(BaseExtractor):
    resource_types = ["AWS::ElasticLoadBalancingV2::LoadBalancer", "AWS::ElasticLoadBalancingV2::Listener", "AWS::ElasticLoadBalancingV2::TargetGroup"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        # Listener → Target Group
        if "ListenerArn" in props or resource.get("type", "").endswith("Listener"):
            tg = props.get("DefaultActions", [{}])[0].get("TargetGroupArn")
            if tg:
                edges.append(Edge(
                    source_arn=arn,
                    target_arn=tg,
                    category="REDE",
                    mechanism="elb-listener-to-target-group",
                    evidence={"source": "listener-default-action"},
                    evidence_level="DECLARADA"
                ))
        # Target Group → Targets (instances, IPs, Lambda)
        for target in props.get("Targets", []):
            target_id = target.get("Id")
            if target_id:
                edges.append(Edge(
                    source_arn=arn,
                    target_arn=target_id,
                    category="REDE",
                    mechanism="target-group-registration",
                    ports=[target.get("Port")] if target.get("Port") else None,
                    evidence={"health": target.get("HealthCheckPort")},
                    evidence_level="DECLARADA"
                ))
        return edges

class CloudFrontExtractor(BaseExtractor):
    resource_types = ["AWS::CloudFront::Distribution"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        origins = props.get("Origins", {}).get("Items", []) if isinstance(props.get("Origins"), dict) else props.get("Origins", [])
        for origin in origins:
            domain = origin.get("DomainName", "")
            if ".s3." in domain or domain.endswith(".s3.amazonaws.com"):
                bucket = domain.split(".")[0]
                edges.append(Edge(
                    source_arn=arn,
                    target_arn=f"arn:aws:s3:::{bucket}",
                    category="DADOS",
                    mechanism="cloudfront-origin-s3",
                    evidence={"origin_id": origin.get("Id")},
                    evidence_level="DECLARADA"
                ))
            else:
                edges.append(Edge(
                    source_arn=arn,
                    target_arn=f"arn:aws:elasticloadbalancing:::loadbalancer/{domain}",
                    category="REDE",
                    mechanism="cloudfront-origin-custom",
                    evidence={"domain": domain},
                    evidence_level="DECLARADA"
                ))
        cert = props.get("ViewerCertificate", {}).get("ACMCertificateArn")
        if cert:
            edges.append(Edge(
                source_arn=arn,
                target_arn=cert,
                category="CRIPTOGRAFIA",
                mechanism="cloudfront-acm",
                evidence_level="DECLARADA"
            ))
        return edges

class APIGatewayExtractor(BaseExtractor):
    resource_types = ["AWS::ApiGateway::RestApi", "AWS::ApiGatewayV2::Api"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        # Integrations (Lambda, HTTP, VPC Link) — preenchido via describe se session disponível
        if session:
            try:
                apigw = session.client("apigateway")
                api_id = arn.split("/")[-1]
                integrations = apigw.get_integrations(restApiId=api_id) if "RestApi" in resource.get("type", "") else {}
                for integ in integrations.get("items", []):
                    uri = integ.get("uri", "")
                    if "lambda" in uri.lower():
                        edges.append(Edge(
                            source_arn=arn,
                            target_arn=uri,
                            category="EVENTO/INTEGRAÇÃO",
                            mechanism="apigw-lambda-integration",
                            evidence={"type": integ.get("type")},
                            evidence_level="DECLARADA"
                        ))
            except Exception:
                pass
        return edges

class EKSExtractor(BaseExtractor):
    resource_types = ["AWS::EKS::Cluster"]

    def relations(self, resource: Dict, session: Optional[boto3.Session] = None) -> List[Edge]:
        edges = []
        arn = resource["arn"]
        props = resource.get("properties", {}) or {}
        role = props.get("RoleArn") or props.get("roleArn")
        if role:
            edges.append(Edge(
                source_arn=arn,
                target_arn=role,
                category="IAM/AUTORIZAÇÃO",
                mechanism="eks-cluster-role",
                evidence_level="DECLARADA"
            ))
        vpc_config = props.get("resourcesVpcConfig") or props.get("VpcConfig") or {}
        for sg in vpc_config.get("securityGroupIds", []) + vpc_config.get("SecurityGroupIds", []):
            edges.append(Edge(
                source_arn=arn,
                target_arn=f"arn:aws:ec2:{resource.get('region')}:{resource.get('account')}:security-group/{sg}",
                category="REDE",
                mechanism="eks-security-group",
                evidence_level="DECLARADA"
            ))
        return edges
