---
name: diagnostico
description: >
  Raio-X do segundo cérebro — audita estrutura, git, invariantes, frescor,
  volume e coerência das skills. Somente leitura, nunca modifica.
  Rodar semanalmente ou quando sentir que algo está estranho.
  Triggers: "diagnostico", "/diagnostico", "raio-x do cérebro", "auditar cérebro", "saúde do cérebro".
---

# /diagnostico

Auditoria do segundo cérebro em 6 camadas. Read-only.

**Pré-requisito:** `$SECOND_BRAIN_PATH` configurado.

**Regras:**
- Nunca modifica arquivos.
- Se um check precisa de dados reais e o brain está virgem (placeholders), degrada pra "N/A — brain em setup".
- Thresholds padrão: crítico 🔴, atenção 🟡, ok 🟢.

---

## Passo 0 — Sanity check

```bash
if [ -z "$SECOND_BRAIN_PATH" ] || [ ! -d "$SECOND_BRAIN_PATH" ]; then
  echo "🔴 SECOND_BRAIN_PATH inválido ou pasta inexistente. Abortando."
  exit 1
fi
BRAIN="$SECOND_BRAIN_PATH"

# Detectar se brain é virgem (só placeholders)
PRISTINE=false
if grep -q "\[SEU NOME\]\|\[Projeto 1\]\|\[Nome\]" "$BRAIN/CLAUDE.md" "$BRAIN/memory/context/business-context.md" 2>/dev/null; then
  PRISTINE=true
fi
```

Se `PRISTINE=true`, incluir no output final: "⚠ Brain ainda tem placeholders não preenchidos — alguns checks foram degradados."

---

## Camada 1 — Estrutura

```bash
echo ""
echo "=== CAMADA 1 — ESTRUTURA ==="
REQUIRED=(
  "CLAUDE.md"
  "PROPAGATION.md"
  "MAPA.md"
  "memory/context/pendencias.md"
  "memory/context/deadlines.md"
  "memory/context/business-context.md"
  "memory/context/people.md"
  "memory/projects/_index.md"
)
MISSING=0
for f in "${REQUIRED[@]}"; do
  if [ ! -f "$BRAIN/$f" ]; then
    echo "🔴 AUSENTE: $f"
    MISSING=$((MISSING+1))
  fi
done
[ "$MISSING" -eq 0 ] && echo "🟢 ${#REQUIRED[@]}/${#REQUIRED[@]} arquivos obrigatórios presentes"

# Decisão do mês corrente
MES=$(date +%Y-%m)
if [ ! -f "$BRAIN/memory/context/decisoes/$MES.md" ]; then
  echo "🟡 decisoes/$MES.md não existe (será criado na primeira decisão do mês)"
fi
```

---

## Camada 2 — Git (do próprio brain)

```bash
echo ""
echo "=== CAMADA 2 — GIT ==="
if [ ! -d "$BRAIN/.git" ]; then
  echo "🟡 Brain não é repo git — sem backup automático"
else
  cd "$BRAIN"
  # Estado quebrado
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    echo "🔴 Rebase em progresso — rodar 'git rebase --abort'"
  fi
  if [ -f .git/MERGE_HEAD ]; then
    echo "🔴 Merge em progresso — rodar 'git merge --abort'"
  fi
  # Working tree
  if ! git diff --quiet || ! git diff --cached --quiet; then
    DIRTY=$(git status --short | wc -l | tr -d ' ')
    echo "🟡 $DIRTY arquivo(s) não-commitados"
  fi
  # Unpushed
  BRANCH=$(git rev-parse --abbrev-ref HEAD)
  REMOTE=$(git remote | head -1)
  if [ -n "$REMOTE" ]; then
    UNPUSHED=$(git rev-list --count "$REMOTE/$BRANCH..HEAD" 2>/dev/null || echo "?")
    if [ "$UNPUSHED" != "?" ] && [ "$UNPUSHED" -gt 0 ]; then
      echo "🟡 $UNPUSHED commit(s) não-pushados"
    fi
    # Remote alcançável
    if ! timeout 5 git ls-remote "$REMOTE" HEAD >/dev/null 2>&1; then
      echo "🔴 Remote '$REMOTE' inalcançável (rede/auth)"
    fi
    # Último push (warn se > 7d)
    LAST_PUSH=$(git log "$REMOTE/$BRANCH" -1 --format=%ct 2>/dev/null || echo 0)
    NOW=$(date +%s)
    DAYS=$(( (NOW - LAST_PUSH) / 86400 ))
    if [ "$DAYS" -gt 7 ] && [ "$LAST_PUSH" -gt 0 ]; then
      echo "🟡 Último push há ${DAYS}d (backup desatualizado)"
    fi
  else
    echo "🟡 Sem remote configurado — sem backup remoto"
  fi
  [ "$MISSING" -eq 0 ] && [ -z "$UNPUSHED" -o "$UNPUSHED" = "0" ] && echo "🟢 Git saudável"
fi
```

---

## Camada 3 — Invariantes cruzadas

Roda só se `PRISTINE=false`. Caso contrário: "N/A — brain ainda em setup".

```bash
echo ""
echo "=== CAMADA 3 — INVARIANTES ==="
if [ "$PRISTINE" = "true" ]; then
  echo "⏭  N/A — brain ainda em setup (placeholders presentes)"
else
  # 3a. Projetos em _index.md têm arquivo?
  INDEX="$BRAIN/memory/projects/_index.md"
  if [ -f "$INDEX" ]; then
    # Extrai refs [arquivo.md] ignorando placeholders óbvios
    REFS=$(grep -oE "\[[a-z0-9_-]+\.md\]" "$INDEX" | grep -vE "^\[projeto-[0-9]\.md\]$" | sort -u)
    for ref in $REFS; do
      file=$(echo "$ref" | tr -d '[]')
      if [ ! -f "$BRAIN/memory/projects/$file" ]; then
        echo "🟡 _index.md cita '$file' mas arquivo não existe"
      fi
    done
  fi
  # 3b. Arquivos em projects/ estão listados no _index?
  find "$BRAIN/memory/projects" -name "*.md" -not -name "_index.md" 2>/dev/null | while read f; do
    name=$(basename "$f")
    if ! grep -q "$name" "$INDEX" 2>/dev/null; then
      echo "🟡 $name existe em projects/ mas não está em _index.md"
    fi
  done
  echo "🟢 Invariantes verificadas"
fi
```

---

## Camada 4 — Frescor (cache stale e zumbis)

```bash
echo ""
echo "=== CAMADA 4 — FRESCOR ==="

# 4a. business-context.md vs última decisão
BC="$BRAIN/memory/context/business-context.md"
DEC_DIR="$BRAIN/memory/context/decisoes"
if [ -f "$BC" ] && [ -d "$DEC_DIR" ]; then
  LAST_DEC=$(ls -t "$DEC_DIR"/*.md 2>/dev/null | head -1)
  if [ -n "$LAST_DEC" ]; then
    BC_MOD=$(stat -c %Y "$BC" 2>/dev/null || stat -f %m "$BC")
    DEC_MOD=$(stat -c %Y "$LAST_DEC" 2>/dev/null || stat -f %m "$LAST_DEC")
    if [ "$DEC_MOD" -gt "$BC_MOD" ]; then
      DIFF=$(( (DEC_MOD - BC_MOD) / 86400 ))
      [ "$DIFF" -gt 7 ] && echo "🟡 business-context.md está ${DIFF}d mais antigo que decisoes/ — atualizar cache"
    fi
  fi
fi

# 4b. Arquivos de contexto > 30d sem update
find "$BRAIN/memory/context" -maxdepth 1 -name "*.md" -mtime +30 2>/dev/null | while read f; do
  echo "🟡 $(basename $f) sem update há > 30 dias"
done

# 4c. Pendências 🔴 paradas > 14d (heurística: arquivo pendencias.md sem update)
PEND="$BRAIN/memory/context/pendencias.md"
if [ -f "$PEND" ] && grep -q "🔴" "$PEND"; then
  PEND_MOD=$(stat -c %Y "$PEND" 2>/dev/null || stat -f %m "$PEND")
  NOW=$(date +%s)
  DAYS=$(( (NOW - PEND_MOD) / 86400 ))
  [ "$DAYS" -gt 14 ] && echo "🟡 pendencias.md tem 🔴 crítica e sem update há ${DAYS}d — revisar zumbis"
fi

# 4d. Projetos 🟢 Ativos sem update > 30d
find "$BRAIN/memory/projects" -name "*.md" -not -name "_index.md" -mtime +30 2>/dev/null | while read f; do
  if grep -q "🟢\|Status: Ativo" "$f" 2>/dev/null; then
    echo "🟡 $(basename $f): 🟢 Ativo mas sem update há > 30 dias"
  fi
done
```

---

## Camada 5 — Volume

```bash
echo ""
echo "=== CAMADA 5 — VOLUME ==="

# Sessions acumuladas
if [ -d "$BRAIN/memory/sessions" ]; then
  TOTAL=$(find "$BRAIN/memory/sessions" -name "*.md" | wc -l | tr -d ' ')
  OLD=$(find "$BRAIN/memory/sessions" -name "*.md" -mtime +90 | wc -l | tr -d ' ')
  echo "Sessions: $TOTAL total · $OLD > 90d"
  [ "$OLD" -gt 30 ] && echo "🟡 $OLD sessions > 90d — considerar arquivar"
fi

# Pendências resolvidas acumuladas
if [ -f "$BRAIN/memory/context/pendencias.md" ]; then
  RESOLVED=$(awk '/^## ✅ Resolvidas/,0' "$BRAIN/memory/context/pendencias.md" | grep -c "^- " || echo 0)
  [ "$RESOLVED" -gt 20 ] && echo "🟡 $RESOLVED pendências resolvidas acumuladas — arquivar histórico"
fi

# Arquivos grandes (> 500KB sugere lixo)
LARGE=$(find "$BRAIN" -type f -size +500k -not -path "*/.git/*" 2>/dev/null)
if [ -n "$LARGE" ]; then
  echo "🟡 Arquivos > 500KB:"
  echo "$LARGE" | sed 's/^/  /'
fi

# Tamanho total
du -sh "$BRAIN" 2>/dev/null | awk '{print "Tamanho total:", $1}'
```

---

## Camada 6 — Self-audit das skills

Verifica skills do brain (`$BRAIN/skills/*/SKILL.md`, se existirem) e skills globais instaladas do kit (`~/.claude/skills/{cerebro,rotina,salve}`):

```bash
echo ""
echo "=== CAMADA 6 — SKILLS ==="

# Skills do brain
SKILLS_DIR="$BRAIN/skills"
if [ -d "$SKILLS_DIR" ]; then
  find "$SKILLS_DIR" -name "SKILL.md" | while read skill; do
    # Referências a paths $SECOND_BRAIN_PATH/... que não existem
    refs=$(grep -oE '\$SECOND_BRAIN_PATH/[a-zA-Z0-9/_-]+\.md' "$skill" | sort -u)
    for ref in $refs; do
      path=$(echo "$ref" | sed "s|\$SECOND_BRAIN_PATH|$BRAIN|")
      # Ignorar padrões dinâmicos (YYYY-MM)
      if ! echo "$path" | grep -qE 'YYYY|\{.*\}'; then
        [ ! -f "$path" ] && echo "🟡 $(basename $(dirname $skill)): referencia '$ref' que não existe"
      fi
    done
    # Sintaxe dos blocos bash
    awk '/^```bash$/,/^```$/' "$skill" | grep -v '^```' | bash -n 2>&1 | head -3
  done
fi

# Registry atualizado?
if [ -f "$BRAIN/skills/_registry.md" ]; then
  DECLARED=$(grep -c "^| /" "$BRAIN/skills/_registry.md" 2>/dev/null || echo 0)
  ACTUAL=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
  [ "$DECLARED" -ne "$ACTUAL" ] && echo "🟡 _registry.md declara $DECLARED skill(s), existem $ACTUAL"
fi
```

---

## Output final — relatório consolidado

Após rodar todas as camadas, apresentar resumo:

```
╔════════════════════════════════════════╗
║  DIAGNÓSTICO — DD/MM/YYYY HH:MM        ║
║  Brain: <path>                         ║
╚════════════════════════════════════════╝

ESTADO GERAL: 🟢 saudável  |  🟡 N alertas  |  🔴 N críticos

CAMADA 1 — Estrutura          🟢
CAMADA 2 — Git                🟡
CAMADA 3 — Invariantes        🟢
CAMADA 4 — Frescor            🟡
CAMADA 5 — Volume             🟢
CAMADA 6 — Skills             🟢

ALERTAS:
  🟡 [detalhe do alerta 1 — com ação sugerida]
  🟡 [detalhe do alerta 2 — com ação sugerida]
  🔴 [crítico 1 — ação imediata]

AÇÕES SUGERIDAS (priorizadas):
  1. [ação mais urgente]
  2. [próxima]
  3. [...]

Próximo diagnóstico recomendado: em 7 dias.
```

---

## Regras

- **Read-only.** Nunca editar, mover, deletar arquivo — só reportar.
- **Agrupar por severidade**, não por ordem de execução.
- **Cada alerta vem com ação concreta** — não "pendencias.md está stale", mas "pendencias.md sem update há 20d — rodar /rotina ou revisar pendências".
- **Não repetir info óbvia** — se Camada 1 passou, não listar cada arquivo ok, só dizer "🟢 8/8 presentes".
- **Brain virgem ≠ brain quebrado** — degradar checks semânticos com "N/A — brain em setup".

## Fallback

- Erro ao ler arquivo → reportar e continuar (não abortar).
- Sem remote git → flag como 🟡, não 🔴.
- Todas camadas verdes → output em 1 linha: "🟢 Cérebro saudável — X arquivos, Y sessions, último push Nd atrás."
