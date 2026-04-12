---
name: cerebro
description: >
  Liga o segundo cérebro — carrega todo o contexto (pendências, deadlines,
  decisões, projetos, equipe, skills) para operar com memória persistente.
  Modo Setup quando não configurado. Modo Briefing quando já configurado.
  Triggers: "cerebro", "/cerebro", "liga o cérebro", "conecta o segundo cérebro".
---

# /cerebro

Dois modos de operação, detectados automaticamente.

---

## Detecção de modo

```bash
echo "SECOND_BRAIN_PATH=$SECOND_BRAIN_PATH"
test -f "${SECOND_BRAIN_PATH}/memory/context/pendencias.md" && echo "CONFIGURED=true" || echo "CONFIGURED=false"
```

- `CONFIGURED=false` → **Modo Setup**
- `CONFIGURED=true` → **Modo Briefing**

---

## MODO SETUP (primeira vez)

O objetivo é configurar o segundo cérebro com o **mínimo de esforço** — aproveitando o que já existe e criando só o que falta.

### Passo 1 — Localizar ou criar a pasta

Pergunte:
> "Você já tem uma pasta com notas ou arquivos markdown em algum lugar? (Notion export, Obsidian, qualquer pasta)"

- **Se sim:** pergunte o caminho e use essa pasta como `BRAIN_PATH`
- **Se não:** pergunte onde quer criar (Enter para `~/segundo-cerebro`) e crie a pasta:

```bash
BRAIN_PATH="${RESPOSTA_DO_USUARIO:-$HOME/segundo-cerebro}"
mkdir -p "$BRAIN_PATH/memory/context/decisoes"
mkdir -p "$BRAIN_PATH/memory/projects"
mkdir -p "$BRAIN_PATH/memory/sessions"
mkdir -p "$BRAIN_PATH/scripts"
mkdir -p "$BRAIN_PATH/skills"
```

Se o usuário informou uma URL do GitHub, clone no lugar de criar:
```bash
git clone <URL_INFORMADA> "$BRAIN_PATH"
```

### Passo 2 — Mapear o que já existe

Escaneie a pasta para ver o que está lá:

```bash
echo "=== MAPEAMENTO DA PASTA ==="
echo "Pasta: $BRAIN_PATH"
echo ""

# Arquivos de contexto esperados
for f in "CLAUDE.md" "PROPAGATION.md" "MAPA.md" "memory/context/pendencias.md" "memory/context/deadlines.md" "memory/context/business-context.md" "memory/context/people.md" "memory/projects/_index.md" "skills/_registry.md" "scripts/brain-boot.sh"; do
  if [ -f "$BRAIN_PATH/$f" ]; then
    echo "✅ $f"
  else
    echo "❌ $f (ausente)"
  fi
done

echo ""
echo "Arquivos existentes na pasta:"
find "$BRAIN_PATH" -name "*.md" | head -20
```

Apresente o resultado ao usuário em formato legível:

```
📂 Pasta: /caminho/para/pasta

Encontrado:
  ✅ [arquivos que existem]

Faltando:
  ❌ [arquivos ausentes]

Arquivos extras detectados:
  [outros .md encontrados que podem ser aproveitados]
```

### Passo 3 — Criar só o que falta

Pergunte:
> "Posso criar os arquivos ausentes com templates em branco para você preencher?"

Se sim, para cada arquivo ausente, crie usando os templates padrão (do kit que instalou). **Nunca sobrescreva arquivos que já existem.**

Scripts de boot ausente — copie se o kit estiver disponível:
```bash
if [ ! -f "$BRAIN_PATH/scripts/brain-boot.sh" ]; then
  # Tentar localizar o template no kit de instalação
  KIT_BOOT=$(find ~/Downloads ~/Desktop ~ -name "brain-boot.sh" -path "*/segundo-cerebro-kit/*" 2>/dev/null | head -1)
  if [ -n "$KIT_BOOT" ]; then
    cp "$KIT_BOOT" "$BRAIN_PATH/scripts/brain-boot.sh"
    chmod +x "$BRAIN_PATH/scripts/brain-boot.sh"
    echo "✓ brain-boot.sh copiado"
  fi
fi
```

### Passo 4 — Configurar SECOND_BRAIN_PATH

```bash
if grep -q "SECOND_BRAIN_PATH" ~/.zshrc 2>/dev/null || grep -q "SECOND_BRAIN_PATH" ~/.bashrc 2>/dev/null; then
  echo "SECOND_BRAIN_PATH já configurado"
else
  SHELL_RC="$HOME/.zshrc"
  [ -f "$HOME/.bashrc" ] && [ ! -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.bashrc"
  echo "" >> "$SHELL_RC"
  echo "# Segundo Cérebro" >> "$SHELL_RC"
  echo "export SECOND_BRAIN_PATH=\"$BRAIN_PATH\"" >> "$SHELL_RC"
  echo "Adicionado em $SHELL_RC"
fi
```

### Passo 5 — Configurar SessionStart hook

```bash
python3 << 'EOF'
import json, os

settings_path = os.path.expanduser("~/.claude/settings.json")
brain_path = os.environ.get("BRAIN_PATH", os.path.expanduser("~/segundo-cerebro"))

try:
    with open(settings_path) as f:
        settings = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    settings = {}

boot_script = os.path.join(brain_path, "scripts", "brain-boot.sh")
hook_command = f'bash "{boot_script}"'

hooks = settings.get("hooks", {})
session_hooks = hooks.get("SessionStart", [])
already_exists = any(hook_command in str(entry) for entry in session_hooks)

if not already_exists and os.path.exists(boot_script):
    if "hooks" not in settings:
        settings["hooks"] = {}
    if "SessionStart" not in settings["hooks"]:
        settings["hooks"]["SessionStart"] = []
    settings["hooks"]["SessionStart"].append({
        "hooks": [{
            "type": "command",
            "command": hook_command,
            "timeout": 20,
            "statusMessage": "Sincronizando segundo cérebro..."
        }]
    })
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    print("Hook configurado.")
elif not os.path.exists(boot_script):
    print("brain-boot.sh não encontrado — hook não configurado. Copie o script manualmente.")
else:
    print("Hook já existe.")
EOF
```

### Passo 6 — Confirmar e orientar

```
✓ Pasta: <path>
✓ SECOND_BRAIN_PATH configurado
✓ <N> arquivos criados / <M> já existiam
✓ SessionStart hook ativo (ou: "hook não configurado — brain-boot.sh ausente")

Para ativar agora:
  source ~/.zshrc   (ou abra um novo terminal)

Reinicie o Claude Code. Na próxima sessão o boot é automático.

Próximo passo recomendado: preencha o CLAUDE.md com seus dados pessoais.
Digite /cerebro a qualquer momento para ver o briefing.
```

---

## MODO BRIEFING (já configurado)

### Fase 1 — Carregar contexto (paralelo, sem output)

Ler TUDO em paralelo (tool calls simultâneos). NÃO exibir o conteúdo bruto:

1. `$SECOND_BRAIN_PATH/memory/context/pendencias.md`
2. `$SECOND_BRAIN_PATH/memory/context/deadlines.md`
3. `$SECOND_BRAIN_PATH/memory/context/decisoes/` — arquivo do mês atual (YYYY-MM.md)
4. `$SECOND_BRAIN_PATH/memory/context/business-context.md`
5. `$SECOND_BRAIN_PATH/memory/context/people.md`
6. `$SECOND_BRAIN_PATH/memory/projects/_index.md`
7. `$SECOND_BRAIN_PATH/memory/sessions/` — últimos 7 dias
8. `$SECOND_BRAIN_PATH/skills/_registry.md` (primeiras 30 linhas, se existir)

Se algum arquivo não existir, pular silenciosamente.

### Fase 1.5 — Checagem de integridade

```bash
today=$(date +%Y-%m-%d)
commits_today=$(cd "$SECOND_BRAIN_PATH" && git log --since="$today" --oneline 2>/dev/null | wc -l | tr -d ' ')
session_today=$(ls "$SECOND_BRAIN_PATH/memory/sessions/$today"* 2>/dev/null | wc -l | tr -d ' ')

# stat difere entre macOS (-f "%m") e Linux (-c "%Y")
if stat -f "%m" /dev/null 2>/dev/null; then
  decisoes_mod=$(stat -f "%m" "$SECOND_BRAIN_PATH/memory/context/decisoes/$(date +%Y-%m).md" 2>/dev/null || echo "0")
  bcontext_mod=$(stat -f "%m" "$SECOND_BRAIN_PATH/memory/context/business-context.md" 2>/dev/null || echo "0")
else
  decisoes_mod=$(stat -c "%Y" "$SECOND_BRAIN_PATH/memory/context/decisoes/$(date +%Y-%m).md" 2>/dev/null || echo "0")
  bcontext_mod=$(stat -c "%Y" "$SECOND_BRAIN_PATH/memory/context/business-context.md" 2>/dev/null || echo "0")
fi

find "$SECOND_BRAIN_PATH/memory/context" -name "*.md" -not -path "*/decisoes/*" -mtime +14
```

Alertas:
- `commits_today > 0` e `session_today = 0` → sessão anterior não foi salva com /salve
- `decisoes_mod > bcontext_mod` → decisões mais recentes que o cache
- arquivo de contexto > 14 dias sem update → desatualizado

### Fase 2 — Briefing compacto

```
=== SEGUNDO CÉREBRO — Conectado DD/MM/YYYY ===

ESTADO:
  📌 N pendências (N críticas, N importantes)
  🔥 N deadlines próximos (mais urgente: [item] em X dias)
  📋 N projetos ativos
  🧰 N skills disponíveis

ÚLTIMOS 7 DIAS:
  <resumo consolidado em 3-5 linhas das sessões recentes>

DECISÕES RECENTES:
  → [decisão 1 — 1 linha]
  → [decisão 2 — 1 linha]
  → [decisão 3 — 1 linha]

ALERTAS:
  → [deadlines ≤7 dias, pendências críticas, arquivos desatualizados]
  (se não houver: "Nenhum alerta.")

Cérebro ligado. O que vamos trabalhar?
```

### Pull on demand

Após o briefing, o usuário pode pedir:
- `mostra pendências` → `pendencias.md` completo
- `mostra deadlines` → `deadlines.md` completo
- `mostra decisões` → decisões do mês completas
- `mostra projetos` → `_index.md` completo
- `mostra equipe` → `people.md`
- `mostra [projeto]` → arquivo individual do projeto

Os dados já foram carregados na Fase 1 — não precisa re-fetch.

### Fallback

- Arquivo não encontrado → omitir da contagem, continuar
- Conflito de merge no git → mencionar ANTES do briefing
- Tudo falha → "Não consegui carregar o cérebro. Verificar $SECOND_BRAIN_PATH."

### Comportamento

- Tom direto, sem preâmbulo
- Aguardar instrução após o briefing
