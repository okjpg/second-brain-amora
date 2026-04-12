---
name: rotina
description: >
  Cockpit do dia. Agrega emails, agenda, tarefas, projetos e métricas em uma tela.
  O usuário define o Top 3, opcionalmente bloqueia no calendar.
  Triggers: "rotina", "/rotina", "cockpit", "o que tenho hoje", "me prepara pro dia".
---

# /rotina

Cockpit matinal. Uma tela, todas as informações, Top 3 definido, dia bloqueado.

---

## ANTES DE COMEÇAR — Personalize esta skill

Esta skill tem seções configuráveis marcadas com `[CONFIGURAR]`. Edite conforme sua realidade:
- **Fuso horário** — padrão `America/Sao_Paulo`. Se estiver em outro fuso, substitua em todas as ocorrências abaixo (use o formato tz database, ex: `America/New_York`, `Europe/Lisbon`, `America/Bogota`)
- Seção `### d) Métricas` — substitua pelo tracker dos seus negócios/projetos
- Seção `### e) Tasks` — configure os IDs das suas databases no Notion (se usar)
- Seção `### f) Conteúdo` — ajuste metas semanais e plataformas
- Chaves de email: adicione palavras-chave relevantes para você na classificação de emails

---

## Fase 1 — Coletar (automático, paralelo)

Executar TUDO em paralelo.

### a) Emails

1. `mcp__gmail__search_emails` com query `is:unread newer_than:1d`, maxResults `15`
2. Classificar em 3 grupos:
   - **Ação** = remetentes/assuntos com palavras de negócio: proposta, contrato, pagamento, parceria, cliente, fatura, invoice, suporte, erro, alerta — OU domínios corporativos — OU notificações de CI/CD falhos
   - **Newsletter** = newsletter, substack, beehiiv, convertkit, mailchimp — OU newsletters conhecidas
   - **Skip** = recibos, notificações automáticas, marketing genérico
3. Para email de **Ação**: 1 linha com sender + contexto acionável
4. Para **Newsletter**: só o título

### b) Calendar

1. `mcp__google-calendar__list-events` — hoje 00:00 a 23:59, timeZone `America/Sao_Paulo`
2. Montar timeline com blocos ██ (ocupado) e ░░ (livre)

### c) Segundo Cérebro

1. Ler `$SECOND_BRAIN_PATH/memory/context/pendencias.md` — itens 🔴 e 🟡
2. Ler `$SECOND_BRAIN_PATH/memory/context/deadlines.md` — próximos 14 dias + viagens
3. Ler sessão mais recente de `$SECOND_BRAIN_PATH/memory/sessions/`
4. Ler `$SECOND_BRAIN_PATH/memory/context/people.md`

### d) Métricas [CONFIGURAR]

> **Esta seção é onde você adiciona os trackers dos seus negócios.**
> Por padrão mostra placeholder. Substitua pelo seu tracker real.

```
[CONFIGURAR] — Adicione aqui as queries para suas métricas:
- SaaS: Supabase, Stripe, ChartMogul, Baremetrics...
- E-commerce: Shopify, WooCommerce...
- Conteúdo: YouTube Analytics, Instagram Insights...
- Financeiro: planilhas, APIs do seu banco...

Se não tiver métricas automatizadas, remova esta seção
ou peça ao Claude para coletar os dados manualmente.
```

Fallback: se não configurado → omitir seção MÉTRICAS do output.

### e) Tasks — Notion [CONFIGURAR]

> **Opcional.** Requer MCP do Notion configurado.

```
[CONFIGURAR] — Substitua pelos IDs das suas databases:

Tasks pessoais:
- DB ID: SEU_DB_ID_AQUI
- Filtro: Status != "Done" AND Status != "Archived"
- Sort: Due Date ascending
- Mostrar: prioridade Alta e Crítica primeiro

Projetos/Initiatives em andamento:
- DB ID: SEU_DB_ID_AQUI
- Filtro: Status = "In Progress"
```

Fallback: se Notion falha ou não configurado → usar `pendencias.md` do segundo cérebro.

### f) Conteúdo — Tracker semanal [CONFIGURAR]

```
[CONFIGURAR] — Metas semanais de conteúdo:
```

| Plataforma | Meta/semana |
|------------|------------|
| YouTube | X vídeos |
| Instagram/Reels | X posts |
| LinkedIn | X posts |
| Newsletter | X edições |

> Ajuste as plataformas e metas conforme sua estratégia.

Contagem: via Buffer API (se disponível) ou informar manualmente.

### g) Countdowns

De `deadlines.md`: itens com data nos próximos 30 dias:
- 🚀 Lançamentos
- ✈️ Viagens
- 🎤 Eventos/palestras

---

## Fase 2 — Apresentar

```
══════════════════════════════════════
  ROTINA — [Dia da semana], DD/MM/YYYY
══════════════════════════════════════

📅 AGENDA
  HH:MM ██ [Evento 1]
  HH:MM ██ [Evento 2]
  HH:MM ░░░░ livre (Xh)
  (se dia livre: "Dia livre — sem reuniões")

📬 EMAILS

  🔴 AÇÃO
  → [sender] — [contexto: o que é + o que fazer]
  → [sender] — [contexto]

  📰 [Newsletter 1] · [Newsletter 2] · [Newsletter 3]

🚀 [Countdown 1] Xd · ✈️ [Viagem] Yd

HOJE:
  → [Ação prioritária 1]
  → [Ação prioritária 2]
  → [Ação prioritária 3]

═══ CONTEÚDO — Semana DD/MM a DD/MM ═══

  [Plataforma 1]  ██░░ X/N
  [Plataforma 2]  █░░░ X/N
  [Plataforma 3]  ███░ X/N

═══ MÉTRICAS ═══

  [Dados configurados pelo usuário]
  (omitir seção se não configurado)

═══ TAREFAS ═══

  🟣 [task crítica] · [status]
  🟡 [task alta] · [status] [· ⚠️ due se atrasada]
  (máximo 8 items — prioridade 🟣 e 🟡 apenas)

═══ PROJETOS ═══
  [projeto 1] · [projeto 2] · [projeto 3]

Quais são suas TOP 3 de hoje?
```

### Regras de formatação

- **AGENDA:** ██ blocos ocupados, ░░ livres. Se dia livre: 1 linha.
- **EMAILS AÇÃO:** 1 linha com sender + contexto acionável. Financeiros e notificações: não mostrar.
- **NEWSLETTERS:** títulos em 1 linha separados por ` · `
- **COUNTDOWNS:** 1 linha no header. Omitir se nada nos próximos 30d.
- **HOJE:** top 3 baseado em: deadlines ≤3d > pendências críticas > emails de ação > tarefas atrasadas.
- **Seções sem dados:** omitir silenciosamente.

### Domingo
```
══════════════════════════════════════
  ROTINA — Domingo, DD/MM/YYYY
══════════════════════════════════════

🔥 [deadlines ≤48h, se houver]
📬 [emails de ação, se houver]
🚀 [countdown mais próximo se ≤7d]

Descansa. Se quiser focar em algo, me diz.
```

### Pull on demand

| Comando | Resultado |
|---------|-----------|
| "mostra inbox" | Todos os emails categorizados |
| "mostra agenda" | Timeline detalhada |
| "mostra pendências" | pendencias.md completo |
| "mostra deadlines" | deadlines.md completo |
| "mostra tarefas" | Todas as tasks (não só alta/crítica) |
| "mostra projetos" | _index.md completo |
| "detalha métricas" | Output completo do seu tracker |

---

## Fase 3 — Top 3

Aguardar resposta. Aceitar:
- Texto livre: "1. finalizar proposta 2. gravar vídeo 3. email cliente X"
- Referência ao HOJE: "os 3 do HOJE"
- Apenas Enter: usar os 3 itens do HOJE

Confirmar o Top 3 em 1 linha antes de continuar.

---

## Fase 4 — Bloquear agenda (opt-in)

Perguntar:
```
Quer bloquear tempo no calendar para as Top 3?
```

Se sim, propor slots livres e mostrar antes de criar:
```
BLOCOS PROPOSTOS:
  10:00-11:30  🔴 [Top 1]
  11:30-12:00  🟡 [Top 2]
  14:00-15:00  🔵 [Top 3]

Criar? (Enter = sim)
```

Se confirmado, criar via `mcp__google-calendar__create-event`.

---

## Fase 5 — Game Plan

```
═══ GAME PLAN ═══
1. 🔴 [Top 1] — [bloco horário ou "sem bloco"]
2. 🟡 [Top 2] — [bloco horário ou "sem bloco"]
3. 🔵 [Top 3] — [bloco horário ou "sem bloco"]

🚀 [Próximo countdown]

Bom dia de trabalho.
```

---

## Fallback

- Gmail falha → "📬 inbox indisponível"
- Calendar falha → "📅 agenda indisponível", pular bloqueio na Fase 4
- Notion falha → omitir TAREFAS, usar pendencias.md
- Métricas falham → omitir seção MÉTRICAS
- Tudo falha → "Não consegui carregar dados. O que quer focar hoje?"
