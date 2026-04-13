# [SEU NOME] — Contexto para o Claude Code

## Fontes de Contexto

| Fonte | Path | O que tem |
|-------|------|-----------|
| **Segundo Cérebro** | `~/segundo-cerebro/` | Contexto operacional: pendências, decisões, projetos |
| **Este arquivo** | `~/.claude/CLAUDE.md` | Perfil, diretrizes gerais |

> **Regra:** antes de criar algo novo, consultar o segundo cérebro. Contexto operacional vive lá, não aqui.

---

## Quem sou eu

[Descreva quem você é em 2-3 linhas: profissão, área de atuação, contexto principal]

Exemplo:
> Empreendedor e criador de conteúdo. Founder de 2 SaaS. 50k seguidores combinados no LinkedIn e YouTube.

---

## Meus Projetos e Negócios

[Liste seus projetos/negócios principais — o Claude vai referenciar isso automaticamente]

Exemplo:
```
- NomeProjeto1: [o que é, status atual]
- NomeProjeto2: [o que é, status atual]
```

---

## Minha Equipe

[Se tiver equipe, liste quem é quem]

---

## Como prefiro trabalhar

[Adicione suas preferências pessoais aqui. Os princípios abaixo são um bom ponto de partida:]

### Pensar antes de agir
- Surfar suposições antes de executar — se algo é ambíguo, perguntar
- Apresentar interpretações diferentes quando o pedido não é claro
- Não assumir que a abordagem é óbvia

### Simplicidade primeiro
- Começar com a solução mais simples possível
- Sem features especulativas, sem abstrações prematuras
- 3 linhas similares são melhores que uma abstração desnecessária
- Se 200 linhas podem ser 50, reescrever

### Mudanças cirúrgicas
- Só tocar no que o pedido requer — toda linha mudada deve rastrear direto ao pedido
- Manter estilo e padrões existentes do código
- Não "melhorar" código adjacente, não adicionar docstrings onde não tinha

### Verificar antes de declarar pronto
- Transformar tarefas em critérios verificáveis: não "fix the bug" mas "teste que reproduz o bug passa"
- Nunca marcar tarefa como completa sem provar que funciona
- Confirmar antes de ações irreversíveis

### Segundo cérebro
- Sempre consultar o segundo cérebro antes de criar algo novo
- Resposta direta, sem preâmbulo

---

## Stack técnico

[Suas tecnologias principais]

Exemplos:
- Backend: Node.js / Python / etc.
- Banco: Supabase / PostgreSQL / etc.
- Frontend: React / Next.js / etc.

---

## Segundo Cérebro

| Estou buscando... | Onde ir |
|-------------------|---------|
| O que está em aberto | `$SECOND_BRAIN_PATH/memory/context/pendencias.md` |
| Prazos | `$SECOND_BRAIN_PATH/memory/context/deadlines.md` |
| Decisões recentes | `$SECOND_BRAIN_PATH/memory/context/decisoes/YYYY-MM.md` |
| Status dos projetos | `$SECOND_BRAIN_PATH/memory/projects/_index.md` |
| Equipe e contatos | `$SECOND_BRAIN_PATH/memory/context/people.md` |
| Contexto geral | `$SECOND_BRAIN_PATH/memory/context/business-context.md` |

---

*Criado: [data]*
*Atualizar: sempre que contexto mudar*
