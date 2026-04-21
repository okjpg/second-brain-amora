# Security Policy

## Reportando vulnerabilidades

Encontrou um problema de segurança neste kit? Obrigado por reportar com responsabilidade.

### Como reportar

Se você descobriu uma vulnerabilidade que afeta este repositório:

1. **NÃO abra uma issue pública** — vulnerabilidades em issues ficam visíveis pra todo mundo antes do patch
2. Use o [**Private vulnerability reporting**](https://github.com/okjpg/second-brain-amora/security/advisories/new) do GitHub
3. Ou envie email para **bruno@microsaas.com.br** com assunto `[SECURITY] second-brain-amora`

### O que incluir no report

- Descrição clara do problema
- Passos pra reproduzir (quanto mais específico, melhor)
- Versão/commit afetado (se aplicável)
- Impacto potencial (ex: exposição de credenciais, RCE, etc)
- Se souber: proposta de fix

### Tempo de resposta

- **Primeira resposta:** até 48h úteis
- **Triage + plano de correção:** até 7 dias
- **Patch em produção:** depende da severidade (crítico = imediato, médio = sprint seguinte)

### O que esperar

1. Confirmação de recebimento
2. Investigação + validação da severidade
3. Patch desenvolvido em private fork
4. Disclosure coordenado após fix publicado
5. Crédito no CHANGELOG (se você quiser reconhecimento público)

---

## Escopo deste repositório

Este kit é **open source (MIT)** e distribui:

- Skills para Claude Code (`/cerebro`, `/rotina`, `/salve`, `skill-audit`)
- Script shell de instalação (`install.sh`)
- Templates de arquivos markdown pra segundo cérebro

### O que é escopo de security aqui

- Scripts shell que executam comandos no sistema do usuário (`install.sh`, `brain-boot.sh`)
- Skills que fazem leitura/escrita em `~/.claude/skills/` e `$SECOND_BRAIN_PATH`
- Sugestões de comandos git/bash que podem ter efeito destrutivo se mal formados
- Paths hardcoded, defaults inseguros, ou parsing frágil que leve a injection

### O que NÃO é escopo

- Bugs de usabilidade ou UX
- Feature requests
- Vulnerabilidades no Claude Code (reportar ao [Anthropic](https://support.anthropic.com))
- Vulnerabilidades em MCPs de terceiros referenciados no README (Gmail, Calendar, Notion) — reportar aos respectivos maintainers

---

## Boas práticas ao usar este kit

- **Nunca** hardcode credenciais nos templates ou skills que você customizar. Use `op` (1Password CLI) ou `.env` (no gitignore).
- O `brain-boot.sh` faz `git pull` automático. Se usa múltiplas máquinas, garanta que não há commits pendentes em outra antes de abrir o Claude Code.
- Ao tornar seu segundo cérebro um repo privado no GitHub, **não adicione colaboradores sem revisar** `memory/context/pendencias.md` e `memory/context/decisoes/` — esses arquivos costumam ter informação operacional sensível.
- O `/salve` faz `git push` automático — se o repo for público, certifique-se de que `.gitignore` cobre qualquer arquivo com credencial.

---

*Política de segurança atualizada em 21/04/2026.*
