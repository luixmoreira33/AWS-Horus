# AWS-Horus

Ferramenta somente-leitura que mapeia toda a sua AWS Organization e mostra como cada recurso se conecta aos demais, com evidência.

## Status
v1.0 (self-hosted) — pronto para produção.

## Quickstart
```bash
# 1. Conta central
cd terraform && terraform init && terraform apply

# 2. Role nas contas-membro (StackSet)
# Ver terraform/member-role-stackset.yaml

# 3. Coleta
export EXTERNAL_ID=seu-external-id
export DATABASE_URL=postgresql://...
python -m collector --external-id $EXTERNAL_ID

# 4. API + UI
cd api && uvicorn main:app --reload
cd frontend && npm install && npm run dev
```

## Casos de uso
- Quem acessa este RDS?
- Blast radius de um Security Group
- Recursos expostos à internet
- Como A chega em B?
- Diff temporal

## Modos
- **Lite** (PostgreSQL) — barato, ideal para trial/HOM
- **Enterprise** (Neptune) — escalável para organizações grandes

Controlado pela variável `DEPLOY_MODE`.

## Documentação
- [Arquitetura](docs/ARCHITECTURE.md)
- [PRD](docs/PRD.md)
- [Pacote Comercial](docs/COMMERCIAL.md)
- [Segurança](docs/SECURITY.md)
- [Matriz de Cobertura](docs/coverage-matrix.md)

## Licença
Self-hosted. Veja docs/COMMERCIAL.md para detalhes de licenciamento.
