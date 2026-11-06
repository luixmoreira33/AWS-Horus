# Frontend React + TypeScript + Cytoscape.js

## Estrutura planejada
```
frontend/
  src/
    components/
      GraphView.tsx       # Cytoscape / ELK hierarchical layout
      ResourcePanel.tsx   # Painel lateral: config, vizinhos, evidências, riscos
      Filters.tsx
      CoverageMatrix.tsx
      PathQuery.tsx
    services/
      api.ts
    App.tsx
  package.json
```

## Recursos principais
- Zoom semântico: Org → Conta → Região → VPC → Subnet → Recurso
- Ícones oficiais AWS por tipo
- Cor por conta, espessura por tráfego observado
- Estilo: tracejada = PERMITIDA, sólida = OBSERVADA
- Clique → painel com todos os vizinhos (categoria, porta, evidência, nível)
- Botão "mostrar tudo que se conecta" (profundidade 1-3)
- Filtros: conta, região, VPC, tipo, tag, porta, categoria, evidência, "exposto à internet", "cross-account", "permitido mas nunca usado"
- Busca: nome, ID, ARN, IP, tag
- Export: PNG, SVG, JSON, Mermaid, Draw.io
- Autenticação SSO/OIDC

O frontend consome a API e renderiza o modelo universal de arestas sem lógica específica de serviço.
