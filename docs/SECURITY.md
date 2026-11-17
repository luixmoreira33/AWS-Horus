# Relatório de Segurança — AWS-Horus v1.0

## Princípios
- Least privilege
- Somente leitura
- ExternalId em todo AssumeRole
- Sem credenciais estáticas de longa duração

## Permissões da role AtlasReadOnly
- AWS managed: SecurityAudit, ViewOnlyAccess
- Adicionais justificados: resource-explorer:Search, config:List*, config:Select*, ec2:Describe*, rds:Describe*, s3:GetBucket*, lambda:Get*, elasticloadbalancing:Describe*, cloudfront:Get*, apigateway:GET, eks:Describe*, etc.
- Explicitamente negado: s3:GetObject, secretsmanager:GetSecretValue, ssm:GetParameter (com decrypt)

## Autenticação
- SSO/OIDC (IAM Identity Center ou IdP externo)
- RBAC: viewer / analyst / admin

## Dados
- Nenhum conteúdo de dados é lido
- Apenas metadados e configuração
