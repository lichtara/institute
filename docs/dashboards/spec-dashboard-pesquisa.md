# Especificação — Dashboard de Pesquisa BRH

Objetivo: monitorar execução de estudos, qualidade de dados e segurança.

## Métricas
- Execução: sessões planejadas vs realizadas, aderência ao protocolo
- Dados: % completude, taxas de artefatos removidos, latência de processamento
- Segurança: incidentes reportados, acessos incomuns
- Ética: status de consentimentos, revisões pendentes

## Fontes
- `research/logs` de sessão (estruturado)
- `analysis/outputs` métricas de qualidade
- `issues`/PRs (governança de mudanças)

## Layout (exemplo)
- Linha 1: KPIs grandes
- Linha 2: série temporal qualidade de dados
- Linha 3: tabela de exceções (outliers, faltantes)
- Linha 4: quadro de conformidade ética (sem PII)

## Atualização
- Frequência diária (automação via workflow)
