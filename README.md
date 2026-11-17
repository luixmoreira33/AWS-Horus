# AWS-Horus

Ferramenta somente-leitura de inventário universal e diagrama de conectividade multi-conta para AWS Organizations.

## Status atual

- Coletor multi-conta com paralelismo, backoff e tolerância a falhas
- Modelo universal de aresta (DECLARADA / PERMITIDA / OBSERVADA)
- Extratores dedicados para os principais serviços (Lambda, S3, RDS, EC2, EKS, CloudFront, VPC, API Gateway, OpenSearch, MWAA, Glue, DMS, MQ, WAF, EFS)
- Writer Neptune com templates openCypher
- API FastAPI
- Frontend React + Cytoscape (grafo, painel, filtros)
- Terraform (conta central + StackSet da role AtlasReadOnly + regras EventBridge)
- CLI de execução
- Testes básicos e documentação

## Como rodar o coletor (local)

```bash
pip install -r requirements.txt
export EXTERNAL_ID=seu-external-id
python -m collector --external-id $EXTERNAL_ID --output resultado.json
```

## Deploy

1. Copie `terraform/terraform.tfvars.example` → `terraform.tfvars` e preencha.
2. `cd terraform && terraform init && terraform apply`
3. Deploy do StackSet nas contas-membro.
4. Configure o endpoint do Neptune no `.env`.

## Criar novo extrator

Veja `docs/how-to-create-extractor.md` e `collector/extractors/_template.py`.

---


