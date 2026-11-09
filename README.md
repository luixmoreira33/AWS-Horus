# AWS-Horus - Produção

## Status

Base completa da Fase 1–4 pronta para deploy e extensão.

- Coletor multi-conta com backoff, paralelismo e tolerância a falhas
- Modelo universal de aresta
- Extratores dedicados (Lambda, S3, RDS, EC2) + template
- Terraform (conta central + StackSet de role)
- API FastAPI
- Estrutura frontend React + Cytoscape
- Documentação de deploy, operação e criação de extratores

## Serviços prioritários

EC2, RDS/Aurora, EFS, CloudFront, CloudWatch, Glue, S3, WAF, VPC, MWAA, ELB, Backup, Config, Route 53, MQ, OpenSearch, ACM, DMS, API Gateway, EKS, ECR.

Todo recurso aparece mesmo sem extrator dedicado (cobertura genérica + marcação "parcial").

## Pré-requisitos

- Conta central com permissões de Organizations
- ExternalId forte gerado
- Resource Explorer multi-account habilitado (recomendado)
- Config Aggregator (recomendado)

## Deploy

1. Ajuste variáveis em `terraform/terraform.tfvars`:
   - `central_account_id`
   - `external_id`
   - `org_id`
2. `cd terraform && terraform init && terraform apply`
3. Deploy do StackSet (`member-role-stackset.yaml`) nas contas-membro
4. Build e deploy do frontend no bucket S3 gerado
5. Suba os workers ECS (task definition a partir da imagem do coletor)

## Operação

- Full scan: executar o coletor periodicamente ou sob demanda
- Incremental: eventos EventBridge → SQS → workers
- Matriz de cobertura: endpoint `/coverage` da API
- Lacunas de Flow Logs / CloudTrail data events aparecem automaticamente

## Criar novo extrator

Ver `docs/how-to-create-extractor.md` e `collector/extractors/_template.py`.

Tempo estimado: 30 minutos para um serviço novo.
