# 10 QA Checks — V3 Skill Standard

> Every `SKILL.md` must pass these 10 checks before being marked ATIVO.
> Failing skills don't trigger reliably in non-Claude LLMs (GPT, Gemini).

---

## The 10 critical checks

```
□ 1. Name in kebab-case and matches folder name
□ 2. Description has 50+ words, third person, 5+ trigger phrases, negative boundaries
□ 3. Every Workflow step is a single, imperative, unambiguous action
□ 4. At least 2 concrete examples (real input → real output)
□ 5. Edge Cases covered (3+ conditions with specific action)
□ 6. Output Format explicitly defined (structure, sections, delivery)
□ 7. Zero vague language ("handle appropriately", "format nicely", "as needed",
     "quando relevante", "se fizer sentido" — all FORBIDDEN)
□ 8. Negative boundaries also in body (## When NOT to Use section)
□ 9. Zero hardcoded credentials/secrets (use env var or secret manager)
□ 10. evals/ folder exists with 2+ evals (1 happy path + 1 edge case)
```

Score 7+ = trigger-reliable. Score 10 = ideal.

---

## Forbidden language (regex patterns)

Workflow and body cannot contain (case-insensitive):

```
handle appropriately
format nicely
as needed
quando relevante
se fizer sentido
adaptar conforme (o )?contexto
apropriadamente
adequadamente
de forma apropriada
conforme necessário
```

These phrases leave execution up to the LLM's guessing. Non-Claude models
(especially GPT-5, Gemini) will produce inconsistent results.

---

## Required sections (H2)

Every V3 skill has these 13 sections in this order:

1. Frontmatter YAML (with expanded description + 5+ triggers + negatives)
2. `# Skill Name` + overview paragraph (3-5 lines, for the LLM)
3. `## When to Use` (3+ scenarios + literal user messages)
4. `## When NOT to Use` (confusable cases + alternative skills)
5. `## Inputs` (table: param / type / required / description)
6. `## Outputs` (table: field / type / description + delivery format)
7. `## Workflow` (numbered imperative steps, SE/SENÃO explicit)
8. `## Edge Cases` (3+ conditions with specific action)
9. `## Examples` (2+ H3 with real input/output)
10. `## Dependencies` (APIs, MCPs, env vars, files, other skills)
11. `## Errors & Recovery` (error / cause / fix table)
12. `## Notes` (optional — limitations, design decisions)
13. `## Changelog` (versions with date)

---

## Description checklist (YAML)

The `description:` field is the single most important trigger for LLM
routing. It must:

- Use `description: >` (block scalar) for multi-line
- Be written in **third person** ("Processes...", not "I process...")
- Have **50+ words** of substantive content
- List **5+ trigger phrases** explicitly in quotes or as `/command`
- End with **negative boundaries**: "NÃO use para: X, Y, Z."
- Be specific, not generic — a description that could apply to 10 skills is a
  description that triggers for none of them

---

## evals/evals.json format

Minimum structure:

```json
{
  "skill_name": "your-skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "real user input that should trigger this skill",
      "expected_output": "concrete description of what skill should produce"
    },
    {
      "id": 2,
      "prompt": "edge case input (broken, partial, ambiguous)",
      "expected_output": "how skill should react"
    }
  ]
}
```

Minimum 2 evals per skill: 1 happy path + 1 edge case.

---

## Issue codes (emitted by audit.py)

| Code | Meaning | Fix |
|------|---------|-----|
| `missing_frontmatter` | No YAML block | Add `---` frontmatter |
| `invalid_name` | Name has uppercase/spaces/underscores | Rename to kebab-case |
| `name_folder_mismatch` | `name:` in YAML ≠ folder name | Sync them |
| `desc_too_short` | Description < 50 words | Expand with triggers + boundaries |
| `desc_no_triggers` | < 5 trigger phrases quoted | Add variations of user phrasing |
| `desc_no_negatives` | No "NÃO use" / "not use" | Append negative boundaries |
| `desc_first_person` | "Eu crio..." / "I process..." | Rewrite in third person |
| `no_workflow_section` | Missing `## Workflow` | Add section |
| `workflow_vague` | Banned language in Workflow | Rewrite specific + imperative |
| `examples_too_few` | < 2 H3 in `## Examples` | Add 2+ examples with real I/O |
| `edge_cases_few` | < 3 bullets in `## Edge Cases` | Add more failure scenarios |
| `no_output_format` | `## Outputs` missing or thin | Add table + delivery format |
| `vague_lang` | Banned language anywhere in body | Remove/replace |
| `no_when_not_to_use` | `## When NOT to Use` absent | Add section |
| `hardcoded_secret` | API key/token in file | Move to env var / secret manager |
| `no_evals_folder` | No `evals/evals.json` | Create file with 2+ evals |
| `broken_refs` | Link `[x](path)` to non-existent file | Remove or fix path |
| `long` | > 350 lines | Move content to `references/` |

---

## When to care about borderline scores (6-7)

Trigger phrase detection uses heuristics (quoted strings + `/commands`). In
dense technical descriptions, false positives happen. If your skill scores 6-7
but the issues look cosmetic, read the issue list manually before spending
time on cleanup.

Score 4-5: almost always real structural problems, fix before shipping.
Score ≤ 3: skill needs rewrite, not polish.
