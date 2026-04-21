#!/usr/bin/env bash
#
# Second Brain Amora — Instalação 1 comando
# Uso: curl -sL https://cerebro.bruno.com.br/install | bash
# Ou: curl -sL https://raw.githubusercontent.com/okjpg/second-brain-amora/main/install.sh | bash
#
# O que faz:
# 1. Clona (ou atualiza) o kit em ~/second-brain-amora
# 2. Cria estrutura de pastas em ~/segundo-cerebro
# 3. Copia templates pro segundo cérebro
# 4. Instala skills /cerebro, /rotina, /salve em ~/.claude/skills
# 5. Adiciona SECOND_BRAIN_PATH no shell rc
#
# Idempotente: pode rodar múltiplas vezes sem quebrar nada.

set -eu

# ─── Cores ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
DIM='\033[2m'
NC='\033[0m'

step() { printf "${YELLOW}[%s/%s]${NC} %s\n" "$1" "$2" "$3"; }
ok()   { printf "  ${GREEN}✓${NC} %s\n" "$1"; }
skip() { printf "  ${DIM}~ %s${NC}\n" "$1"; }
warn() { printf "  ${YELLOW}!${NC} %s\n" "$1"; }
err()  { printf "${RED}✗ %s${NC}\n" "$1" >&2; exit 1; }

# ─── Config ──────────────────────────────────────────────────────────────────
BRAIN_PATH="${SECOND_BRAIN_PATH:-$HOME/segundo-cerebro}"
KIT_DIR="${KIT_DIR:-$HOME/second-brain-amora}"
REPO_URL="https://github.com/okjpg/second-brain-amora.git"

# Detecta shell rc
if [ -n "${ZSH_VERSION:-}" ] || [ "$(basename "${SHELL:-}")" = "zsh" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.zshrc"
fi
[ -f "$SHELL_RC" ] || touch "$SHELL_RC"

# ─── Header ──────────────────────────────────────────────────────────────────
printf "\n${BLUE}╔═══════════════════════════════════════════════════╗${NC}\n"
printf "${BLUE}║  Second Brain Amora — Instalação                  ║${NC}\n"
printf "${BLUE}╚═══════════════════════════════════════════════════╝${NC}\n\n"

# ─── [1/5] Pré-requisitos ────────────────────────────────────────────────────
step 1 5 "Verificando pré-requisitos…"
command -v git >/dev/null 2>&1 || err "git não encontrado. Instale: https://git-scm.com"
ok "git encontrado"
if command -v claude >/dev/null 2>&1; then
  ok "claude encontrado no PATH"
else
  warn "claude não encontrado no PATH. Se ainda não instalou: https://claude.ai/download"
fi
printf "\n"

# ─── [2/5] Clona o kit ───────────────────────────────────────────────────────
step 2 5 "Clonando kit em $KIT_DIR…"
if [ -d "$KIT_DIR/.git" ]; then
  cd "$KIT_DIR"
  git pull --ff-only origin main >/dev/null 2>&1 && ok "kit atualizado" || skip "kit já existe (pull sem fast-forward, deixando como tá)"
else
  git clone --quiet "$REPO_URL" "$KIT_DIR"
  ok "kit clonado"
fi
cd "$KIT_DIR"
printf "\n"

# ─── [3/5] Estrutura do cérebro ──────────────────────────────────────────────
step 3 5 "Criando estrutura em $BRAIN_PATH…"
mkdir -p "$BRAIN_PATH/memory/context/decisoes"
mkdir -p "$BRAIN_PATH/memory/projects"
mkdir -p "$BRAIN_PATH/memory/sessions"
mkdir -p "$BRAIN_PATH/scripts"
mkdir -p "$BRAIN_PATH/skills"
touch "$BRAIN_PATH/memory/sessions/.gitkeep"
ok "pastas criadas"

# Copia templates (não sobrescreve existentes)
for src in "$KIT_DIR/templates"/*; do
  name=$(basename "$src")
  dest="$BRAIN_PATH/$name"
  if [ ! -e "$dest" ]; then
    cp -r "$src" "$dest"
    ok "template: $name"
  else
    skip "template já existe: $name"
  fi
done
printf "\n"

# ─── [4/5] Skills ────────────────────────────────────────────────────────────
step 4 5 "Instalando skills…"
for skill in cerebro rotina salve; do
  mkdir -p "$HOME/.claude/skills/$skill"
  if [ -f "$KIT_DIR/skills/$skill/SKILL.md" ]; then
    cp "$KIT_DIR/skills/$skill/SKILL.md" "$HOME/.claude/skills/$skill/"
    ok "/$skill"
  else
    warn "skill $skill não encontrada no kit"
  fi
done
printf "\n"

# ─── [5/5] Variável de ambiente ──────────────────────────────────────────────
step 5 5 "Configurando SECOND_BRAIN_PATH em $SHELL_RC…"
if grep -q "SECOND_BRAIN_PATH" "$SHELL_RC" 2>/dev/null; then
  skip "SECOND_BRAIN_PATH já está em $SHELL_RC"
else
  {
    printf "\n# Second Brain Amora\n"
    printf "export SECOND_BRAIN_PATH=\"%s\"\n" "$BRAIN_PATH"
  } >> "$SHELL_RC"
  ok "SECOND_BRAIN_PATH adicionado"
fi
printf "\n"

# ─── Fim ─────────────────────────────────────────────────────────────────────
printf "${GREEN}╔═══════════════════════════════════════════════════╗${NC}\n"
printf "${GREEN}║  Instalação concluída                             ║${NC}\n"
printf "${GREEN}╚═══════════════════════════════════════════════════╝${NC}\n\n"
printf "Próximos passos:\n"
printf "  1. Reabra o terminal ou rode: ${BLUE}source %s${NC}\n" "$SHELL_RC"
printf "  2. Edite ${BLUE}%s/CLAUDE.md${NC} com seus dados\n" "$BRAIN_PATH"
printf "  3. Abra o Claude Code e digite: ${BLUE}/cerebro${NC}\n\n"
printf "Docs: ${BLUE}https://github.com/okjpg/second-brain-amora${NC}\n"
printf "Comunidade: ${BLUE}https://cerebro.bruno.com.br${NC}\n\n"
