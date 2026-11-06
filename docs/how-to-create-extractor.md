# Como criar um novo extrator em 30 minutos

## Template

Copie `collector/extractors/_template/` e implemente:

```python
from collector.collector import BaseExtractor, Edge

class MyServiceExtractor(BaseExtractor):
    resource_types = ["AWS::MyService::Resource"]
    edge_types = ["specific-relation-1", "specific-relation-2"]

    def discover(self, session, account, region):
        # Use session.client("myservice").list_... or Resource Explorer filter
        client = session.client("myservice", region_name=region)
        return [...]  # list of dicts with arn, properties

    def relations(self, resource):
        edges = []
        # Exemplo: target ARN from config
        target = resource["properties"].get("TargetArn")
        if target:
            edges.append(Edge(
                source_arn=resource["arn"],
                target_arn=target,
                category="EVENTO/INTEGRAÇÃO",
                mechanism="service-specific",
                evidence={"config_field": "TargetArn"},
                evidence_level="DECLARADA"
            ))
        return edges

    def health(self):
        return {"status": "ok", "types": self.resource_types}
```

## Registro
Adicione o módulo em `collector/extractors/__init__.py` ou discovery automático por pasta.

## Testes
Crie fixtures em `tests/fixtures/myservice.json` e teste em `tests/test_extractors.py`.

## Garantia
Adicionar extrator **não** exige alterar:
- Motor de grafo
- Schema de arestas
- API
- Interface (painel usa o modelo universal)
