# Frontend AWS-Horus (React + TypeScript + Cytoscape.js)

## Setup rápido

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install cytoscape cytoscape-elk @types/cytoscape
```

## Componentes principais

- `GraphView.tsx` — Cytoscape com layout ELK hierárquico
- `ResourcePanel.tsx` — painel lateral com vizinhos, evidências, riscos
- `Filters.tsx` — conta, região, VPC, tipo, tag, porta, categoria, nível de evidência
- `CoverageMatrix.tsx` — matriz de cobertura
- `PathQuery.tsx` — “como A chega em B?”

## Recursos

- Zoom semântico: Org → Conta → Região → VPC → Subnet → Recurso
- Ícones oficiais AWS, cor por conta, espessura por tráfego
- Tracejada = PERMITIDA, sólida = OBSERVADA
- Painel lateral completo + filtros + busca + export

## Autenticação

SSO / OIDC (Cognito ou IAM Identity Center).

## Deploy

Build estático → S3 + CloudFront (provisionado no Terraform).
