# Segundo Cérebro para Claude Code
### Sistema /cerebro + /rotina + /salve

> Um repositório (ou pasta local) que funciona como memória persistente do Claude Code.  
> Três skills que transformam qualquer sessão em trabalho acumulativo.

---

## O que é esse sistema

O problema padrão com o Claude Code: cada sessão começa do zero. Você re-explica contexto, re-toma decisões, perde o fio da meada.

Esse sistema resolve isso com três skills:

| Skill | Quando usar | O que faz |
|-------|-------------|-----------|
| `/cerebro` | Início de sessão | Carrega todo o contexto (pendências, projetos, decisões recentes, últimas sessões) |
| `/rotina` | Manhã | Cockpit do dia: emails, agenda, tarefas, métricas — tudo em uma tela |
| `/salve` | Fim de sessão | Flush: salva decisões, pendências, projetos, cria log, faz commit/push |
| `/skill-audit` | Antes de publicar skill | Audita `SKILL.md` contra 10 QA checks — garante que dispara em Claude, GPT, Gemini |

**O loop:** `/cerebro` → trabalha → `/salve` → amanhã `/cerebro` já sabe tudo que aconteceu.

Bonus: [`skill-audit`](skills/skill-audit/) valida qualquer skill sua contra o padrão V3 (útil pra quem migrou de Claude pre-4.5). Standalone também em [`okjpg/skill-audit`](https://github.com/okjpg/skill-audit).

---

## Você já tem notas organizadas em algum lugar?

Não precisa construir do zero. Existem dois caminhos:

### Caminho A — Tenho arquivos/notas (Notion export, Obsidian, pasta com markdowns...)

1. Coloque sua pasta onde está
2. Configure `SECOND_BRAIN_PATH` apontando para ela
3. Instale as skills
4. Rode `/cerebro` — ele vai **mapear o que existe**, identificar o que está faltando e criar só os arquivos ausentes, sem tocar no que você já tem

### Caminho B — Começo do zero

Siga o passo a passo completo abaixo.

Em ambos os casos, o sistema funciona com o que tiver. Ele usa os arquivos que encontrar e ignora o que não existe.

---

## Pré-requisitos

### Claude Code
Baixe e instale em [claude.ai/download](https://claude.ai/download).

> Se preferir instalar via terminal, você precisa do **Node.js** (baixe em [nodejs.org](https://nodejs.org)) e depois rode:
> ```bash
> npm install -g @anthropic-ai/claude-code
> ```

### Git
Verifique se já tem instalado abrindo o terminal e rodando `git --version`. Se não tiver, baixe em [git-scm.com](https://git-scm.com).

### Conta no GitHub (opcional, mas recomendado)
Para backup e sincronização entre máquinas. Crie gratuitamente em [github.com](https://github.com).  
Sem GitHub, o sistema funciona 100% local — você só não tem backup automático.

---

## Instalação

> **Mac/Linux:** use o Terminal.  
> **Windows:** use o PowerShell (comandos alternativos indicados abaixo) ou instale o WSL (recomendado para acesso completo).

---

### Passo 1 — Criar a pasta do segundo cérebro

**Mac/Linux:**
```bash
mkdir -p ~/segundo-cerebro/memory/context/decisoes
mkdir -p ~/segundo-cerebro/memory/projects
mkdir -p ~/segundo-cerebro/memory/sessions
mkdir -p ~/segundo-cerebro/scripts
mkdir -p ~/segundo-cerebro/skills
touch ~/segundo-cerebro/memory/sessions/.gitkeep
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force "$HOME\segundo-cerebro\memory\context\decisoes"
New-Item -ItemType Directory -Force "$HOME\segundo-cerebro\memory\projects"
New-Item -ItemType Directory -Force "$HOME\segundo-cerebro\memory\sessions"
New-Item -ItemType Directory -Force "$HOME\segundo-cerebro\scripts"
New-Item -ItemType Directory -Force "$HOME\segundo-cerebro\skills"
New-Item -ItemType File "$HOME\segundo-cerebro\memory\sessions\.gitkeep"
```

> **Já tem uma pasta com notas?** Pule este passo e use a pasta que já tem no próximo.

---

### Passo 2 — Copiar os templates

Vá até a pasta deste kit (onde você descompactou):

**Mac/Linux:**
```bash
cd ~/Downloads/segundo-cerebro-kit
cp -r templates/* ~/segundo-cerebro/
```

**Windows (PowerShell):**
```powershell
cd "$HOME\Downloads\segundo-cerebro-kit"
Copy-Item -Recurse templates\* "$HOME\segundo-cerebro\"
```

> **Já tem notas:** copie apenas os arquivos que você não tiver. O `/cerebro` vai identificar o que está faltando quando você rodar pela primeira vez.

---

### Passo 3 — Preencher seus dados

Abra a pasta `~/segundo-cerebro` no seu editor (VS Code, Notion, qualquer editor de texto) e edite:

- **`CLAUDE.md`** — o mais importante. Substitua `[SEU NOME]` e preencha seus projetos, equipe e contexto geral. O Claude usa isso em todas as sessões.
- **`memory/context/business-context.md`** — visão geral dos seus negócios ou projetos
- **`memory/context/people.md`** — equipe e contatos relevantes

Os outros arquivos você preenche conforme usa. Pode deixar com os placeholders por enquanto — o sistema funciona com arquivos vazios.

---

### Passo 4 — Configurar a variável de ambiente

Isso diz ao Claude onde está seu segundo cérebro.

**Mac/Linux:** Abra `~/.zshrc` (no Mac) ou `~/.bashrc` (no Linux/bash) em qualquer editor e adicione no final:
```bash
export SECOND_BRAIN_PATH="$HOME/segundo-cerebro"
```
Depois aplique: `source ~/.zshrc`

> Não sabe qual shell usa? Rode `echo $SHELL`. Se mostrar `/bin/zsh`, edite `.zshrc`. Se mostrar `/bin/bash`, edite `.bashrc`.

**Windows (PowerShell):**
```powershell
# Variável permanente (persiste após reiniciar)
[System.Environment]::SetEnvironmentVariable("SECOND_BRAIN_PATH", "$HOME\segundo-cerebro", "User")
```
Feche e reabra o PowerShell para ativar.

> **Pasta diferente?** Substitua `$HOME/segundo-cerebro` pelo caminho real da sua pasta.  
> Para descobrir o caminho: **Mac/Linux:** `echo $HOME` | **Windows:** `echo $HOME` ou `$env:USERPROFILE`

---

### Passo 5 — Instalar as skills

**Mac/Linux:**
```bash
mkdir -p ~/.claude/skills/cerebro ~/.claude/skills/rotina ~/.claude/skills/salve

# (ainda dentro da pasta segundo-cerebro-kit)
cp skills/cerebro/SKILL.md ~/.claude/skills/cerebro/
cp skills/rotina/SKILL.md ~/.claude/skills/rotina/
cp skills/salve/SKILL.md ~/.claude/skills/salve/
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills\cerebro"
New-Item -ItemType Directory -Force "$HOME\.claude\skills\rotina"
New-Item -ItemType Directory -Force "$HOME\.claude\skills\salve"

Copy-Item skills\cerebro\SKILL.md "$HOME\.claude\skills\cerebro\"
Copy-Item skills\rotina\SKILL.md "$HOME\.claude\skills\rotina\"
Copy-Item skills\salve\SKILL.md "$HOME\.claude\skills\salve\"
```

---

### Passo 6 — Configurar o Git (opcional, para backup e sync)

Se quiser backup no GitHub:

```bash
cd ~/segundo-cerebro
git init
git add .
git commit -m "setup: estrutura inicial do segundo cérebro"
```

Crie um repositório privado em [github.com/new](https://github.com/new) e conecte:
```bash
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

Sem isso, o `/salve` ainda funciona — só não faz push para o remoto.

#### Regras de sync (importante se usar Git)

O sistema usa **merge** para sincronizar, nunca rebase. Motivo: rebase pode deixar o repositório num estado quebrado (rebase incompleto) que trava todas as operações seguintes. Merge é mais seguro — no pior caso cria um merge commit, mas nunca trava.

Se o repositório ficar num estado estranho (rebase/merge incompleto), o `brain-boot.sh` detecta e recupera automaticamente ao abrir uma nova sessão.

**Se usar em múltiplas máquinas:** cada uma faz pull no início (via `brain-boot.sh`) e push no final (via `/salve`). Evite editar os mesmos arquivos em duas máquinas ao mesmo tempo sem sincronizar entre elas.

---

### Passo 7 — Testar

Abra o Claude Code e digite:
```
/cerebro
```

Na primeira vez, ele vai:
1. Detectar o que já existe na sua pasta
2. Listar o que está faltando
3. Perguntar se quer criar os arquivos ausentes
4. Configurar o hook de boot automático (opcional)

---

## Como usar no dia a dia

### Início de sessão
```
/cerebro
```
Carrega todo o contexto. Você vê o estado atual do seu segundo cérebro em segundos.

Para ver detalhes, diga:
- `mostra pendências` → lista completa
- `mostra projetos` → status de todos os projetos
- `mostra deadlines` → prazos próximos
- `mostra [nome do projeto]` → detalhes de um projeto

### Manhã
```
/rotina
```
Cockpit completo: emails, agenda, tarefas, métricas. Define o Top 3 do dia, bloqueia no calendar se quiser.

### Fim de sessão
```
/salve
```
Salva tudo que mudou, cria log da sessão, faz commit e push (se tiver Git configurado).

---

## Estrutura do segundo cérebro

Os arquivos que o sistema usa (todos opcionais — use só os que fizerem sentido pra você):

```
segundo-cerebro/
├── CLAUDE.md                       # Quem você é — Claude lê em todo projeto
├── PROPAGATION.md                  # O que atualizar quando algo muda
├── MAPA.md                         # Guia de navegação (onde encontrar o quê)
├── scripts/
│   └── brain-boot.sh              # Script de sync automático ao abrir Claude
├── skills/
│   └── _registry.md               # Índice de skills (cresce com você)
└── memory/
    ├── context/
    │   ├── pendencias.md          # Tudo em aberto (🔴 crítico, 🟡 importante)
    │   ├── deadlines.md           # Prazos
    │   ├── business-context.md    # Visão geral dos seus projetos/negócios
    │   ├── people.md              # Equipe e contatos
    │   └── decisoes/
    │       └── YYYY-MM.md         # Decisões do mês
    ├── projects/
    │   ├── _index.md              # Status de todos os projetos
    │   └── {nome-projeto}.md      # 1 arquivo por projeto (criado pelo /salve)
    └── sessions/
        └── YYYY-MM-DD.md          # Log de cada sessão (criado pelo /salve)
```

**Mínimo para funcionar:** qualquer pasta com `SECOND_BRAIN_PATH` apontando pra ela. O resto vai sendo criado conforme você usa.

---

## Personalizando o /rotina

Edite `~/.claude/skills/rotina/SKILL.md` e localize as marcações `[CONFIGURAR]`:

- **Fuso horário** — padrão `America/Sao_Paulo`; troque pelo seu (ex: `America/Bogota`, `Europe/Lisbon`)
- **Métricas** — adicione queries para seus negócios (SaaS, e-commerce, planilhas...)
- **Tasks no Notion** — configure os IDs das suas databases
- **Metas de conteúdo** — ajuste plataformas e frequências

---

## Configurando MCPs (para /rotina completo)

MCPs são integrações que permitem ao Claude acessar serviços externos. São opcionais.

Todas as configurações vão em `~/.mcp.json`. Se não existir, crie o arquivo.

> **Dica:** Não sabe configurar? Abra o Claude Code e peça: *"me ajuda a configurar o MCP do Gmail"*. Ele te guia passo a passo.

### Gmail
Repositório: [github.com/GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server)

### Google Calendar
Repositório: [github.com/nspady/google-calendar-mcp](https://github.com/nspady/google-calendar-mcp)

### Notion
Repositório oficial: [github.com/makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server)

### Como adicionar ao ~/.mcp.json

Exemplo de estrutura (adicione os servidores que quiser):
```json
{
  "mcpServers": {
    "gmail": { ... },
    "google-calendar": { ... },
    "notion": { ... }
  }
}
```

Cada repositório tem as instruções de configuração específicas.

---

## Quando escalar a estrutura

O sistema começa simples e cresce com você. Aqui estão os sinais de que é hora de expandir:

| Sinal | Ação |
|-------|------|
| `people.md` tem 10+ pessoas | Criar pasta `memory/context/people/` com 1 arquivo por pessoa. Manter `people.md` como sumário |
| Você criou 2+ skills | Criar `skills/_registry.md` (template incluso) para indexar |
| Tem operações por área (marketing, vendas...) | Criar `areas/{nome}/` com contexto, skills e rotinas por área |
| `business-context.md` está enorme | Criar `memory/context/business/` com 1 arquivo por negócio. Manter `business-context.md` como cache |
| Tem 5+ skills | Organizar em categorias: `skills/{categoria}/{nome}/SKILL.md` |

O `/cerebro` e o `/salve` funcionam igual independente do tamanho — eles leem o que existe e ignoram o que não existe.

---

## Dúvidas frequentes

**P: Não tenho negócio. Funciona para outras áreas?**  
R: Sim. Use `business-context.md` para qualquer contexto: carreira, estudos, projetos pessoais, pesquisa. A estrutura é a mesma.

**P: Já tenho notas no Notion / Obsidian. Preciso migrar tudo?**  
R: Não. Você pode exportar o que quiser para markdown e colocar na pasta, ou simplesmente criar os arquivos-chave (pendencias.md, business-context.md) do zero com o resumo do que já tem. O `/cerebro` vai mapear o que existe e sugerir o que falta.

**P: Precisa de GitHub?**  
R: Não. O sistema funciona local. GitHub só adiciona backup e sync entre máquinas.

**P: O /rotina funciona sem MCPs?**  
R: Sim. Sem Gmail: seção de email indisponível. Sem Calendar: agenda indisponível. Pendências, projetos e deadlines sempre funcionam.

**P: Como o Claude "lembra" entre sessões?**  
R: Não é memória do modelo — é o Git (ou sua pasta local). Cada sessão lê os arquivos que o `/salve` da sessão anterior atualizou.

**P: O Git ficou travado / dá erro de "rebase in progress" ou "merge in progress".**  
R: Acontece quando um pull encontra conflito e não consegue resolver. O `brain-boot.sh` já detecta e recupera automaticamente ao abrir uma nova sessão. Se precisar resolver manualmente, rode: `cd ~/segundo-cerebro && git rebase --abort` (ou `git merge --abort`). Depois rode `/cerebro` normalmente.

**P: Estou no Windows. Funciona?**  
R: Funciona para os passos de configuração via PowerShell (comandos listados acima). O script `brain-boot.sh` de sync automático **requer WSL** (Windows Subsystem for Linux) para rodar — sem ele, você apenas não terá o git pull automático ao abrir o Claude, mas tudo mais funciona.  
Para instalar WSL: abra o PowerShell como administrador e rode `wsl --install`, reinicie, e siga os passos normalmente dentro do Ubuntu instalado.

**P: O fuso horário do /rotina está errado.**  
R: Edite `~/.claude/skills/rotina/SKILL.md` e substitua `America/Sao_Paulo` pelo seu fuso. Lista completa: [wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

**P: Posso ter mais de um segundo cérebro?**  
R: Sim. Mude `SECOND_BRAIN_PATH` para outra pasta. Útil para separar contextos (trabalho / pessoal).

---

## Próximos passos

1. Rode `/cerebro` — ele mapeia o que existe e configura o que falta
2. Preencha o `CLAUDE.md` com seus dados reais (é o arquivo mais importante)
3. Faça uma sessão de trabalho normal com o Claude
4. Rode `/salve` no final
5. Abra uma nova sessão e rode `/cerebro` — o contexto vai estar lá

---

*Sistema criado por [Bruno Okamoto](https://bruno.microsaas.com.br). Inspirado no conceito de "segundo cérebro" do Tiago Forte, adaptado para Claude Code.*
