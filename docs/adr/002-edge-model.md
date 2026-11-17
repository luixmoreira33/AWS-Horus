# ADR 002 — Modelo Universal de Aresta

## Decisão
Toda relação é uma aresta com:
- source_arn, target_arn
- category, mechanism
- ports, protocol
- evidence (objeto livre), evidence_level (DECLARADA | PERMITIDA | OBSERVADA)
- risk, first_seen, last_seen

IDs estáveis são ARNs. Schema versionado em schemas/edge.schema.json.
