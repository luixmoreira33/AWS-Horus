# Testes de amostragem (critério de aceite)

Para cada tipo de recurso presente, ao menos 1 recurso real deve ter as relações esperadas.

## Exemplos esperados (Fase 1 - genérico + serviços prioritários)

- Lambda / EC2 / EKS: deve ter aresta para Role (IAM/AUTORIZAÇÃO, DECLARADA)
- S3 Bucket: deve ter aresta para resource policy principals (se existir) e KMS
- RDS / OpenSearch / MQ: deve ter aresta para Security Group e Subnet (REDE, DECLARADA)
- Qualquer recurso em VPC: aresta para SG/subnet via ENI
- Qualquer recurso com KMS: aresta CRIPTOGRAFIA
- CloudFront / API Gateway / ALB: arestas de origem e targets

## Como rodar
```bash
pytest tests/ -v
```

Os testes usam fixtures de Resource Explorer / Config e verificam o modelo de Edge.
