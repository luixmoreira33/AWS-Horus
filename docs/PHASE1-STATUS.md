# Fase 1 — Status

## Concluído
- Relações genéricas por ARN (roles, KMS, SGs)
- Extratores reais: Security Group (regras), EC2 (ENI→SG), RDS (SG+KMS), S3 (encryption), Lambda, ELB (listener→TG→targets), CloudFront (origins + ACM), API Gateway (integrations), EKS (role + SG)
- Abstracao de writer + PostgresWriter (Lite) com schema idempotente
- Testbed sintético mínimo (VPC + SG + Lambda + S3)

## Próximo
- Conectar o coletor ao PostgresWriter no modo lite
- Expandir testbed com RDS + ALB
- Queries de caminho e exposição sobre o Postgres
