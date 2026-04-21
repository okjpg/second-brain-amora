# Como gravar o GIF do /cerebro

Instruções pra regravar o GIF que aparece no README (`docs/cerebro-demo.gif`).

## Abordagem recomendada — vhs (Charmbracelet)

Instalação (Mac):
```bash
brew install vhs ttyd ffmpeg
```

Roda na raiz do repo:
```bash
vhs docs/cerebro-demo.tape
```

O output vai pra `docs/cerebro-demo.gif` automaticamente.

### Script `docs/cerebro-demo.tape` (exemplo)

```tape
Output docs/cerebro-demo.gif

Set FontSize 14
Set Width 1200
Set Height 700
Set Theme "Dracula"

Type "claude"
Enter
Sleep 2s

Type "/cerebro"
Enter
Sleep 8s
```

Ajusta `Sleep` de acordo com o tempo real do briefing carregar.

## Alternativa — asciinema + agg

Se não quiser instalar vhs:

```bash
brew install asciinema agg

# Grava
asciinema rec demo.cast
# (roda /cerebro, espera terminar, Ctrl+D pra parar)

# Converte pra GIF
agg demo.cast docs/cerebro-demo.gif
```

## Dicas

- **Não vaze dados sensíveis:** se o briefing mostra pendências/pessoas reais, considere:
  - Rodar num segundo cérebro com dados fake
  - Ou blur/edit o GIF final com alguma ferramenta (`giflossy`, `ezgif.com`)
- **Tamanho alvo:** <2MB pra carregar rápido no GitHub. Se ultrapassar, reduz resolução ou FPS.
- **Velocidade:** 1x é chato, 2x-3x fica mais dinâmico. vhs ajusta com `Set PlaybackSpeed 2.0`.

## Regravação

Quando evoluir o /cerebro (ex: novas seções Agendados / Onde paramos / Projetos WIP), regravar:
1. Edita `docs/cerebro-demo.tape` se precisar
2. Roda `vhs docs/cerebro-demo.tape`
3. Commit do novo `docs/cerebro-demo.gif`
