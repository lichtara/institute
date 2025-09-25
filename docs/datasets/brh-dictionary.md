# Dicionário de Dados — BRH

Este dicionário documenta o mapeamento Notion ↔ repositório para os conjuntos **Protocolos**, **Sessões** e **Métricas**.

## BRH – Protocolos
- **Nome do Protocolo**
  - Tipo: string
  - Notion: `title`
  - Observação: chave humana
- **Status**
  - Tipo: enum `{Em rascunho, Em validação, Ativo}`
  - Notion: `status`
- **Nível de complexidade**
  - Tipo: enum `{Básico, Intermediário, Avançado}`
  - Notion: `status`
- **Dimensão-alvo**
  - Tipo: enum `{3D, 4D, 5D, Multidimensional}`
  - Notion: `select`
- **Faixa de frequência (Hz)**, **Objetivo**, **Indicadores de coerência**, **Contraindicações**, **Notas**
  - Tipo: string
  - Notion: `text`

## BRH – Sessões
- **Título da Sessão**
  - Tipo: string
  - Notion: `title`
- **Data**
  - Tipo: date (`YYYY-MM-DD`)
  - Notion: `date`
- **Protocolo aplicado**
  - Tipo: string
  - Notion: `relation → Protocolos`
  - Observação: usar id/slug humano do protocolo
- **Dimensão percebida**
  - Tipo: enum `{3D, 4D, 5D, Multidimensional}`
- **Intensidade**
  - Tipo: enum `{Baixa, Média, Alta}`
- **Estado da Sessão**
  - Tipo: enum `{Aberta, Em integração, Encerrada}`
- **Indicador de validação**
  - Tipo: enum `{Coerência percebida, Assentimento corporal, Outro}`
- **Janela de validação**
  - Tipo: enum `{24h, 7d}`
- **Microdecisão**, **Pergunta central**, **Critério de validação**, **Confirmação do Campo**, **Timbre**, **Pessoas**, **Projeto**, **Log ML**
  - Tipo: string

## BRH – Métricas
- **Indicador**
  - Tipo: string
  - Notion: `title`
- **Sessão**
  - Tipo: string
  - Notion: `relation → Sessões`
  - Observação: usar id/slug humano da sessão
- **Valor**
  - Tipo: number
- **Unidade**
  - Tipo: string
- **Janela temporal**
  - Tipo: enum `{Imediato, 24h, 7d, 28d}`
- **Método de medição**, **Observações**
  - Tipo: string

## Convenções
- Nenhum dado sensível ou identificação pessoal deve ser versionado.
- Apenas dados sintéticos ou devidamente anonimizados permanecem no repositório.
- Datas sempre em ISO (`YYYY-MM-DD`).
- Textos codificados em UTF-8.
- Valores `enum` devem corresponder exatamente aos definidos no Notion.
