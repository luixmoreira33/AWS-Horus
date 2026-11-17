# Fase 2 — Em andamento

## Entregue
- API FastAPI com endpoints reais: `/resources/{arn}/neighbors`, `/path`, `/exposure`, `/search`
- Ligação à camada de queries do Postgres (LiteQueries)
- Frontend React + Cytoscape com:
  - Busca de recursos
  - Painel de vizinhos (entrada/saída com evidência)
  - UI para "Como A chega em B?"
  - Layout básico do grafo

## Próximo
- Conectar fetch real no frontend
- Agrupamento por camadas (Conta → Região → VPC)
- Filtros por categoria e nível de evidência
- Export (Mermaid / PNG)
