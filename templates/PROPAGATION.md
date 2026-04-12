# Propagação de Dados — Protocolo Único

> Este arquivo é a fonte de verdade sobre o que atualizar quando algo muda.
> Lido pelo Claude Code durante sessões e pelo /salve no fim de cada sessão.
> Quando a regra mudar, mude AQUI.

---

## Regra geral

**Toda ação que mude o estado de algo deve atualizar o arquivo correspondente no momento em que acontecer.** O /salve é o safety net — não o método principal.

---

## Tabela de Propagação

| Evento | Atualizar | O que escrever |
|--------|-----------|----------------|
| **Pendência criada ou resolvida** | `memory/context/pendencias.md` | Adicionar ou mover pra ✅ Resolvidas |
| **Decisão tomada** | `memory/context/decisoes/YYYY-MM.md` | Data, contexto, owner, status |
| | `memory/context/business-context.md` | SE mudou deal, equipe ou foco |
| **Pessoa nova ou role mudou** | `memory/context/people.md` | Adicionar ou atualizar entry |
| | `memory/context/business-context.md` | SE é equipe principal |
| **Projeto novo** | `memory/projects/{nome}.md` | Criar com template |
| | `memory/projects/_index.md` | Adicionar na seção correta |
| | `memory/context/business-context.md` | SE é negócio principal |
| **Projeto mudou de status** | `memory/projects/{nome}.md` | Atualizar status |
| | `memory/projects/_index.md` | Atualizar status na tabela |
| **Métrica atualizada** | `memory/projects/{nome}.md` | Atualizar tabela de métricas |
| | `memory/context/business-context.md` | SE é métrica-chave |
| **Deadline novo ou concluído** | `memory/context/deadlines.md` | Adicionar ou mover pra concluídos |
| **Ideia registrada** | arquivo de ideias (crie onde fizer sentido) | Adicionar com data |

---

## Fontes de Verdade

| Dado | Fonte principal | Cache/overview |
|------|-----------------|----------------|
| Status de projeto | `memory/projects/{nome}.md` | `_index.md`, `business-context.md` |
| Decisões | `memory/context/decisoes/YYYY-MM.md` | `business-context.md` |
| Pessoas/equipe | `memory/context/people.md` | `business-context.md` |
| Pendências | `memory/context/pendencias.md` | — |
| Deadlines | `memory/context/deadlines.md` | — |
| Panorama geral | `memory/context/business-context.md` | (é o próprio overview compilado) |

`business-context.md` é um **cache compilado**. Em caso de conflito, as fontes individuais prevalecem.

---

## Template — Novo Project File

```markdown
# [Nome do Projeto]

> Status: [emoji + status]

## O que é
[1-2 frases]

## Responsáveis
- **[Nome]:** [role]

## Timeline
| Data | Evento |
|------|--------|
| [data] | Projeto criado |

## Decisões Tomadas
- [DD/MM/YYYY] [decisão]

## Pendências
- [ ] [próxima ação]

---
*Criado: DD/MM/YYYY*
```

---

*Criado: [data de setup]*
