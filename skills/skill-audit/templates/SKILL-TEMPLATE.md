---
name: your-skill-name
description: >
  [50+ palavras em TERCEIRA PESSOA. Descrever o que a skill faz + quando disparar.
  Listar 5+ TRIGGER PHRASES explícitas que o usuário realmente digitaria —
  variações de fraseado, com e sem a palavra "skill", formal e informal.
  Incluir NEGATIVE BOUNDARIES no fim: "NÃO use para X, Y, Z." Quanto mais
  específico, maior a chance de acionar corretamente em Claude/GPT/Gemini.
  Exemplos: "faz X", "cria Y", "processa Z", "/nome-da-skill", "me ajuda com W".
  NÃO use para: [caso parecido 1], [caso parecido 2], [caso parecido 3].]
type: skill
category: your-category
status: ATIVO
version: 1.0
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
estimated_time: 5min
model_compatible: [claude-sonnet-4, claude-opus-4, gpt-5, gpt-4o, gemini-pro]
---

# Your Skill Name

[Overview escrito para o LLM (não pra humano): o que a skill faz, qual input
espera, qual output produz, em que contexto dispara. 3-5 linhas.]

---

## When to Use

Aciona quando:
- [Cenário 1 — específico, não genérico]
- [Cenário 2 — com variação de fraseado]
- [Cenário 3 — caso automático/cron se aplicável]

Exemplos literais de mensagens que devem disparar:
- "[exemplo real 1]"
- "[exemplo real 2]"
- "[exemplo real 3]"

## When NOT to Use

NÃO aciona se:
- [Caso confundível 1] → usar skill `{alternativa-1}`
- [Caso confundível 2] → usar skill `{alternativa-2}`
- [Caso fora de escopo] → [o que fazer em vez disso]

---

## Inputs

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| input_1 | string | ✅ | [o que esperar — formato, range, exemplo] |
| input_2 | string | ❌ | [opcional, default: X] |

## Outputs

| Campo | Tipo | Descrição |
|-------|------|-----------|
| output_1 | string | [formato exato] |
| output_2 | file | [path absoluto se gera arquivo] |

Formato de entrega: [markdown no chat / arquivo em {path} / etc]

---

## Workflow

Executar na ordem exata. Cada passo é UMA ação imperativa.

1. **[Verbo imperativo] [objeto]** — [comando exato se houver]
   ```bash
   comando exato aqui
   ```
2. **SE [condição explícita] → [ação]**
   SENÃO → [ação alternativa]
3. **[Ler / Extrair / Perguntar / Executar]** [o quê]
4. **Validar** que [resultado esperado bate com critério X]
5. **Entregar** output no formato [especificado]

### Regras do workflow

- Voz imperativa obrigatória: "Ler arquivo X", NÃO "O arquivo X deve ser lido"
- Condicionais explícitas: "SE [condição] → [ação]", NÃO "quando apropriado"
- Linguagem BANIDA: "handle appropriately", "format nicely", "as needed",
  "quando relevante", "se fizer sentido", "adaptar conforme contexto"

---

## Edge Cases

- **Se [input faltando]** → [ação: perguntar / default / abortar]
- **Se [formato errado]** → [ação]
- **Se [API/dependência fora]** → [fallback ou erro exato]
- **Se [condição ambígua]** → [regra de desempate]

---

## Examples

### Example 1 — Happy path
**Input real:** "[mensagem exata que o usuário digitaria]"
**Workflow executado:**
1. [passo com valores reais]
2. [passo]
3. [passo]
**Output real:**
```
[output literal, não descrição abstrata]
```

### Example 2 — Edge case
**Input:** "[input quebrado / ambíguo / parcial]"
**Workflow executado:**
1. [detecta problema]
2. [aplica fallback]
**Output:**
```
[como skill reage]
```

---

## Dependencies

- **APIs:** [Notion, Buffer, etc — "nenhuma" se vazio]
- **MCPs:** [nome do MCP server]
- **Env vars:** [VAR_NAME — onde está armazenada]
- **Files:** [paths absolutos que a skill lê/escreve]
- **Outras skills:** [chamadas por esta — ou "nenhuma"]

---

## Errors & Recovery

| Erro | Causa provável | Fix |
|------|----------------|-----|
| [msg exata] | [por que acontece] | [comando/ação pra resolver] |
| Timeout | [qual step] | [retry N vezes / fallback Y] |
| API 4xx | [creds expiradas / rate limit] | [revalidar / aguardar] |

---

## Notes

[Observações: limitações conhecidas, decisões de design, contexto histórico,
gotchas que o LLM precisa saber mas não são parte do workflow.]

---

## Changelog

- v1.0 (YYYY-MM-DD): Versão inicial.

---

## Estrutura de pastas

```
your-skill-name/
├── SKILL.md              ← este arquivo
└── evals/
    └── evals.json        ← mínimo 2 evals: 1 happy path + 1 edge case
```

Opcionais:
- `references/` — docs de apoio, specs, guias
- `scripts/` — código executável chamado pelo workflow
- `assets/` — templates, fontes, arquivos estáticos

### evals/evals.json (obrigatório)

```json
{
  "skill_name": "your-skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "input real do Example 1",
      "expected_output": "descrição concreta do output esperado"
    },
    {
      "id": 2,
      "prompt": "input real do Example 2 — edge case",
      "expected_output": "como skill deve reagir"
    }
  ]
}
```
