---
name: generate-report
description: >
  Generates weekly analytics reports from a CSV file with traffic data. Ativa
  quando o usuário diz "gera o weekly report", "roda o report semanal", "report
  da semana", "/generate-report", "monta o resumo semanal de tráfego", ou cola
  um path de CSV pedindo análise. Retorna markdown com top 5 fontes, delta vs
  semana anterior, e 3 insights priorizados. NÃO use para: reports mensais (usa
  `monthly-report`); análise ad-hoc de dados arbitrários (usa `data-explorer`);
  geração de gráficos visuais.
type: skill
category: analytics
status: ATIVO
version: 1.0
created: 2026-04-19
last_reviewed: 2026-04-19
estimated_time: 2min
model_compatible: [claude-sonnet-4, claude-opus-4, gpt-5, gpt-4o, gemini-pro]
---

# Generate Report

Generates weekly traffic reports from a CSV file. Compares current week vs
previous, ranks top traffic sources, extracts 3 actionable insights. Output is
markdown, ready to paste into email or Notion.

---

## When to Use

Aciona quando:
- Usuário cola path de um CSV e pede análise semanal
- Toda segunda-feira 9h (cron job chama esta skill)
- Usuário pede "weekly report" / "report da semana"

Exemplos literais:
- "gera o weekly report de /data/traffic.csv"
- "roda o report semanal"
- "/generate-report"

## When NOT to Use

NÃO aciona se:
- Usuário quer report mensal → `monthly-report`
- Usuário quer análise ad-hoc de dados arbitrários → `data-explorer`
- Usuário quer gráfico visual → `chart-builder`

---

## Inputs

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| csv_path | string | ✅ | Path absoluto do CSV. Colunas esperadas: date, source, visits |
| weeks_back | int | ❌ | Quantas semanas comparar (default: 1) |

## Outputs

| Campo | Tipo | Descrição |
|-------|------|-----------|
| report | markdown | Report formatado, 300-500 palavras |
| top_sources | array | Top 5 fontes com visits + % |
| delta | object | Variação vs semana anterior (visits, %) |
| insights | array | 3 strings priorizadas |

Formato de entrega: arquivo markdown em `./reports/weekly-YYYY-MM-DD.md`.

---

## Workflow

1. **Validar CSV** — abrir `csv_path`, confirmar colunas `date`, `source`, `visits`
2. **SE colunas faltando → abortar com erro específico**
3. **Filtrar semana atual** — últimos 7 dias
4. **Agrupar por source** — sum visits, sortear desc
5. **Filtrar semana anterior** — dias 8-14
6. **Calcular delta** — (atual - anterior) / anterior * 100
7. **Extrair top 5 sources** da lista agrupada
8. **Gerar 3 insights** baseados em: maior gain, maior loss, nova fonte
9. **Renderizar markdown** no template `reports/template.md`
10. **Salvar** em `./reports/weekly-{today}.md`
11. **Retornar** path do arquivo gerado

---

## Edge Cases

- **Se CSV vazio** → retornar report com "Sem dados disponíveis"
- **Se apenas 1 semana de histórico** → omitir delta, marcar "sem comparação"
- **Se mais de 50 sources** → agregar cauda em "Outros"
- **Se CSV com encoding errado** → tentar UTF-8 → Latin-1 → abortar

---

## Examples

### Example 1 — Happy path
**Input:** `generate-report /data/traffic.csv`
**Workflow:**
1. Abre CSV com 14 dias de dados, 8 sources
2. Top fonte: Google (5.2k visits, +12%)
3. Insight chave: novo source "ProductHunt" trouxe 800 visits

**Output:**
```markdown
# Weekly Report — 2026-04-19

**Total visits:** 12,340 (+8% vs semana anterior)

## Top 5 Sources
1. Google — 5,234 (42%)
2. Twitter — 2,108 (17%)
3. Direct — 1,890 (15%)
4. ProductHunt — 812 (7%) 🆕
5. LinkedIn — 754 (6%)

## Insights
- ProductHunt é nova fonte, 7% do tráfego total
- Twitter caiu 15% vs semana anterior — investigar
- Google cresceu +12%, provavelmente ganho de ranking
```

### Example 2 — Edge case (sem histórico)
**Input:** `generate-report /data/new-site.csv`
**Workflow:**
1. CSV tem só 5 dias, não dá pra comparar semana
2. Retorna report sem seção de delta

**Output:**
```markdown
# Weekly Report — 2026-04-19

**Total visits:** 420 (primeira semana — sem comparação)
...
```

---

## Dependencies

- **Libs:** Python stdlib (csv, datetime, pathlib)
- **Files:** `reports/template.md` (read-only)
- **Outras skills:** nenhuma

---

## Errors & Recovery

| Erro | Causa | Fix |
|------|-------|-----|
| `ColumnError: missing 'source'` | CSV sem coluna esperada | Verificar header do CSV |
| `UnicodeDecodeError` | Encoding não-UTF8 | Salvar CSV como UTF-8 |
| `PermissionError: reports/` | Pasta sem write | `chmod +w reports/` |

---

## Notes

Template do report em `reports/template.md` pode ser customizado. Campos entre
`{{ }}` são substituídos no step 9.

---

## Changelog

- v1.0 (2026-04-19): Versão inicial
