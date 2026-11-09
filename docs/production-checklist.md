# Production readiness checklist

- [ ] ExternalId gerado e armazenado em Secrets Manager
- [ ] StackSet aplicado em todas as contas-membro
- [ ] Resource Explorer multi-account + aggregator index habilitado
- [ ] Config Aggregator da organização
- [ ] Neptune em VPC privada + IAM auth
- [ ] Workers ECS com task role correta
- [ ] EventBridge rules nas contas-membro encaminhando para o bus central
- [ ] Frontend com autenticação SSO
- [ ] Logs sem dados sensíveis
- [ ] Auditoria de consultas habilitada
- [ ] Testes de amostragem automatizados passando
- [ ] Matriz de cobertura visível na UI
- [ ] Reconciliação full a cada 6h (configurável)
- [ ] Alertas de falhas de coleta (permissão, throttling, serviço desabilitado)

## Custo estimado (produção, org média)

- Neptune db.r6g.large: ~$250–350
- ECS Fargate (workers + API): ~$60–120
- EventBridge + SQS + CloudFront + S3: ~$20
- **Total aproximado: $350–500/mês**

Reduções: Neptune Serverless, workers em Lambda, Flow Logs seletivos.
