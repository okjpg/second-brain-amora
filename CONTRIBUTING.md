# Contribuindo

Valeu pelo interesse em contribuir com o **Second Brain Amora**.

## O que é bem-vindo

- 🐛 **Bug fixes** em scripts (`install.sh`, `brain-boot.sh`)
- 📚 **Melhorias no README** (clareza, correção de typos, instruções pra outros SOs)
- 🧪 **Edge cases** no `install.sh` que ainda não foram tratados
- 🌐 **Traduções** (README pra inglês/espanhol são especialmente úteis)
- 💡 **Novas skills** que complementem o kit (ex: `/export`, `/archive`, `/search`)
- 🎨 **Melhorias visuais** nos templates markdown

## O que NÃO é escopo

- Adicionar dependências pesadas (manter kit leve e sem instalação complexa)
- Opiniões sobre a estrutura do segundo cérebro — ela reflete uma abordagem específica testada em produção. Se quiser uma estrutura diferente, fork o projeto
- Mudanças que quebrem compatibilidade com Claude Code CLI
- Frameworks de JS/Python — stack é HTML/shell/markdown vanilla de propósito

## Como contribuir

1. **Fork** o repositório
2. Cria uma branch descritiva (`feat/obsidian-support`, `fix/install-wsl-path`)
3. Faz o commit seguindo [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`)
4. Abre um **Pull Request** com:
   - Descrição do problema/feature
   - O que a mudança faz
   - Como testar
5. Aguarda review — respondo em até 48h úteis

## Testando localmente

Antes de abrir PR, roda:

```bash
# Valida sintaxe dos shell scripts
bash -n install.sh
bash -n templates/scripts/brain-boot.sh

# Testa install.sh em ambiente limpo (VM, container ou pasta temp)
# Garanta que é idempotente: rode 2x sem quebrar
SECOND_BRAIN_PATH=/tmp/test-brain bash install.sh
SECOND_BRAIN_PATH=/tmp/test-brain bash install.sh

# Valida skill-audit em suas próprias mudanças de skill
python3 skills/skill-audit/scripts/audit.py <caminho-da-skill>/SKILL.md
```

## Skills novas

Pra submeter uma skill ao kit:

1. Estrutura: `skills/<nome-skill>/SKILL.md`
2. Roda `skill-audit` na sua skill — precisa passar em 10/10 QA checks V3
3. Adiciona exemplo de uso no PR
4. Se a skill precisa de config (tokens, paths), documenta isso no `SKILL.md`

## Reportar vulnerabilidades

Não abra issue pública. Ver [`SECURITY.md`](SECURITY.md).

## Código de conduta

Trate os outros como gostaria de ser tratado. Discussão técnica acima de personalismo. Se tiver dúvida, pergunta — se achar que algo tá errado, explica o porquê com respeito.

Comportamento tóxico (assédio, discriminação, ataques pessoais) leva a ban sem aviso.

---

Pra dúvidas que não caibam em issue: [`bruno@microsaas.com.br`](mailto:bruno@microsaas.com.br).
