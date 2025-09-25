# Especificação — Dashboard Operacional

Objetivo: visibilidade de fluxo de trabalho, conformidade e prazos.

## Métricas
- Throughput semanal de tarefas (issues fechadas)
- Tempo médio de ciclo por tipo (pesquisa, código, docs)
- Conformidade com checklists de certificação
- Status de revisões e aprovações (gates)

## Fontes
- GitHub issues/PRs
- `docs/certification/states/checks.csv`
- CI pipelines (status)

## Atualização
- Contínua (webhooks) + diária (batch)
