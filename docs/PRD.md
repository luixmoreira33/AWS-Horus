# PRD — AWS-Horus v1.0 (MVP Self-hosted)

## Visão
Ferramenta somente-leitura que mapeia toda a AWS Organization e responde perguntas reais de conectividade, exposição e impacto, com evidência em cada aresta.

## Personas
- SRE / DevOps: troubleshooting e blast radius
- CloudSec / Segurança: exposição e permissões sem uso
- Arquitetura: documentação viva e onboarding
- FinOps / Gestão: custo previsível e cobertura

## Casos de uso campeões (ordem confirmada)
1. Quem acessa este RDS e por qual caminho?
2. O que acontece se eu apagar este Security Group? (blast radius)
3. Quais recursos estão expostos à internet?
4. Como A chega em B?
5. O que mudou desde ontem?

## Escopo do MVP
Cobertura completa dos serviços listados originalmente: EC2, RDS/Aurora, EFS, Data Transfer, CloudFront, CloudWatch, Glue, S3, WAF, VPC, MWAA, ELB, Backup, Config, Route 53, MQ, OpenSearch, ACM, DMS, API Gateway, EKS, ECR.

## Critérios de aceite do MVP
- Deploy ajustável por variável (HOM/PRD → Lite ou Enterprise)
- Primeira coleta útil em ≤ 10 minutos
- Os 5 casos de uso respondidos na UI com evidência
- Somente-leitura, ExternalId, sem dados sensíveis
- Matriz de cobertura visível
- Modo self-hosted only

## Fora do MVP (v2)
- SaaS gerenciado
- Tráfego observado em tempo real em todas as contas (pode ser parcial no MVP)
- Multi-cloud
