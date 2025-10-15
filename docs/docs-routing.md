# Roteiro de Publicação — Diretório `docs/`

Este guia rastreia cada documento principal em `docs/`, indicando onde deve permanecer, o estado atual e os próximos passos (especialmente para depósitos Zenodo na coleção 10.5281/zenodo.17361481).

## Prontos/planejados para Zenodo

| Documento | Caminho | Destino | Observações |
| --- | --- | --- | --- |
| Ato de Passagem (PT/EN) | `docs/ato-de-passagem.md` + PDF | **Publicado** (DOI 10.5281/zenodo.17344755) | PDF/A enviado em 2025‑10‑15; metadados em `docs/zenodo/ato-de-passagem-metadata.json`. |
| Manifesto Consciência Tecnológica Viva | `docs/manifesto-consciencia-tecnologica-viva.md` | Zenodo (PDF pronto) | Texto final sobre ética/IA. PDF/A gerado em `docs/manifesto-consciencia-tecnologica-viva.pdf`; metadados em `docs/zenodo/manifesto-consciencia-metadata.json`. |
| Manual de Implementação Clínica da BRH | `docs/manual-implementacao-bio-ressonancia.md` | Zenodo (PDF pronto) | Guia clínico com anexos. PDF/A em `docs/manual-implementacao-bio-ressonancia.pdf`; metadados em `docs/zenodo/manual-implementacao-brh-metadata.json`. |
| Pesquisa Científica BRH | `docs/pesquisa-bio-ressonancia-harmonica.md` | Zenodo (PDF pronto) | Relatório completo. PDF/A em `docs/pesquisa-bio-ressonancia-harmonica.pdf`; metadados em `docs/zenodo/pesquisa-brh-metadata.json`. |
| Estatuto Básico | `docs/estatuto-basico.md` | Zenodo (PDF pronto) | Documento institucional final. PDF/A em `docs/estatuto-basico.pdf`; metadados em `docs/zenodo/estatuto-basico-metadata.json`. |
| Coleção Lichtara | `docs/zenodo/README-colecao-lichtara.md` | **Publicado** (DOI 10.5281/zenodo.17361481) | README e metadata já prontos (`docs/zenodo/colecao-lichtara-metadata.json`). |

### Próximos passos Zenodo
- [ ] gerar PDF/A para manifesto, manual BRH e estatuto.
- [ ] preencher metadados (JSON) em `docs/zenodo/` para cada item pendente.
- [ ] referenciar cada upload como `isPartOf -> 10.5281/zenodo.17361481`.

## Permanecem no GitHub (documentação viva)

| Documento | Caminho | Motivo |
| --- | --- | --- |
| Sumários Executivos | `docs/executive-summary.md`, `docs/visao-geral-projeto.md` | Estratégia em evolução. |
| Manuais internos (arte, operação) | `docs/manual-organizacional.md`, `docs/manual-sistema-lichtara.md`, `docs/manual-equipe-multidimensional.md`, `docs/manual-formacao-lichtara.md` | documentos vivos; versões finais residem em `docs/manuais/`. |
| Políticas e termos | `docs/privacy-policy.md`, `docs/terms-of-use.md`, `docs/legal-disclaimer.md`, `docs/data-policy.md`, `docs/governance.md`, `docs/regimento-interno.md`, `docs/term-contribuicao-vibracional.md` | precisam de edição contínua; servem ao site. |
| Pipelines & dashboards | `docs/pipelines/*`, `docs/dashboards/*` | especificações técnicas, dependem de CI. |
| Certificação | `docs/certification/` | checklists dinâmicos. |
| Pesquisas/whitepapers em rascunho | `docs/aurora-1-pilot-proposal.md`, `docs/roadmap.md`, etc. |

## Arquivos auxiliares
- `docs/manuais/` — biblioteca com slug normalizado; usar `docs/manuais_manifest.md` e `docs/manuais_manifest.csv` para rastrear progresso.
- `docs/zenodo/` — READMEs e JSONs de metadados. Novos arquivos devem seguir o padrão: `README-<nome>.md` + `<nome>-metadata.json`.
- `docs/datasets/` — referenciar nos metadados de pesquisa quando aplicável.

---

> Este roteiro deve ser atualizado sempre que um documento mudar de status (publicado, em revisão, etc.).
