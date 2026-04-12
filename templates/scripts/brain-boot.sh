#!/bin/bash
# brain-boot.sh — Executado pelo SessionStart hook do Claude Code
# Sincroniza o repositório do segundo cérebro antes de cada sessão.
#
# Como instalar:
#   1. Salve este arquivo em $SECOND_BRAIN_PATH/scripts/brain-boot.sh
#   2. Dê permissão: chmod +x $SECOND_BRAIN_PATH/scripts/brain-boot.sh
#   3. Configure o hook em ~/.claude/settings.json (veja README.md)

set -e

# Verifica se SECOND_BRAIN_PATH está configurado
if [ -z "$SECOND_BRAIN_PATH" ]; then
  echo "⚠️  SECOND_BRAIN_PATH não configurado. Adicione ao seu .zshrc ou .bashrc:"
  echo "    export SECOND_BRAIN_PATH=\"$HOME/segundo-cerebro\""
  exit 1
fi

# Verifica se o diretório existe
if [ ! -d "$SECOND_BRAIN_PATH" ]; then
  echo "⚠️  Diretório não encontrado: $SECOND_BRAIN_PATH"
  exit 1
fi

cd "$SECOND_BRAIN_PATH"

echo "=== SEGUNDO CÉREBRO — $(date '+%d/%m/%Y %H:%M') ==="
echo "Repo: $SECOND_BRAIN_PATH"

# Sync Git (se for um repositório git)
if [ -d "$SECOND_BRAIN_PATH/.git" ]; then
  # Recuperar de estados quebrados (rebase/merge/cherry-pick incompletos)
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    git rebase --abort 2>/dev/null || true
    echo "Git:  ⚠️ Rebase incompleto recuperado"
  fi
  if [ -f .git/MERGE_HEAD ]; then
    git merge --abort 2>/dev/null || true
    echo "Git:  ⚠️ Merge incompleto recuperado"
  fi
  if [ -f .git/CHERRY_PICK_HEAD ]; then
    git cherry-pick --abort 2>/dev/null || true
    echo "Git:  ⚠️ Cherry-pick incompleto recuperado"
  fi

  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
  REMOTE=$(git remote 2>/dev/null | head -1)

  if [ -n "$REMOTE" ]; then
    # Usar merge (não rebase) para evitar estados quebrados em caso de conflito
    OUTPUT=$(git pull --no-rebase "$REMOTE" "$BRANCH" 2>&1) || true
    echo "Git:  $OUTPUT"
  else
    echo "Git:  Repositório local (sem remote configurado)"
  fi
else
  echo "Git:  Pasta local (sem Git — backup não configurado)"
fi

# Exibe pendências ativas (boot rápido)
PENDENCIAS="$SECOND_BRAIN_PATH/memory/context/pendencias.md"
if [ -f "$PENDENCIAS" ]; then
  echo ""
  echo "--- PENDÊNCIAS ---"
  cat "$PENDENCIAS"
fi

# Exibe última sessão
SESSIONS_DIR="$SECOND_BRAIN_PATH/memory/sessions"
if [ -d "$SESSIONS_DIR" ]; then
  LAST_SESSION=$(ls "$SESSIONS_DIR"/*.md 2>/dev/null | sort | tail -1)
  if [ -n "$LAST_SESSION" ]; then
    SESSION_DATE=$(basename "$LAST_SESSION" .md)
    echo ""
    echo "--- ÚLTIMA SESSÃO ($SESSION_DATE) ---"
    cat "$LAST_SESSION"
  fi
fi
