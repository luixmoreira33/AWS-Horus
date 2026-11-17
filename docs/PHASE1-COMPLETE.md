# Fase 1 — Completa

## Entregue
- Coletor multi-conta com relações genéricas reais + extratores dedicados (SG, VPC, EC2, RDS, S3, Lambda, ELB, CloudFront, API Gateway, EKS)
- Writer abstraído + PostgresWriter (modo Lite) com schema e upsert
- Runner que liga coleta → gravação no grafo
- Queries Lite: neighbors, path (recursive CTE), exposure
- Testbed sintético: VPC + SG + Lambda + S3 + RDS + ALB

## Como validar
1. `cd testbed && terraform apply`
2. Configurar ExternalId e role AtlasReadOnly na conta de teste
3. `python -m collector --external-id ...` ou usar `runner.run_full_scan`
4. Consultar vizinhos e caminhos via `LiteQueries`

## Critério de pronto da Fase 1
- Mapa de uma organização de teste aparece corretamente de ponta a ponta (recursos + arestas reais no Postgres).
