# AWS-Horus

**AWS-Horus** (evolução do conceito AWS Atlas) é uma ferramenta somente-leitura que se conecta à sua AWS Organization (conta central + todas as subcontas) e gera um diagrama interativo, atualizado quase em tempo real, mostrando **todos** os recursos e **como** eles se conectam: quem fala com quem, por qual caminho, porta/protocolo, permissão e se a conexão é apenas permitida ou realmente usada.

O modelo é **universal**. Não é específico de nenhum serviço. RDS, EC2, Lambda, S3, SQS, EKS, API Gateway, KMS, CloudFront e qualquer outro seguem o mesmo modelo de aresta. Ao clicar em qualquer recurso, você vê todos os vizinhos de entrada e saída com a evidência de cada conexão.

## Serviços prioritários na sua organização

Com base no inventário atual, os extratores dedicados serão priorizados para:

- Elastic Compute Cloud (EC2)
- Relational Database Service (RDS / Aurora)
- Elastic File System (EFS)
- Data Transfer
- CloudFront
- CloudWatch
- Glue
- Simple Storage Service (S3)
- WAF
- Virtual Private Cloud (VPC)
- Managed Workflows for Apache Airflow (MWAA)
- Elastic Load Balancing (ELB / ALB / NLB)
- Backup
- Config
- Route 53
- MQ
- OpenSearch Service
- Certificate Manager (ACM)
- Database Migration Service (DMS)
- API Gateway
- EKS
- ECR

Mesmo sem extrator dedicado, **todo** recurso aparece com relações genéricas (ARN, ENI, SG, role, KMS, resource policy etc.) e a marcação "cobertura parcial" na matriz.

## Arquitetura (resumo)

- **Inventário**: Resource Explorer (multi-account) + Config Aggregator + APIs diretas para gaps.
- **Modelo de aresta universal**: origem/destino ARN, categoria (REDE | EVENTO/INTEGRAÇÃO | IAM | DNS | DADOS | CRIPTO | OBSERVABILIDADE | CI/CD), mecanismo, porta/protocolo, evidência, nível (DECLARADA | PERMITIDA | OBSERVADA).
- **Atualização**: EventBridge → SQS → workers incrementais + full reconciliation periódica.
- **Banco**: Amazon Neptune (openCypher).
- **Interface**: React + Cytoscape.js com zoom semântico e painel lateral.
- **Acesso**: Role `AtlasReadOnly` (SecurityAudit + ViewOnlyAccess + extras) via STS + ExternalId. Somente leitura.

## Estrutura do repositório

```
├── README.md
├── docs/
│   ├── architecture.md
│   ├── coverage-matrix.md
│   └── how-to-create-extractor.md
├── terraform/
│   ├── main.tf
│   ├── member-role-stackset.yaml
│   └── event-rules-note.md
├── collector/
│   └── collector.py
├── api/
│   └── main.py
├── frontend/
│   └── README.md
└── tests/
    └── README.md
```

## Como começar

1. Ajuste o ExternalId e o account ID central no Terraform.
2. `cd terraform && terraform init && terraform apply` (conta central).
3. Deploy do StackSet nas contas-membro.
4. Configure workers e frontend.

Veja `docs/` para detalhes completos, matriz de cobertura e como criar novos extratores em ~30 minutos.

---

**Princípio**: um serviço novo ou raro entra no diagrama sem mudar o motor, o banco ou a interface.
