---
name: salve
description: >
  Flush de fim de sessão — captura tudo que aconteceu e atualiza o segundo cérebro.
  Percorre todas as áreas (pendências, decisões, pessoas, projetos, métricas, skills)
  e garante que nada se perde entre sessões. Sempre rodar antes de fechar.
  Triggers: "salve", "salva", "salva a sessão", "flush", "fecha a sessão".
---

# /salve

Flush completo de fim de sessão. Captura o contexto da conversa e persiste no segundo cérebro.

**Pré-requisito:** `$SECOND_BRAIN_PATH` configurado e repositório Git acessível.

---

## Passo 1 — Revisar a sessão (sem output)

Revisar mentalmente TUDO que aconteceu nesta conversa:
- Decisões tomadas
- Pendências criadas ou resolvidas
- Pessoas mencionadas (novas ou com role atualizado)
- Projetos com status alterado
- Métricas atualizadas
- Deadlines novos ou concluídos
- Skills criadas, editadas ou removidas
- Arquivos criados ou movidos
- Ideias mencionadas (conteúdo, produto, negócio)

---

## Passo 2 — Atualizar arquivos conforme PROPAGATION.md

Ler `$SECOND_BRAIN_PATH/PROPAGATION.md` e seguir a tabela completa.

Resumo rápido:

| Mudou? | Atualizar |
|--------|-----------|
| Pendência criada/resolvida | `memory/context/pendencias.md` |
| Decisão tomada | `memory/context/decisoes/YYYY-MM.md` |
| Decisão afeta negócio/equipe/foco | também `memory/context/business-context.md` |
| Pessoa nova ou role mudou | `memory/context/people.md` |
| Pessoa é da equipe principal | também `memory/context/business-context.md` |
| Projeto novo | `memory/projects/{nome}.md` + `memory/projects/_index.md` |
| Projeto mudou de status | `memory/projects/{nome}.md` + `_index.md` |
| Métrica atualizada | `memory/projects/{nome}.md` |
| Métrica-chave (MRR, usuários, receita) | também `memory/context/business-context.md` |
| Deadline novo ou concluído | `memory/context/deadlines.md` |
| Ideia mencionada | arquivo de ideias (crie onde fizer sentido) |

**Lembrete:** `business-context.md` é cache compilado — atualizar sempre que qualquer dado de negócio mudar. Em conflito, as fontes individuais prevalecem.

### Template para novo project file

Quando um projeto novo foi mencionado:

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

## Passo 3 — Criar/atualizar sessão do dia

Escrever em `$SECOND_BRAIN_PATH/memory/sessions/YYYY-MM-DD.md`:

```markdown
# Sessão — YYYY-MM-DD

## O que foi feito
- [lista de ações principais, 1 linha cada]

## Decisões
- [decisões tomadas, se houver]
- (omitir seção se não houve decisões)

## Em aberto
- [o que ficou pendente para a próxima sessão]
```

Se o arquivo já existir (outra sessão do dia), **adicionar** nova seção no final:

```markdown
## Sessão [HH:MM]

### O que foi feito
- ...

### Em aberto
- ...
```

---

## Passo 4 — Auditoria de propagação

Antes de commitar, verificar que TUDO da sessão foi propagado. Dois blocos:

### 4a — Checks estruturais (rápidos)

```bash
# Nenhum arquivo novo na raiz que deveria estar em subpasta?
ls "$SECOND_BRAIN_PATH"/*.md 2>/dev/null | grep -v "^$SECOND_BRAIN_PATH/CLAUDE.md\|PROPAGATION.md\|README.md\|MAPA.md"

# _index.md existe e lista os projetos ativos?
head -5 "$SECOND_BRAIN_PATH/memory/projects/_index.md" 2>/dev/null || echo "AVISO: _index.md não encontrado"

# Skills registry atualizado? (se existir)
test -f "$SECOND_BRAIN_PATH/skills/_registry.md" && head -3 "$SECOND_BRAIN_PATH/skills/_registry.md"
```

### 4b — Cruzamento de conteúdo

Revisar mentalmente cada item contra os arquivos atualizados:

| O que verificar | Contra o quê |
|-----------------|-------------|
| Decisões tomadas na sessão | Estão em `memory/context/decisoes/YYYY-MM.md`? |
| Pendências criadas/resolvidas | Estão em `memory/context/pendencias.md`? |
| Deadlines mencionados | Estão em `memory/context/deadlines.md`? |
| Projetos discutidos | `memory/projects/{nome}.md` reflete o estado atual? `_index.md` consistente? |
| Pessoas novas mencionadas | Estão em `memory/context/people.md`? |
| `business-context.md` | Está mais antigo que `decisoes/`? Se sim, atualizar cache |

Se encontrar inconsistência, corrigir ANTES de commitar.

---

## Passo 5 — Commit e push

```bash
cd "$SECOND_BRAIN_PATH"

# Recuperar estado quebrado (se houver)
[ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] && git rebase --abort 2>/dev/null
[ -f .git/MERGE_HEAD ] && git merge --abort 2>/dev/null

git add .
git commit -m "sessao: [resumo do que foi feito em 1 linha]"
git push origin main
```

Se o push falhar com "rejected":
```bash
# NUNCA usar rebase aqui — merge evita estados quebrados
git pull --no-rebase origin main
git push origin main
```

---

## Passo 6 — Confirmar

```
✓ Sessão salva — DD/MM/YYYY

Atualizado:
  [arquivo 1]
  [arquivo 2]
  ...

Não precisou atualizar:
  [categorias sem mudanças]

Pushed para origin/main.
```

---

## Regras

- **Nunca pular o Passo 2** — mesmo que pareça que nada mudou, revisar cada categoria
- **Nunca sobrescrever sessão existente** — se arquivo existe, adicionar seção no final
- **Commits específicos** — "sessao: reunião com cliente X + decisão sobre preço" > "sessao: updates"
- **Conflito no push** → sempre usar `pull --no-rebase` (merge), nunca `push --force` nem `pull --rebase` (rebase pode travar o repo)
- Tom direto no output, sem explicação desnecessária
