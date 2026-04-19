---
name: skill-audit
description: >
  Audits a Claude Code / Agent SDK skill (or folder of skills) against 10 QA
  checks to verify it will trigger and execute correctly in any LLM (Claude,
  GPT, Gemini). Ativa quando o usuário diz "audit my skill", "roda skill-audit",
  "verifica se essa skill funciona", "check skill quality", "skill-audit ./my-skill",
  "minha skill não dispara", "migrei do Claude antigo e quebrou", ou colar path
  de um SKILL.md. Retorna score 0-10 por skill, issues priorizados, e sugestões
  de conserto. NÃO use para: criar uma skill nova do zero (use `criar-skill`
  ou `skill-creator`); executar a skill alvo; refatorar código genérico.
type: skill
category: meta
status: ATIVO
version: 1.0
created: 2026-04-19
last_reviewed: 2026-04-19
estimated_time: 2min
model_compatible: [claude-sonnet-4, claude-opus-4, gpt-5, gpt-4o, gemini-pro]
---

# skill-audit

Auditoria estática de `SKILL.md` contra o padrão V3 (LLM-friendly). Roda 10 QA
checks, detecta issues mecânicos e semânticos, entrega report priorizado. Útil
especialmente pra quem migrou de Claude pre-4.5 — skills antigas costumam
funcionar só no contexto do autor, não em agentes externos.

---

## When to Use

Aciona quando:
- Usuário tem uma skill que "não dispara" ou "não executa direito"
- Migrou de Claude 3.x / 4.0 pra 4.6+ e viu comportamento quebrado
- Quer rodar a skill em GPT-5, Gemini, ou outro LLM que não seja Claude
- Está criando skills em massa (ex: para alunos, time, comunidade)
- Quer priorizar quais skills da coleção conserta primeiro

Exemplos literais de mensagens:
- "roda skill-audit em skills/my-skill/SKILL.md"
- "minha skill não dispara no GPT"
- "audita essa pasta de skills pra mim"
- "skill-audit ./skills"
- "por que essa skill funciona no Claude mas não no Gemini?"

## When NOT to Use

NÃO aciona se:
- Usuário quer CRIAR uma skill do zero → usar `criar-skill` ou `skill-creator`
- Usuário quer EXECUTAR a skill auditada → rodar a skill diretamente
- Usuário quer auditoria de segurança (OWASP, secrets em produção) → outra ferramenta
- Arquivo alvo não é `SKILL.md` (ex: script Python, README) → refatoração genérica

---

## Inputs

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| path | string | ✅ | Path de um `SKILL.md` OU pasta contendo subpastas com `SKILL.md` (recursivo) |
| format | string | ❌ | `markdown` (default) ou `json` — formato do report |

## Outputs

| Campo | Tipo | Descrição |
|-------|------|-----------|
| score | int 0-10 | Quantos dos 10 QA checks a skill passa |
| issues | array | Lista priorizada de problemas (ex: `desc_no_triggers`, `examples_too_few`) |
| by_category | object | Score médio e passing rate por categoria de skill |
| report | markdown | Report completo com ranking + detalhamento por skill |

Formato de entrega: arquivo markdown em `./audit-results.md` + resumo no terminal.

---

## Workflow

1. **Validar input** — path existe? É arquivo `.md` ou diretório?
2. **Coletar SKILL.md files**
   - SE path aponta pra arquivo `.md` → lista única
   - SENÃO → `glob **/SKILL.md` recursivo no diretório
3. **Para cada SKILL.md:**
   - Parsear frontmatter YAML (`---` ... `---`)
   - Split do body em seções H2 (ignorando H2 dentro de code fences ``` ou ~~~)
   - Rodar os 10 QA checks
   - Registrar score + issues + contagens
4. **Agregar resultados** — score médio, distribuição, issues mais comuns
5. **Gerar report markdown** em `./audit-results.md` com:
   - Sumário global
   - Distribuição de scores
   - Issues por frequência
   - Top 30 skills que mais precisam conserto
   - Detalhamento por skill
6. **Imprimir resumo no terminal** — total, score médio, passing ≥7

### Os 10 QA checks

1. Nome em kebab-case e bate com pasta
2. Description: 50+ palavras, terceira pessoa, 5+ trigger phrases, negative boundaries
3. Cada passo do Workflow é ação única, imperativa, não-ambígua
4. 2+ exemplos concretos (input real → output real)
5. Edge Cases cobertos (3+ condições)
6. Output Format explicitamente definido
7. Zero linguagem vaga (lista de palavras banidas em `references/qa-checklist.md`)
8. Negative boundaries na seção `## When NOT to Use`
9. Zero credenciais hardcoded (secrets, API keys, tokens)
10. Pasta `evals/evals.json` existe com 2+ casos

---

## Edge Cases

- **Se path não existe** → exit 1 com mensagem "Path não encontrado: {path}"
- **Se diretório vazio (0 SKILL.md)** → exit 0 com mensagem "Nenhum SKILL.md encontrado em {path}"
- **Se SKILL.md sem frontmatter YAML** → score 0, issue `missing_frontmatter`
- **Se YAML inválido** → score 0, issue `yaml_parse_error`
- **Se pasta `evals/` existe mas sem `evals.json`** → issue `no_evals_folder`
- **Se SKILL.md muito grande (>350 linhas)** → warning `long`, sugere mover conteúdo para `references/`
- **Se placeholder ref (`link`, `url`, `path`) em markdown link** → ignorado (não conta como broken ref)

---

## Examples

### Example 1 — Auditar uma skill única

**Input real:** `skill-audit ./my-skill/SKILL.md`

**Workflow executado:**
1. Valida que `./my-skill/SKILL.md` existe
2. Parseia YAML — encontra `name: my-skill`, description de 32 palavras
3. Body split: tem `## When to Use`, falta `## When NOT to Use`
4. Roda 10 checks: description short (32w<50), no negatives, no evals folder, só 1 Example
5. Gera report

**Output real:**
```
skill-audit: 1 skill analisada
  my-skill — 6/10 (232L, 32w desc, 4 triggers, 1 ex, 4 edge, evals ✗)
  Issues: desc_too_short(32w), desc_no_negatives, examples_too_few(1), no_evals_folder

Report: ./audit-results.md
```

### Example 2 — Auditar pasta inteira (edge: várias skills)

**Input real:** `skill-audit ~/my-claude-skills/`

**Workflow executado:**
1. Valida que `~/my-claude-skills/` é diretório
2. Glob encontra 12 `SKILL.md`
3. Para cada: parseia + checks + score
4. Agrega: score médio 7.1, 4/12 passing ≥7
5. Report priorizado: pior primeiro

**Output real:**
```
skill-audit: 12 skills analisadas
  Score médio: 7.1/10
  Passing (≥7): 4/12 (33%)

Top 3 issues mais comuns:
  desc_no_negatives (12, 100%)
  no_evals_folder (9, 75%)
  desc_too_short (7, 58%)

Worst offenders:
  1. legacy-skill-x — 3/10
  2. migrated-from-gpt — 4/10
  3. old-claude35-skill — 5/10

Report: ./audit-results.md
```

---

## Dependencies

- **Runtime:** Python 3.8+
- **Libs:** stdlib only (re, json, pathlib, argparse, collections)
- **APIs:** nenhuma — 100% estático/offline
- **Files:** `templates/SKILL-TEMPLATE.md` + `references/qa-checklist.md` (read-only)
- **Outras skills:** nenhuma — ferramenta standalone

---

## Errors & Recovery

| Erro | Causa provável | Fix |
|------|----------------|-----|
| `Path não encontrado` | Path inválido ou digitado errado | Verificar path absoluto; usar `ls {path}` pra confirmar |
| `yaml.YAMLError` | Frontmatter mal formado | Abrir SKILL.md, verificar indentação e fechamento `---` |
| `UnicodeDecodeError` | SKILL.md em encoding não-UTF8 | Salvar como UTF-8 no editor |
| `ModuleNotFoundError: yaml` | PyYAML ausente | `pip3 install pyyaml` |
| Report não gerado | Permissão de escrita em `./audit-results.md` | Rodar de diretório com permissão de escrita |

---

## Notes

**Sobre o score:** 7/10 é o mínimo aceitável pra considerar uma skill "trigger-confiável"
em LLMs externos. 10/10 é ideal. Abaixo de 7 geralmente significa que a skill foi
escrita em prosa livre e não em contrato executável — formato comum em skills pre-V3.

**Sobre evals.json:** o check 10 não valida conteúdo dos evals, só presença do arquivo
e estrutura mínima (2+ casos com `prompt` e `expected_output`). Qualidade dos evals é
trabalho do autor da skill, não do audit.

**Limitações conhecidas:**
- Não audita qualidade semântica do workflow (se os passos fazem sentido pro domínio)
- Não executa a skill (só análise estática)
- Heurísticas de trigger phrase podem dar falso positivo em descriptions técnicas
  densas — revisar issues manualmente quando score for borderline (6-7)

---

## Changelog

- v1.0 (2026-04-19): Versão inicial. 10 QA checks baseados no padrão V3.
  Deriva de auditoria em 119 skills do workspace Amora (score médio 5.9 → 10.0).
