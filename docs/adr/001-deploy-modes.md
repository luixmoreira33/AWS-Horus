# ADR 001 — Modos de Deploy

## Contexto
Produto self-hosted. Precisa de opção barata (trial/HOM) e opção escalável (PRD).

## Decisão
Variável de ambiente/Terraform `DEPLOY_MODE=lite|enterprise`.
- Lite: PostgreSQL + tabelas de arestas (ou DuckDB para single-node).
- Enterprise: Amazon Neptune.

HOM default = lite. PRD default = enterprise. Ambos suportados.

## Consequências
Código de grafo deve ser abstraído atrás de uma interface. Custo documentado por modo.
