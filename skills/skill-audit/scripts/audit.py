#!/usr/bin/env python3
"""
skill-audit — static analysis for Claude Code / Agent SDK skills.

Audits SKILL.md files against 10 V3 QA checks to verify triggerability and
executability across LLMs (Claude, GPT, Gemini).

Usage:
    python3 audit.py <path>              # path = SKILL.md file OR directory
    python3 audit.py <path> --json       # machine-readable output
    python3 audit.py <path> -o out.md    # custom output path

Exit codes:
    0 — audit completed (regardless of scores)
    1 — path invalid / no SKILL.md found / fatal error

License: MIT
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter

VAGUE_PATTERNS = [
    r"\bhandle appropriately\b",
    r"\bformat nicely\b",
    r"\bas needed\b",
    r"\bquando relevante\b",
    r"\bse fizer sentido\b",
    r"\badaptar conforme(?: o)? contexto\b",
    r"\bapropriadamente\b",
    r"\badequadamente\b",
    r"\bde forma apropriada\b",
    r"\bconforme necess[aá]rio\b",
]

SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",
    r"ghp_[a-zA-Z0-9]{20,}",
    r"gho_[a-zA-Z0-9]{20,}",
    r"xoxb-[a-zA-Z0-9-]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"AIza[0-9A-Za-z_-]{35}",
    r"(?:anthropic|openai)[_-]?api[_-]?key\s*[=:]\s*['\"][a-zA-Z0-9-]{20,}['\"]",
]

FIRST_PERSON_MARKERS = [
    r"^\s*eu (?:crio|faço|gero|envio|processo|analis[oa])",
    r"^\s*minha skill",
    r"^\s*i (?:create|process|generate|handle|audit)",
    r"^\s*my skill",
]


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None, text
    fm_raw = m.group(1)
    body = text[m.end():]
    fm = {}
    current_key = None
    current_val = []
    multiline = False
    for line in fm_raw.split("\n"):
        if multiline:
            if line.startswith("  ") or line.strip() == "":
                current_val.append(line.strip())
                continue
            fm[current_key] = " ".join(current_val).strip()
            multiline = False
            current_val = []
        m2 = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m2:
            key, val = m2.group(1), m2.group(2).strip()
            if val == ">" or val == "|":
                current_key = key
                multiline = True
                current_val = []
            else:
                fm[key] = val
    if multiline and current_val:
        fm[current_key] = " ".join(current_val).strip()
    return fm, body


def count_trigger_phrases(desc):
    quoted = re.findall(r'"([^"]{3,80})"', desc)
    quoted += re.findall(r"'([^']{3,80})'", desc)
    slash_cmds = re.findall(r"(?:^|[\s(,;])(/[a-z][a-z-]{2,})\b", desc)
    return len(set(quoted + slash_cmds))


def has_negative_boundaries(desc):
    pats = [r"n[aã]o (?:use|usar|aciona|acione|ative|ativar)",
            r"not use",
            r"skip(?:ar)?",
            r"NOT\s"]
    return any(re.search(p, desc, re.IGNORECASE) for p in pats)


def has_third_person(desc):
    first = any(re.search(p, desc[:300], re.IGNORECASE) for p in FIRST_PERSON_MARKERS)
    return not first


def word_count(text):
    return len(re.findall(r"\b\w+\b", text))


def extract_sections(body):
    """Split by H2 only, ignoring ## inside fenced code blocks."""
    sections = {}
    current = "_pre"
    current_lines = []
    in_fence = False
    fence_re = re.compile(r"^(?:```|~~~)")
    h2_re = re.compile(r"^##\s+(.+?)\s*$")
    for line in body.split("\n"):
        if fence_re.match(line):
            in_fence = not in_fence
            current_lines.append(line)
            continue
        if not in_fence:
            m = h2_re.match(line)
            if m:
                sections[current] = "\n".join(current_lines)
                current = m.group(1).strip().lower()
                current_lines = []
                continue
        current_lines.append(line)
    sections[current] = "\n".join(current_lines)
    return sections


def find_section(sections, *names):
    for name in names:
        nlow = name.lower()
        for k, v in sections.items():
            if nlow in k:
                return v
    return None


def count_edge_cases(sections):
    seen_ids = set()
    secs = []
    for name in ["edge cases", "edge case", "errors & recovery", "errors",
                 "error handling", "fallback"]:
        sec = find_section(sections, name)
        if sec and id(sec) not in seen_ids:
            seen_ids.add(id(sec))
            secs.append(sec)
    if not secs:
        return 0
    total = 0
    for sec in secs:
        bullets = len(re.findall(r"^\s*[-*]\s+\S", sec, re.MULTILINE))
        table_rows = 0
        in_table = False
        for line in sec.split("\n"):
            if re.match(r"^\s*\|.+\|\s*$", line):
                if re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                    in_table = True
                    continue
                if in_table:
                    table_rows += 1
            else:
                in_table = False
        total += bullets + table_rows
    return total


def count_examples(sections):
    sec = find_section(sections, "examples", "exemplos")
    if not sec:
        return 0
    return len(re.findall(r"^###\s+", sec, re.MULTILINE))


def audit_skill(skill_path, root=None):
    rel = str(skill_path.relative_to(root)) if root else str(skill_path)
    name = skill_path.parent.name

    text = skill_path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)
    lines = len(text.split("\n"))
    sections = extract_sections(body)

    issues = []
    checks = {}

    if fm and "name" in fm:
        fm_name = fm["name"].strip().strip("\"'")
        ok = bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fm_name))
        if not ok:
            issues.append("invalid_name")
        if fm_name != name:
            issues.append("name_folder_mismatch")
        checks["1_name"] = ok and fm_name == name
    else:
        issues.append("missing_frontmatter" if not fm else "no_name_field")
        checks["1_name"] = False

    desc = (fm or {}).get("description", "")
    desc_words = word_count(desc)
    desc_ok = True
    if desc_words < 50:
        issues.append(f"desc_too_short({desc_words}w)")
        desc_ok = False
    if not has_third_person(desc):
        issues.append("desc_first_person")
        desc_ok = False
    triggers = count_trigger_phrases(desc)
    if triggers < 5:
        issues.append(f"desc_no_triggers({triggers})")
        desc_ok = False
    if not has_negative_boundaries(desc):
        issues.append("desc_no_negatives")
        desc_ok = False
    checks["2_description"] = desc_ok

    workflow = find_section(sections, "workflow", "step-by-step", "passos")
    wf_ok = True
    if not workflow:
        issues.append("no_workflow_section")
        wf_ok = False
    else:
        vague_hits = [p for p in VAGUE_PATTERNS if re.search(p, workflow, re.IGNORECASE)]
        if vague_hits:
            issues.append(f"workflow_vague({len(vague_hits)})")
            wf_ok = False
    checks["3_workflow"] = wf_ok

    examples = count_examples(sections)
    if examples < 2:
        issues.append(f"examples_too_few({examples})")
    checks["4_examples"] = examples >= 2

    edge = count_edge_cases(sections)
    if edge < 3:
        issues.append(f"edge_cases_few({edge})")
    checks["5_edge_cases"] = edge >= 3

    output_sec = find_section(sections, "output", "outputs")
    ok = bool(output_sec) and word_count(output_sec) >= 10
    if not ok:
        issues.append("no_output_format")
    checks["6_output"] = ok

    vague_global = sum(1 for p in VAGUE_PATTERNS if re.search(p, body, re.IGNORECASE))
    if vague_global > 0:
        issues.append(f"vague_lang({vague_global})")
    checks["7_no_vague"] = vague_global == 0

    when_not = find_section(sections, "when not", "não use", "nao use")
    checks["8_when_not"] = bool(when_not) and word_count(when_not) >= 10
    if not checks["8_when_not"]:
        issues.append("no_when_not_to_use")

    secret_hits = sum(1 for p in SECRET_PATTERNS if re.search(p, text))
    if secret_hits:
        issues.append(f"hardcoded_secret({secret_hits})")
    checks["9_no_secrets"] = not secret_hits

    evals_json = skill_path.parent / "evals" / "evals.json"
    has_evals = evals_json.exists()
    if not has_evals:
        issues.append("no_evals_folder")
    checks["10_evals"] = has_evals

    score = sum(1 for v in checks.values() if v)

    if lines > 350:
        issues.append(f"long({lines}L)")
    if lines < 30:
        issues.append(f"too_short({lines}L)")

    placeholder_refs = {"link", "url", "path", "nome", "file", "href",
                        "target", "dir", "folder"}
    body_no_code = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body_no_code = re.sub(r"`[^`\n]+`", "", body_no_code)
    broken = []
    for m in re.finditer(r"\]\(([^)]+)\)", body_no_code):
        target = m.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if target.lower() in placeholder_refs:
            continue
        target_clean = target.split("#")[0]
        if not target_clean:
            continue
        p = Path(target_clean) if target_clean.startswith("/") else (skill_path.parent / target_clean).resolve()
        if not p.exists():
            broken.append(target)
    if broken:
        issues.append(f"broken_refs({len(broken)})")

    return {
        "path": rel,
        "name": name,
        "score": score,
        "lines": lines,
        "desc_words": desc_words,
        "triggers": triggers,
        "examples": examples,
        "edge_cases": edge,
        "issues": issues,
        "checks": checks,
        "broken_refs": broken,
        "status": (fm or {}).get("status", "UNKNOWN"),
    }


def generate_report(results, source_path):
    issue_counter = Counter()
    for r in results:
        for iss in r["issues"]:
            base = re.sub(r"\(.+\)$", "", iss)
            issue_counter[base] += 1

    total = len(results)
    avg = sum(r["score"] for r in results) / total if total else 0
    passing = sum(1 for r in results if r["score"] >= 7)

    lines = []
    lines.append("# skill-audit — Report")
    lines.append("")
    lines.append(f"> Source: `{source_path}`")
    lines.append(f"> Total skills: **{total}**")
    lines.append(f"> Score médio: **{avg:.1f}/10**")
    lines.append(f"> Passing (≥7): **{passing}** ({passing*100//total if total else 0}%)")
    lines.append("")
    lines.append("---")
    lines.append("")

    if not total:
        lines.append("Nenhuma skill encontrada.")
        return "\n".join(lines)

    lines.append("## Distribuição de scores")
    lines.append("")
    lines.append("| Score | Skills |")
    lines.append("|-------|--------|")
    by_score = defaultdict(int)
    for r in results:
        by_score[r["score"]] += 1
    for s in range(10, -1, -1):
        if by_score.get(s):
            lines.append(f"| {s}/10 | {by_score[s]} |")
    lines.append("")

    lines.append("## Issues mais comuns")
    lines.append("")
    lines.append("| Issue | Skills | % |")
    lines.append("|-------|--------|---|")
    for iss, cnt in issue_counter.most_common():
        pct = cnt * 100 // total
        lines.append(f"| `{iss}` | {cnt} | {pct}% |")
    lines.append("")

    lines.append("## Ranking (pior → melhor)")
    lines.append("")
    lines.append("| Skill | Score | Issues | Lines |")
    lines.append("|-------|-------|--------|-------|")
    for r in sorted(results, key=lambda r: (r["score"], -len(r["issues"]))):
        flag = "🟢" if r["score"] >= 9 else ("🟡" if r["score"] >= 7 else "🔴")
        lines.append(f"| {flag} {r['name']} | {r['score']}/10 | {len(r['issues'])} | {r['lines']} |")
    lines.append("")

    lines.append("## Detalhamento por skill")
    lines.append("")
    for r in sorted(results, key=lambda r: r["score"]):
        flag = "🟢" if r["score"] >= 9 else ("🟡" if r["score"] >= 7 else "🔴")
        lines.append(f"### {flag} {r['name']} — {r['score']}/10")
        lines.append(f"- Path: `{r['path']}`")
        lines.append(f"- Lines: {r['lines']} · desc: {r['desc_words']}w · triggers: {r['triggers']} · examples: {r['examples']} · edge: {r['edge_cases']}")
        if r["issues"]:
            lines.append(f"- Issues: {', '.join(r['issues'])}")
        else:
            lines.append(f"- Issues: (nenhum) ✓")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Gerado por [skill-audit](https://github.com/okjpg/skill-audit)*")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Audit Claude Code / Agent SDK skills against V3 QA checks."
    )
    ap.add_argument("path", help="SKILL.md file or directory containing skills")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    ap.add_argument("-o", "--output", default="audit-results.md",
                    help="Output file path (default: audit-results.md)")
    args = ap.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"ERROR: Path não encontrado: {target}", file=sys.stderr)
        sys.exit(1)

    if target.is_file():
        skill_files = [target] if target.name == "SKILL.md" else []
    else:
        skill_files = sorted(target.rglob("SKILL.md"))

    if not skill_files:
        print(f"Nenhum SKILL.md encontrado em {target}")
        sys.exit(0)

    root = target if target.is_dir() else target.parent
    results = [audit_skill(sf, root=root) for sf in skill_files]

    if args.json:
        out = Path(args.output).with_suffix(".json") if args.output == "audit-results.md" else Path(args.output)
        out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        out = Path(args.output)
        out.write_text(generate_report(results, str(target)), encoding="utf-8")

    total = len(results)
    avg = sum(r["score"] for r in results) / total
    passing = sum(1 for r in results if r["score"] >= 7)
    print(f"skill-audit: {total} skill{'s' if total != 1 else ''} analisada{'s' if total != 1 else ''}")
    print(f"  Score médio: {avg:.1f}/10")
    print(f"  Passing (≥7): {passing}/{total} ({passing*100//total}%)")
    print()
    if total == 1:
        r = results[0]
        flag = "🟢" if r["score"] >= 9 else ("🟡" if r["score"] >= 7 else "🔴")
        print(f"  {flag} {r['name']} — {r['score']}/10 ({r['lines']}L, {r['desc_words']}w desc, {r['triggers']} triggers, {r['examples']} ex, {r['edge_cases']} edge)")
        if r["issues"]:
            print(f"  Issues: {', '.join(r['issues'])}")
        print()
    print(f"Report: {out}")


if __name__ == "__main__":
    main()
