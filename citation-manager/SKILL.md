---
name: citation-manager
description: Academic citation management for QNFO research pipeline. Extract citations from Markdown, verify against BibTeX bibliographies, auto-generate BibTeX entries from DOIs, flag missing/unused citations, and produce citation verification reports. Use when user says "check my citations," "verify bibliography," "generate BibTeX entries," "are all citations accounted for," or when Phase 2 of LRAP requires citation validation before publication.
version: "1.1"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('citation-manager')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

> **Related:** deep-research, publication-publisher, literature-search

---

## Autonomous Continuation Protocol (v1.0)

**All citation stages execute autonomously.** Agent MUST: (1) chain extract→verify→BibTeX→report without user prompts, (2) tag `[AUTO-CONTINUE]` between stages, (3) flag `[BLOCKED: reason]` on failure. **ANTI-PATTERN:** User NEVER says "CONTINUE."

---

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Extract citations from Markdown/paper", "status": "pending"},
  {"step": "Verify citations against BibTeX bibliography", "status": "pending"},
  {"step": "Auto-generate missing BibTeX entries from DOIs", "status": "pending"},
  {"step": "Flag missing/unused citations", "status": "pending"},
  {"step": "Generate citation verification report", "status": "pending"}
])


# CITATION MANAGER SKILL — v1.0

> **Version:** v1.0 (Kaizen-audited 2026-07-05)

> **Version:** v1.0 (Kaizen-audited 2026-07-05)


> **Phase 2 gateway of LRAP.** Verifies that every citation in the paper text resolves to a bibliography entry and vice versa. Enables automated BibTeX generation from DOIs.

---

## Purpose

Eliminate the #1 source of academic paper errors: citation drift. Citations in text (e.g., `[@Smith2023]`) must match bibliography entries exactly. Missing citations produce dead references; unused bibliography entries bloat the references section. This skill automates extraction, cross-reference, and BibTeX generation.

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Verify my citations" | Full citation audit |
| "Generate BibTeX for these DOIs" | Batch BibTeX generation |
| "Are all `[@key]` entries in the bibliography?" | Cross-reference scan |
| "Clean up unused bibliography entries" | Unused entry removal |
| Phase 2 (Paper Writing) complete | Automatic gate check before Phase 3 |

## Workflow — 4 Stages

### Stage 1: Extract Citations from Paper Text

Scan the paper Markdown for all `[@key]` citation references:

```python
import re

def extract_citations(md_path: str) -> list[str]:
    """Extract all citation keys from [@key] references in Markdown."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Match [@key] or [@key1; @key2] patterns
    citations = re.findall(r'\[@(\w+(?:[,;\s]+@\w+)*)\]', text)
    
    keys = set()
    for group in citations:
        for key in re.findall(r'@(\w+)', f"@{group}"):
            keys.add(key)
    
    return sorted(keys)
```

### Stage 2: Extract Bibliography Entries

Parse the References/Bibliography section to extract BibTeX entries:

```python
def extract_bibliography(md_path: str) -> dict[str, str]:
    """Extract BibTeX entries from the bibliography section."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find bibliography section (common headings)
    bib_section = re.search(
        r'##\s+(?:References?|Bibliography|Works Cited)\s*\n(.*?)(?=\n##\s|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    
    if not bib_section:
        return {}
    
    bib_text = bib_section.group(1)
    entries = {}
    
    # Extract ```bibtex ... ``` blocks
    for match in re.finditer(r'```(?:bibtex)?\s*\n(.*?)```', bib_text, re.DOTALL):
        entry = match.group(1).strip()
        key_match = re.search(r'@\w+\{(\w+),', entry)
        if key_match:
            entries[key_match.group(1)] = entry
    
    # Also handle raw BibTeX (no code fences)
    for match in re.finditer(r'@\w+\{(\w+),.*?(?=\n@|\n\n|\Z)', bib_text, re.DOTALL):
        key = match.group(1)
        if key not in entries:
            entries[key] = match.group(0).strip()
    
    return entries
```

### Stage 3: Cross-Reference & Audit

Compare extracted citations against bibliography entries:

```python
def audit_citations(cited_keys: list[str], bib_entries: dict[str, str]) -> dict:
    """Cross-reference citations against bibliography."""
    cited_set = set(cited_keys)
    bib_set = set(bib_entries.keys())
    
    missing = cited_set - bib_set       # Cited but no bibliography entry
    unused = bib_set - cited_set        # In bibliography but never cited
    matched = cited_set & bib_set       # All good
    
    return {
        "total_cited": len(cited_set),
        "total_bib_entries": len(bib_set),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "unused": sorted(unused),
        "status": "PASS" if not missing else "FAIL",
        "report": generate_report(cited_set, bib_set, matched, missing, unused),
    }


def generate_report(cited, bib, matched, missing, unused) -> str:
    """Generate human-readable citation audit report."""
    lines = [
        "# CITATION AUDIT REPORT",
        f"**Date:** {datetime.now(timezone.utc).isoformat()}",
        "",
        f"| Metric | Count |",
        f"|:-------|:-----:|",
        f"| Citations in text | {len(cited)} |",
        f"| Bibliography entries | {len(bib)} |",
        f"| Matched (cited + in bibliography) | {len(matched)} |",
        f"| **Missing (cited but NO entry)** | **{len(missing)}** |",
        f"| Unused (in bibliography but NOT cited) | {len(unused)} |",
    ]
    
    if missing:
        lines.extend([
            "",
            "## ❌ MISSING CITATIONS (in text but not in bibliography)",
            "These citations are referenced in the paper but have no bibliography entry:",
            "",
        ])
        for key in missing:
            lines.append(f"- `@{key}` — No BibTeX entry found")
        lines.append(f"**Action:** Add BibTeX entries for {len(missing)} missing citations.")

    if unused:
        lines.extend([
            "",
            "## ⚠️ UNUSED BIBLIOGRAPHY ENTRIES",
            "These are in the bibliography but never cited in the paper text:",
            "",
        ])
        for key in unused:
            lines.append(f"- `@{key}` — Never cited in text")
        lines.append(f"**Action:** Either cite these {len(unused)} entries or remove them.")

    if not missing:
        lines.extend([
            "",
            "## ✅ ALL CITATIONS VERIFIED",
            f"All {len(cited)} citations in the text have matching bibliography entries.",
            f"No missing citations. ({len(unused)} unused entries in bibliography.)",
        ])
    
    return "\n".join(lines)
```

### Stage 4: BibTeX Generation from DOIs

For missing citations with DOIs, auto-generate BibTeX entries using the DOI API:

```python
def generate_bibtex_from_doi(doi: str) -> Optional[str]:
    """Generate BibTeX entry from DOI using Crossref API."""
    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/x-bibtex")
    req.add_header("User-Agent", "QNFO-CitationManager/1.0 (mailto:rwnquni@outlook.com)")
    
    try:
        response = urllib.request.urlopen(req, timeout=10)
        return response.read().decode("utf-8").strip()
    except Exception as e:
        print(f"[WARN] DOI lookup failed for {doi}: {e}", file=sys.stderr)
        return None
```

For citations without DOIs, generate stub BibTeX entries that the researcher fills in:

```python
def generate_stub_bibtex(citation_key: str, title_hint: str = "") -> str:
    """Generate a stub BibTeX entry for manual completion."""
    return f"""@misc{{{citation_key},
  author = {{[AUTHOR NEEDED]}},
  title = {{{title_hint or '[TITLE NEEDED]'}}},
  year = {{[YEAR NEEDED]}},
  note = {{[STUB — needs verification]}},
}}"""
```

---

## Embedded Script

### `scripts/citation_manager.py`

```python
#!/usr/bin/env python3
"""
Citation Manager — Verify and generate academic citations.
Usage: python citation_manager.py --paper paper.md --bibliography references.bib
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def extract_citations(text: str) -> list[str]:
    """Extract all citation keys from [@key] references in text."""
    citations = re.findall(r'\[@(\w+(?:[,;\s]+@\w+)*)\]', text)
    keys = set()
    for group in citations:
        for key in re.findall(r'@(\w+)', f"@{group}"):
            keys.add(key)
    return sorted(keys)


def extract_bib_keys(bib_text: str) -> dict[str, str]:
    """Extract BibTeX entry keys and full entries from bibliography text."""
    entries = {}
    
    # Extract ```bibtex ... ``` blocks
    for match in re.finditer(r'```(?:bibtex)?\s*\n(.*?)```', bib_text, re.DOTALL):
        entry = match.group(1).strip()
        key_match = re.search(r'@\w+\{(\w+),', entry)
        if key_match:
            entries[key_match.group(1)] = entry
    
    # Also handle raw @article{key, ... } blocks
    for match in re.finditer(r'@\w+\{(\w+),\s*\n?(.*?)\n\}', bib_text, re.DOTALL):
        key = match.group(1)
        if key not in entries:
            entries[key] = match.group(0).strip()
    
    return entries


def generate_bibtex_from_doi(doi: str) -> Optional[str]:
    """Generate BibTeX from DOI using Crossref API."""
    url = f"https://api.crossref.org/works/{doi.strip()}/transform/application/x-bibtex"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/x-bibtex")
    req.add_header("User-Agent", "QNFO-CitationManager/1.0 (mailto:rwnquni@outlook.com)")
    
    try:
        response = urllib.request.urlopen(req, timeout=10)
        bibtex = response.read().decode("utf-8").strip()
        return bibtex
    except Exception as e:
        print(f"[WARN] DOI lookup failed for {doi}: {e}", file=sys.stderr)
        return None


def run_audit(paper_path: str, bib_path: str = None) -> dict:
    """Run full citation audit."""
    with open(paper_path, 'r', encoding='utf-8') as f:
        paper_text = f.read()
    
    cited_keys = extract_citations(paper_text)
    
    if bib_path:
        with open(bib_path, 'r', encoding='utf-8') as f:
            bib_text = f.read()
    else:
        # Extract bibliography from the paper itself
        bib_section = re.search(
            r'##\s+(?:References?|Bibliography|Works Cited)\s*\n(.*?)(?=\n##\s|\Z)',
            paper_text, re.DOTALL | re.IGNORECASE
        )
        bib_text = bib_section.group(1) if bib_section else ""
    
    bib_entries = extract_bib_keys(bib_text)
    
    cited_set = set(cited_keys)
    bib_set = set(bib_entries.keys())
    
    missing = cited_set - bib_set
    unused = bib_set - cited_set
    matched = cited_set & bib_set
    
    # Try DOI lookup for missing entries
    repaired = {}
    for key in missing:
        # Search for DOI in the paper text near the citation
        cite_pattern = rf'\[@{re.escape(key)}\][\s\S]*?doi[:\s]*([^\s\n,]+)'
        doi_match = re.search(cite_pattern, paper_text, re.IGNORECASE)
        if doi_match:
            doi = doi_match.group(1).rstrip('.,;:')
            bibtex = generate_bibtex_from_doi(doi)
            if bibtex:
                repaired[key] = bibtex
                print(f"[REPAIRED] @{key} — BibTeX generated from DOI {doi}")
    
    return {
        "total_cited": len(cited_set),
        "total_bib_entries": len(bib_set),
        "matched_count": len(matched),
        "missing_count": len(missing),
        "unused_count": len(unused),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "unused": sorted(unused),
        "repaired": repaired,
        "status": "PASS" if not missing else "FAIL" if not repaired else "REPAIRED",
    }


def format_report(audit: dict) -> str:
    """Format audit results as Markdown report."""
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# CITATION AUDIT REPORT",
        f"**Date:** {now}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|:-------|:-----:|",
        f"| Citations in text | {audit['total_cited']} |",
        f"| Bibliography entries | {audit['total_bib_entries']} |",
        f"| ✅ Matched | {audit['matched_count']} |",
        f"| ❌ Missing (cited, no entry) | **{audit['missing_count']}** |",
        f"| ⚠️ Unused (entry, not cited) | {audit['unused_count']} |",
        f"| 🔧 Auto-repaired from DOI | {len(audit.get('repaired', {}))} |",
    ]

    if audit["missing"]:
        lines.extend([
            "",
            "## ❌ MISSING CITATIONS",
            "These are cited in the text but have NO bibliography entry:",
            "",
        ])
        for key in audit["missing"]:
            status = "🔧 [AUTO-REPAIRED]" if key in audit.get("repaired", {}) else "❌ [NEEDS MANUAL ENTRY]"
            lines.append(f"- `@{key}` — {status}")
        lines.append("")
        lines.append(f"**Action needed:** Add BibTeX entries for {len(audit['missing'])} citations.")

        if audit.get("repaired"):
            lines.extend([
                "### Auto-Repaired BibTeX Entries",
                "",
                "```bibtex",
            ])
            for key, bibtex in audit["repaired"].items():
                lines.append(f"% @{key}")
                lines.append(bibtex)
                lines.append("")
            lines.append("```")
            lines.append("**Review these auto-generated entries for accuracy.**")

    if audit["unused"]:
        lines.extend([
            "",
            "## ⚠️ UNUSED BIBLIOGRAPHY ENTRIES",
            "In bibliography but never cited in the text:",
            "",
        ])
        for key in audit["unused"]:
            lines.append(f"- `@{key}`")
        lines.append(f"\n**Action:** Either cite these {len(audit['unused'])} entries or remove them.")

    if audit["status"] == "PASS":
        lines.extend([
            "",
            "## ✅ ALL CITATIONS VERIFIED",
            f"All {audit['total_cited']} citations have matching bibliography entries.",
        ])
    elif audit["status"] == "REPAIRED":
        lines.extend([
            "",
            "## 🔧 CITATIONS AUTO-REPAIRED",
            f"{len(audit.get('repaired', {}))} of {audit['missing_count']} missing citations were auto-repaired from DOIs.",
            f"{audit['missing_count'] - len(audit.get('repaired', {}))} still need manual BibTeX entries.",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Verify and manage academic citations")
    parser.add_argument("--paper", "-p", required=True, help="Path to paper Markdown file")
    parser.add_argument("--bib", "-b", help="Path to separate bibliography file (optional)")
    parser.add_argument("--output", "-o", default="citation-audit.md", help="Output report path")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of report")
    parser.add_argument("--fix", action="store_true", help="Auto-fix missing citations by appending repaired BibTeX")
    args = parser.parse_args()

    audit = run_audit(args.paper, args.bib)

    if args.json:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
        return

    report = format_report(audit)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n[{'PASS' if audit['status'] == 'PASS' else 'ACTION NEEDED'}] Report written to {args.output}")
    
    if audit["status"] != "PASS":
        if audit["repaired"]:
            print(f"[REPAIRED] {len(audit['repaired'])} citations auto-repaired from DOIs")
        remaining = audit["missing_count"] - len(audit.get("repaired", {}))
        if remaining > 0:
            print(f"[BLOCKED] {remaining} citations still missing bibliography entries")
        sys.exit(1 if remaining > 0 else 0)
    sys.exit(0)


if __name__ == "__main__":
    main()
```

### Dependencies
- Python 3.8+ (standard library only)
- Crossref DOI API (free, no key required, rate-limited to 50 req/s)

### Usage

```bash
# Verify citations in paper
python citation_manager.py --paper paper.md

# Verify against separate bibliography file
python citation_manager.py --paper paper.md --bib references.bib

# Output JSON for pipeline integration
python citation_manager.py --paper paper.md --json

# Auto-repair missing citations from DOIs
python citation_manager.py --paper paper.md --fix
```

---

## Integration Points

| Upstream Skill | How It Feeds Citation Manager |
|:---------------|:------------------------------|
| `literature-search` | Provides DOIs → auto-generate BibTeX entries for new papers |
| `research-orchestrator` | Calls this skill as Phase 2 gateway |

| Downstream Skill | How Citation Manager Enables It |
|:-----------------|:-------------------------------|
| `fabrication-audit` | Verified citations → cross-reference claims against sources |
| `publication-publisher` | Clean bibliography → artifact-ready paper |
## Handoff Protocol (MANDATORY at Closeout)

1. **Verify** ALL execute_plan items marked [EXECUTED] with tool evidence (Test-Path, exec output, git log)
2. **Archive** session artifacts to R2 canonical storage: `npx wrangler r2 object put qnfo/audit/... --remote --file=<artifact>`
3. **Generate** continuation prompt documenting pending work and current state for the next session
4. **Clean up** ephemeral _* files and __pycache__ directories: `Remove-Item _* -Recurse -Force`

### Continuation Prompt Template
```
TASK: [description of pending work from execute_plan]
STATE: [current state — what's executed, what's blocked, why]
NEXT: [first executable action for the next session]
R2: [canonical path for session artifacts]
```


## Closeout Protocol (MANDATORY)

Before declaring this skill workflow complete:
1. **Task Execution Verification:** Compare planned tasks ([PENDING] in execute_plan) vs executed tasks ([EXECUTED] with evidence)
2. **Filesystem Verification:** `Test-Path <file>` for every file claimed as created/modified. Never claim from memory.
3. **Git Verification:** `git log -1 --oneline` for every commit claimed. Verify commit hash exists.
4. **R2 State Upload:** Upload session audit trail to `qnfo/audit/` — conversations, decisions, state files.
5. **Discovery Index Update:** Update `qnfo/discovery/index.json` with any new resources created, projects modified, or publications generated.
6. **Ephemeral Cleanup:** Delete ALL _* prefixed files and __pycache__ directories. Session is not complete until `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }` returns zero results.
