# Arquitetura AWS-Horus

## Fluxo
Contas-membro (role AtlasReadOnly) → Coletor (Resource Explorer + Config + Describe) → Modelo de Aresta → Grafo (Lite=Postgres / Enterprise=Neptune) → API FastAPI → UI React+Cytoscape

## Atualização
EventBridge cross-account + SQS + workers incrementais + full reconciliation periódica.

## Modos
Controlado por variável DEPLOY_MODE (lite | enterprise).

## Segurança
Somente-leitura, ExternalId, sem GetObject / GetSecretValue / GetParameter decrypt.
