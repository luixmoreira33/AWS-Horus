# Matriz de Cobertura e Relatório de Lacunas

## Matriz de Cobertura (exemplo - gerada dinamicamente pela ferramenta)

| Tipo de Recurso          | Qtd (exemplo) | Extrator     | Arestas calculadas                  | Arestas faltantes          | Lacunas de fonte          |
|--------------------------|---------------|--------------|-------------------------------------|----------------------------|---------------------------|
| AWS::Lambda::Function    | 120           | DEDICADO     | role, vpc/sg, event-source, kms    | X-Ray traces               | Flow Logs parcial         |
| AWS::S3::Bucket          | 85            | DEDICADO     | resource-policy, kms, events       | access logs content        | -                         |
| AWS::RDS::DBInstance     | 12            | DEDICADO     | sg, subnet, kms, role              | performance insights       | -                         |
| AWS::EC2::Instance       | 45            | GENÉRICO     | eni, sg, subnet, role, kms         | detailed process           | Flow Logs                 |
| AWS::SQS::Queue          | 30            | DEDICADO     | resource-policy, lambda trigger    | -                          | -                         |
| AWS::IAM::Role           | 200           | GENÉRICO     | trust-policy, attached policies    | SCP intersection           | -                         |
| ... (todos os tipos)     | ...           | SEM COBERTURA| ARN refs genéricos                 | -                          | -                         |

**Regra:** 100% dos tipos encontrados aparecem. Sem extrator dedicado → GENÉRICO + marcação "cobertura parcial".

## Serviços prioritários (sua organização)

Extratores dedicados devem ser criados primeiro para: EC2, RDS, EFS, CloudFront, CloudWatch, Glue, S3, WAF, VPC, MWAA, ELB, Backup, Config, Route 53, MQ, OpenSearch, ACM, DMS, API Gateway, EKS, ECR.

## Relatório de Lacunas e Recomendações

### Fontes de tráfego observado
- **VPC Flow Logs**: Habilitados em 40% das VPCs. Recomendação: habilitar em VPCs críticas (custo ~$0.50/GB). IaC disponível no StackSet.
- **CloudTrail data events**: Desabilitado na maioria. Recomendação: habilitar seletivamente para S3/Lambda (custo alto se volume grande).
- **X-Ray**: Parcial. Recomendação: sampling em Lambdas críticas.
- **ALB/NLB access logs**: Baixa cobertura. Recomendação: habilitar para load balancers expostos.

### Cobertura de extratores
- Priorizar os tipos mais numerosos (descobertos no inventário).
- Extratores dedicados Fase 2: Lambda, S3, RDS, EC2, SQS, SNS, EventBridge, ECS, EKS, IAM + os listados acima.
- Genérico cobre o restante via ARN references + ENI ownership.

### Riscos e aproximações
- IAM + SCPs: análise marcada como "aproximada" na UI quando SCPs não forem totalmente resolvidas.
- Alcançabilidade completa (TGW/peering/NACL) em Fase 2.

### Como melhorar
1. Habilitar Resource Explorer multi-account + aggregator index.
2. Habilitar Config em todas as contas/regiões.
3. Adicionar extratores seguindo o template (`collector/extractors/_template/`).
4. Ativar Flow Logs seletivamente.
