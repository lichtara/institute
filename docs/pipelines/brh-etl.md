# Pipeline ETL — BRH (Notion → Repo → Análise)

Objetivo: exportar dados do Notion, validar contra schemas, anonimizar e disponibilizar artefatos sintéticos para desenvolvimento.

## Fluxo
1. **Export Notion**
   - Exportar como CSV por data source (Protocolos, Sessões, Métricas)
   - Armazenar export bruto fora do repositório
2. **Normalização**
   - Padronizar nomes de colunas conforme o dicionário de dados
   - Converter datas para `YYYY-MM-DD`
   - Garantir enums exatos
3. **Anonimização**
   - Remover campos sensíveis ou substituir por códigos
   - Mapear relações por slug humano (não usar URLs internas)
4. **Validação**
   - Validar CSVs com os JSON Schemas em `data/schemas/*`
   - Rejeitar linhas com enums inválidos ou datas fora do padrão
5. **Publicação sintética**
 - Gerar `data/samples/*.csv` com subconjuntos e dados sintéticos
  - Nunca commitar dados reais
  - Registrar resultados de certificação em `docs/certification/states/checks.csv`
6. **Consumo**
   - `analysis/notebooks/*` consome samples e schemas
   - Dashboards utilizam agregados sem PII

## Ferramentas sugeridas
- Python: `pandera` ou `pydantic` + `jsonschema`
- Pre-commit hooks: `csvlint`, verificação de PII básica
- Makefile: `make validate`, `make samples`

## Padrões de erro comuns
- Espaços extras em valores enum
- Datas com timezone
- Relações usando URL em vez de slug humano

## Próximos passos
- Considerar Makefile simples com tarefas `validate` e `samples`
- Criar script Python para validação utilizando `jsonschema`
  - Comando disponível: `make validate`
