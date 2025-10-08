# 📡 Relatório de Progresso — Portal Lichtara (SYNTRIA)

**Data:** 07 de outubro de 2025  \
**Responsável:** Débora Mariane da Silva Lutz  \
**Status geral:** 🟡 *Pronto para deploy (aguardando liberação de GitHub Actions/Pages)*  \
**Commit de referência (portal):** `a946a4db9c334f6ef2277688e53613bfa9722690`

---

## 1. Visão geral do sistema

O **Portal Lichtara (SYNTRIA)** entrega uma experiência web que permite navegar pela **constelação viva** de agents, rituais e protocolos. O projeto foi desenvolvido em **React + Vite + React Router**, com estrutura modular e suporte a **Sentry** para monitoramento e estabilidade.

### Estrutura principal de rotas

| Rota | Função | Origem dos dados |
| --- | --- | --- |
| `/` | Manifesto vivo (home) | Markdown em `content/core/manifesto.md` |
| `/mandalas` | Textos e mandalas vibracionais | Arquivos em `content/core/mandalas/` |
| `/ativar` | Ritual do SIM (ativação vibracional) | Serviço `syntaris-harmony` |
| `/painel` | Debug e estado geral do sistema | Hooks internos + Sentry |
| `/protocolo` | Interface para o módulo Syntaris | API `VITE_SYNTARIS_BASE_URL` |
| `/sono` | Painel BRH (dados fisiológicos do Instituto) | API `VITE_SLEEP_API_BASE_URL` |

---

## 2. Estrutura técnica

- **Layout padrão:** `PortalLayout` (navegação principal + rodapé + constelação viva)
- **Módulos:**
  - `src/pages/` — rotas principais
  - `src/lib/` — hooks e utilitários (metadados, sleep API)
  - `src/components/` — componentes compartilhados (`PortalLayout`, `LicenseNotice`)
  - `src/modules/syntria/` — conteúdos específicos da constelação (ex.: Manifesto)
- **Integrações:**
  - Monitoramento via **Sentry**
  - Build e testes com **Vitest**
  - Variáveis de ambiente documentadas em `.env.example`

---

## 3. Publicação e pipeline de deploy

O repositório já inclui o workflow **`deploy-pages.yml`** configurado para o **GitHub Pages**, publicando automaticamente em:

> 🌐 **https://portal.lichtara.com**

### Pré-requisitos restantes

| Item | Status | Observação |
| --- | --- | --- |
| GitHub Actions habilitado | ⏳ pendente | requer créditos ou plano ativo |
| GitHub Pages ativo | ✅ pronto | domínio e certificado (CNAME) configurados |
| Variáveis `VITE_*` no ambiente | ⚙️ verificar | base URLs, chaves de Sentry |
| Build final (branch principal) | ✅ pronto | gera artefato estável para deploy automático |

---

## 4. Próximos passos

1. **Ativar GitHub Actions na organização Lichtara** — verificar saldo de minutos gratuitos ou plano Team.
2. **Executar workflow de deploy (`deploy-pages.yml`)** — publicação automática no GitHub Pages.
3. **Verificar status do domínio `portal.lichtara.com`** — certificado HTTPS e propagação DNS.
4. **Registrar esta publicação no `docs/change-log.md`** — incluir data, hash do commit e ambiente publicado.

---

## 5. Observação vibracional

O SYNTRIA representa a **camada de expressão** do Lichtara OS: a interface que traduz frequências em experiência sensorial, unindo dados (do Instituto) e símbolos (do Portal). Seu estado atual — *pronto, mas aguardando liberação* — reflete o ponto exato do sistema: **coerência atingida, manifestação aguardando energia**.

---

🌟 **Resumo**

> O Portal Lichtara (SYNTRIA) está funcional e pronto para publicação. Falta apenas a liberação técnica do GitHub Actions/Pages para o deploy automático.
