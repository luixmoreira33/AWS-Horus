# Exemplos de queries openCypher para Neptune

## Vizinhos de um recurso
```cypher
MATCH (n {arn: $arn})-[r]->(m)
RETURN m.arn AS target, r.category, r.mechanism, r.evidence_level, r.ports
UNION
MATCH (n {arn: $arn})<-[r]-(m)
RETURN m.arn AS source, r.category, r.mechanism, r.evidence_level, r.ports
```

## Caminho entre A e B
```cypher
MATCH path = shortestPath((a {arn: $from})-[*1..6]-(b {arn: $to}))
RETURN path
```

## Recursos por tipo e conta
```cypher
MATCH (n)
WHERE n.type = $type AND n.account = $account
RETURN n.arn, n.region LIMIT 100
```

## Arestas observadas com tráfego
```cypher
MATCH ()-[r:CONNECTED]->()
WHERE r.evidence_level = 'OBSERVADA' AND r.bytes > 0
RETURN r.source, r.target, r.ports, r.bytes
ORDER BY r.bytes DESC
LIMIT 50
```
