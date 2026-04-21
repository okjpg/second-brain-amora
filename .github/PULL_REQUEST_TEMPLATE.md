<!-- Obrigado por contribuir! Segue o checklist rápido abaixo antes de abrir o PR. -->

## O que este PR faz
<!-- Descrição em 1-2 frases. Se fecha uma issue, referencia: "Closes #123" -->

## Tipo
- [ ] 🐛 Bug fix
- [ ] ✨ Feature nova
- [ ] 📚 Documentação
- [ ] 🧰 Chore / refactor
- [ ] 🎨 Melhoria visual/UX

## Como testar
<!-- Passos claros pra reviewer reproduzir e validar -->

```bash
# exemplo
bash -n install.sh
SECOND_BRAIN_PATH=/tmp/test-brain bash install.sh
```

## Checklist
- [ ] Rodei `bash -n` nos shell scripts modificados (sem erro de sintaxe)
- [ ] Se mexi em skill: rodei `skill-audit` e passou em 10/10
- [ ] Testei em pelo menos um SO (Mac OU Linux OU Windows+WSL)
- [ ] README atualizado se necessário
- [ ] Commit segue [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Não commitei credenciais, .env, ou paths pessoais

## Screenshots (se aplicável)
<!-- Antes/Depois, gifs, terminal output -->
