# Diário BRH

Registros de práticas individuais organizados por data no formato `YYYY-MM-DD-sessao-NN`.

## Convenção

- **YYYY-MM-DD** — data da prática.
- **sessao-NN** — número sequencial do registro no dia.
- Para cada data mantemos normalmente:
  - um arquivo `.md` com o registro detalhado;
  - anexos relevantes (imagens, PDFs, biofeedback).

## Último registro

- **Data:** 2025-09-26 • **Sessão:** 01
- MD: [2025-09-26-sessao-01.md](/analysis/reports/diarios/2025-09-26-sessao-01.md)
- PDF: [2025-09-26-sessao-01.pdf](/analysis/reports/diarios/2025-09-26-sessao-01.pdf)
- Print: [2025-09-26-sessao-01-garmin.png](/analysis/reports/diarios/2025-09-26-sessao-01-garmin.png)

## Como adicionar novos registros

1. Criar arquivos seguindo a convenção acima dentro desta pasta.
2. Referenciar anexos na seção **Anexos** do `.md` correspondente.
3. Executar `make diarios-index` para atualizar o índice e este README.

### Padronização dos dados de sono (JSON)

- Registros objetivos devem ser salvos como `YYYY-MM-DD-dados.json` seguindo o schema `schema/sleep-entry.schema.json`.
- Para validar rapidamente todos os arquivos utilizamos `tools/validate_sleep_reports.py`:

  ```bash
  # ambiente raiz de /institute
  tools/validate_sleep_reports.py
  # ou especificando outro diretório/glob
  tools/validate_sleep_reports.py --glob 'analysis/reports/diarios/2025-*-dados.json'
  ```
- O schema define campos obrigatórios (ex.: `total_sleep_h`, `spo2_min_pct`, `resp_rate_avg_brpm`), limites e listas opcionais (`notes`, `awakenings`).
- Campos adicionais podem ser acomodados em `measurements` para manter a padronização.

### 2025-09-26 — Sexta-feira (Folga Consciente)

- **Body Battery final:** 30
- **Resumo:** Dia intenso em decisões de salvaguardas e missão. Sensação de “cansaço bom”, semelhante a pós-prática vibracional.  
- **Insight:** “Folgar é deixar o Campo reorganizar. Se a inspiração vier, recebo sem cobrança. Se vier o silêncio, celebro a pausa.”
- **Arquivo:** [2025-09-26-sexta-feira.pdf](2025-09-26-sexta-feira.pdf)

### 2025-09-27 — Sábado (Recarga Autônoma)

- **Body Battery atual:** 39/100 (carga +70 / drenagem −51).
- **Resumo:** Folga com cochilos leves; picos de estresse emocionais entre manhã e tarde sincronizados com queda da bateria.
- **Leituras:** FC repouso 56 bpm (pico 117 bpm); SpO₂ média 93% com janelas noturnas de 80–89%. Sono prévio de ~4h54 com REM reduzido.
- **Plano noturno:** NSDR/respiração 4-6, higiene nasal + decúbito lateral, corte de telas 60–90 min antes, aferir SpO₂ sentada.  
- **Arquivos:** [2025-09-27-relatorio.md](2025-09-27-relatorio.md), [2025-09-27-resumo-diario.pdf](2025-09-27-resumo-diario.pdf), [2025-09-27-diario.pdf](2025-09-27-diario.pdf), [2025-09-27-diario-do-sono.pdf](2025-09-27-diario-do-sono.pdf), [2025-09-27-sono.csv](2025-09-27-sono.csv)

### 2025-09-28 — Domingo (Monitoramento Físico)

- **Body Battery ao meio-dia:** 47/100 (carga noturna +57).
- **Resumo:** Recuperação tranquila; observação de alterações em unhas/cutículas e parestesia na mão esquerda.
- **Leituras:** Sono 7h49 (profundo 1h20; REM 1h08; leve 5h21); FC repouso 57 bpm; SpO₂ média 92% (mín. 81%).
- **Plano:** Registrar sintomas, manter respirações longas, agendar avaliação médica para oxigenação e sensibilidade das mãos.
- **Arquivos:** [2025-09-28-diario.md](2025-09-28-diario.md), [2025-09-28-diario.pdf](2025-09-28-diario.pdf), [2025-09-28-resumo-diario.pdf](2025-09-28-resumo-diario.pdf), [2025-09-28-diario-do-sono.pdf](2025-09-28-diario-do-sono.pdf), [2025-09-28-sono.csv](2025-09-28-sono.csv)

### 2025-09-29 — Segunda-feira (Sono Curto)

- **Body Battery ao meio-dia:** 47/100 (recarga +53).
- **Resumo:** Noite curta (6h32) com SpO₂ mínima 73%; foco em autorregulação suave e acompanhamento de sinais físicos.
- **Leituras:** Sono profundo 1h22; leve 4h51; REM 19min; FC repouso 56 bpm; SpO₂ média 90%; respiração média 15 brpm.
- **Plano:** Registrar sintomas, manter respirações 4-6, preparar consulta para avaliação respiratória/vascular das mãos.
- **Arquivos:** [2025-09-29-diario.md](2025-09-29-diario.md), [2025-09-29-diario.pdf](2025-09-29-diario.pdf), [2025-09-29-resumo-diario.pdf](2025-09-29-resumo-diario.pdf), [2025-09-29-sono.pdf](2025-09-29-sono.pdf), [2025-09-29-sono.csv](2025-09-29-sono.csv)
