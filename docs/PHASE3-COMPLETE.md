# Fase 3 — Completa

## Entregue
- Atualização incremental por eventos (EventBridge → handler que recoleta apenas a conta/região afetada)
- Reconciliação periódica (full scan agendado)
- Ingestão de VPC Flow Logs para marcar arestas como OBSERVADA
- Extratores dos serviços restantes: Route 53, ACM, ECR, Backup, Config, MQ, OpenSearch, MWAA, Glue, DMS, WAF, EFS
- Cobertura completa dos serviços listados originalmente

## Como funciona a atualização
1. Evento CloudTrail/Config chega no EventBridge
2. Handler processa apenas a conta/região
3. Extratores geram arestas atualizadas
4. Writer faz upsert (idempotente)
5. Reconciliação periódica corrige qualquer drift

## Critério de pronto
Mudança de configuração em serviço coberto aparece no diagrama em poucos minutos, e tráfego real eleva o nível de evidência para OBSERVADA.
