# Segundo Cerebro — Mapa de Navegacao

> Guia rapido: onde encontrar cada tipo de informacao.

## Estrutura

```
segundo-cerebro/
├── CLAUDE.md                       # Quem voce e — Claude le em toda sessao
├── PROPAGATION.md                  # O que atualizar quando algo muda
├── MAPA.md                         # Este arquivo — guia de navegacao
├── scripts/
│   └── brain-boot.sh              # Sync automatico ao abrir Claude
├── skills/
│   └── _registry.md               # Indice de skills (cresce com voce)
└── memory/
    ├── context/
    │   ├── pendencias.md          # Tudo em aberto
    │   ├── deadlines.md           # Prazos
    │   ├── business-context.md    # Visao geral (cache compilado)
    │   ├── people.md              # Equipe e contatos
    │   └── decisoes/
    │       └── YYYY-MM.md         # Decisoes por mes
    ├── projects/
    │   ├── _index.md              # Status de todos os projetos
    │   └── {nome-projeto}.md      # 1 arquivo por projeto
    └── sessions/
        └── YYYY-MM-DD.md          # Log de cada sessao
```

## Onde procurar o que

| Estou buscando... | Onde ir |
|-------------------|---------|
| O que esta em aberto | `memory/context/pendencias.md` |
| Prazos e deadlines | `memory/context/deadlines.md` |
| Decisoes recentes | `memory/context/decisoes/YYYY-MM.md` |
| Status de todos os projetos | `memory/projects/_index.md` |
| Detalhes de 1 projeto | `memory/projects/{nome}.md` |
| Equipe e contatos | `memory/context/people.md` |
| Contexto geral | `memory/context/business-context.md` |
| O que aconteceu ontem | `memory/sessions/YYYY-MM-DD.md` |
| Skills disponiveis | `skills/_registry.md` (quando tiver) |

## Como o cerebro cresce

Conforme voce usa, o Claude vai criando arquivos novos automaticamente (via `/salve`). Pastas opcionais que surgem com o tempo:

| Pasta | Quando criar | O que guarda |
|-------|-------------|-------------|
| `skills/` | Quando tiver 2+ skills | Skills organizadas por categoria + `_registry.md` |
| `memory/context/people/` | Quando `people.md` ficar grande (10+ pessoas) | 1 arquivo por pessoa (detalhes, historico) |
| `areas/` | Quando tiver operacoes por area (marketing, vendas...) | Contexto, skills e rotinas por area |

Nao precisa criar tudo de uma vez. O sistema funciona com o minimo e escala conforme a necessidade.

---

*Atualizado: [data de setup]*
