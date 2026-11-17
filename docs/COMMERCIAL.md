# AWS-Horus — Pacote Comercial (Self-hosted)

## Proposta de valor
Mapa interativo somente-leitura de toda a AWS Organization, com evidência em cada conexão. Responde em segundos:
- Quem acessa este RDS?
- O que acontece se eu apagar este Security Group?
- Quais recursos estão expostos à internet?
- Como A chega em B?
- O que mudou desde ontem?

## Modos
| Modo | Grafo | Uso | Custo estimado (conta central) |
|------|-------|-----|--------------------------------|
| Lite | PostgreSQL | Trial / HOM / Organizações pequenas | ~USD 50-150/mês |
| Enterprise | Amazon Neptune | Produção / Organizações grandes | ~USD 400-900/mês |

## Pricing (self-hosted)
- Licença anual por Organization (ilimitadas contas-membro)
- Inclui atualizações e suporte
- Sem cobrança por recurso ou por aresta

## ROI típico
- Redução de tempo de troubleshooting (SRE)
- Descoberta de exposições antes de auditoria
- Documentação viva (substitui diagramas manuais)

## Quickstart (10 minutos)
1. `terraform apply` na conta central
2. StackSet da role AtlasReadOnly nas contas-membro
3. Primeira coleta
4. Acessar a UI

## Segurança
- Somente leitura (SecurityAudit + ViewOnlyAccess + permissões mínimas adicionais)
- ExternalId obrigatório
- Sem GetObject, GetSecretValue ou GetParameter decrypt
- Auth SSO/OIDC + RBAC
