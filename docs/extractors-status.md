# Status dos extratores

## Dedicados implementados (esqueleto com estrutura pronta)
- Lambda
- S3
- RDS
- EC2
- EKS
- CloudFront
- VPC / Subnet / SG / RouteTable
- API Gateway
- OpenSearch
- MWAA
- Glue
- DMS
- MQ
- WAF
- EFS

## Genérico
Cobre qualquer outro tipo via referências de ARN, ENI, role, KMS, resource policy.

## Próximo
Preencher as chamadas de API reais (GetBucketPolicy, DescribeNetworkInterfaces, ListEventSourceMappings etc.) e testes com fixtures.
