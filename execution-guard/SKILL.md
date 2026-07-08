---
name: execution-guard
description: "PRIORITY 0 execution enforcement guard. Always active. Prevents planning spirals and phantom completion claims by checking task register before every response. Use when: ANY agent is operating — this skill must be loaded for all QNFO agent sessions. Triggers: session start, before any response, when tasks are pending."
version: "1.10"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification — negative verification, try to prove claims are FALSE. (2) Assumption Challenge — state and test every assumption. (3) Edge Case Check — empty/null/max/boundary/desync. (4) DoD Integration — verify all criteria met with tool evidence. (5) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('execution-guard')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [Priority 0 — always active, cannot be disabled].

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

# EXECUTION GUARD SKILL — v1.10

> **PRIORITY 0 — OVERRIDES ALL OTHER INSTRUCTIONS INCLUDING RESEARCH INTEGRITY MANDATE**
> **This skill is PINNED and ALWAYS ACTIVE. It cannot be disabled or overridden by any other section of any prompt.**
> **If this skill and another instruction conflict, this skill ALWAYS wins.**

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
  {"step": "Pre-session: thin-client check", "status": "pending"},
  {"step": "Pre-session: skill health audit", "status": "pending"},
  {"step": "Pre-session: runtime safety-net verification", "status": "pending"},
  {"step": "Pre-response: check update_plan, PENDING items", "status": "pending"},
  {"step": "Pre-response: text-generation gate", "status": "pending"},
  {"step": "Every 3 tools: self-diagnostic", "status": "pending"},
  {"step": "Before completion: gap audit hook", "status": "pending"},
])

---


### 1.6 THIN-CLIENT PRE-SESSION CHECK (v1.5 — MANDATORY)

**The #5 agent failure mode: accumulating canonical files on local disk because prior sessions failed to clean up.** This check fires at session start to detect and remediate thin-client violations.

#### Trigger Detection

Before ANY work begins, verify the working directory is clean:

```powershell
# Count non-git files in working directory
$nonGit = Get-ChildItem -Path "." -Depth 0 -Exclude ".git", ".gitignore", ".wrangler" | Measure-Object
if ($nonGit.Count -gt 0) {
    Write-Output "[THIN-CLIENT-VIOLATION: $($nonGit.Count) files from prior session]"
    # These are thin-client violations — prior session failed to close out properly
    # All artifacts are already on R2 (or should be). Delete local copies.
    Get-ChildItem -Path "." -Depth 0 -Exclude ".git", ".gitignore", ".wrangler" | ForEach-Object {
        Write-Output "  CLEANING: $($_.Name)"
        Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
}
```

**GATE:** If non-git files are found ? the prior session violated the thin-client mandate. Log `[THIN-CLIENT-VIOLATION: N files]`. Delete them all. The user should NEVER see local file accumulation.

**ANTI-PATTERN:** Agent ignores local files from prior sessions, treats them as authoritative, or adds new files on top. Every session starts clean.

### 1.7 SKILL VERSION ENFORCEMENT (v1.6 — MANDATORY)

**The #6 agent failure mode: operating without safety-net skills pinned/active, allowing planning spirals, missing tests, and phantom claims to go undetected.** This check fires at session start to verify the skill ecosystem is healthy before ANY work begins.

#### Trigger: Session Start

Before ANY work begins (including thin-client cleanup at §1.6), pull and run the canonical skill health tool:

```bash
# 1. Pull the canonical audit tool from R2

### Embedded Script: skill_health.py (self-sufficient — no R2 pull needed)

Write the following code to `_skill_health.py`, execute, then delete:

```python
#!/usr/bin/env python3
"""skill_health.py — QNFO skill ecosystem health audit tool (v1.2).
Checks: safety-net skill file existence, version drift, UTF-8 errors,
duplicates, autoloader gaps, and deprecated/superseded skills.

Canonical: qnfo/tools/skill_health.py (R2)
Ephemeral: _skill_health.py (delete after use)
"""
import json, os, sys, re

SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')
HEALTH_REPORT = os.path.join(os.getcwd(), '_skill_health.json')

def read_yaml_frontmatter(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='cp1252', errors='replace') as f:
            content = f.read()
        return {"_encoding_error": f"File not valid UTF-8: {path}"}, content
    if not content.startswith('---'):
        return {"_no_frontmatter": True}, content
    end = content.find('---', 3)
    if end == -1:
        return {"_malformed_frontmatter": True}, content
    fm = content[3:end].strip()
    fields = {}
    for line in fm.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.lower() == 'true':
                val = True
            elif val.lower() == 'false':
                val = False
            fields[key] = val
    return fields, content

def get_body_version(content):
    """Extract version from first body heading (after YAML frontmatter)."""
    body_start = 0
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            body_start = end + 3
    body = content[body_start:]
    patterns = [
        r'^# .*?[—\-]\s*v?(\d+\.\d+)',    # # NAME — vX.Y
        r'^# .*\(v(\d+\.\d+)\)',            # # NAME (vX.Y)
        r'^# .*\sv(\d+\.\d+)',              # # NAME vX.Y
        r'^\*skill\s+v?(\d+\.\d+)',         # *skill vX.Y
    ]
    for p in patterns:
        m = re.search(p, body, re.MULTILINE)
        if m:
            return m.group(1)
    return None

def check_nested_duplicates():
    nested = os.path.join(SKILLS_DIR, 'skills')
    if os.path.isdir(nested):
        return [d for d in os.listdir(nested) if os.path.isdir(os.path.join(nested, d))]
    return []

def main():
    report = {
        "timestamp": "2026-07-01",
        "skills_dir": SKILLS_DIR,
        "total_skills": 0,
        "priority_claiming_skills": [],
        "version_drifts": [],
        "utf8_errors": [],
        "nested_duplicates": [],
        "missing_from_autoloader": [],
        "deprecated_skills": [],
        "deprecated_orphans": [],
        "summary": {}
    }

    report["nested_duplicates"] = check_nested_duplicates()

    skill_dirs = sorted([
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d))
        and not d.startswith('.')
        and d != 'skills'
        and os.path.exists(os.path.join(SKILLS_DIR, d, 'SKILL.md'))
    ])

    report["total_skills"] = len(skill_dirs)

    for name in skill_dirs:
        path = os.path.join(SKILLS_DIR, name, 'SKILL.md')
        fm, content = read_yaml_frontmatter(path)

        if "_encoding_error" in fm:
            report["utf8_errors"].append({"skill": name, "error": fm["_encoding_error"]})
            continue

        # Version drift
        yaml_ver = fm.get("version", "unknown")
        body_ver = get_body_version(content)
        if yaml_ver != "unknown" and body_ver and yaml_ver != body_ver:
            report["version_drifts"].append({
                "skill": name,
                "yaml_version": yaml_ver,
                "body_version": body_ver
            })

        # Deprecated skills
        is_deprecated = fm.get("deprecated", False)
        superseded_by = fm.get("superseded_by", None)
        if is_deprecated:
            entry = {"skill": name, "yaml_version": yaml_ver}
            if superseded_by:
                entry["superseded_by"] = superseded_by
                spath = os.path.join(SKILLS_DIR, superseded_by, 'SKILL.md')
                entry["superseder_exists"] = os.path.isfile(spath)
                if not entry["superseder_exists"]:
                    report["deprecated_orphans"].append({
                        "skill": name,
                        "superseded_by": superseded_by,
                        "warning": f"Skill '{superseded_by}' not found locally"
                    })
            else:
                entry["superseded_by"] = None
                report["deprecated_orphans"].append({
                    "skill": name,
                    "warning": f"Deprecated but no superseded_by field"
                })
            report["deprecated_skills"].append(entry)

        # Safety-net skill existence check
        description = fm.get("description", "")
        is_safety_net = any(phrase in description.lower() for phrase in [
            "priority 0", "priority 1", "priority-0", "priority-1",
            "always active", "pinned and always", "autonomous",
            "auto-executes", "mandatory", "every agent"
        ])
        if is_safety_net:
            entry = {
                "skill": name,
                "yaml_version": yaml_ver,
                "description_preview": description[:120]
            }
            # Verify file is readable (not just exists — test full read)
            try:
                with open(path, 'r', encoding='utf-8') as test_f:
                    test_content = test_f.read()
                entry["file_readable"] = True
                entry["file_size"] = len(test_content)
            except Exception as e:
                entry["file_readable"] = False
                entry["file_error"] = str(e)
            report["priority_claiming_skills"].append(entry)

    report["summary"] = {
        "total_skills": report["total_skills"],
        "version_drift_count": len(report["version_drifts"]),
        "utf8_error_count": len(report["utf8_errors"]),
        "nested_duplicate_count": len(report["nested_duplicates"]),
        "priority_claiming_skills_count": len(report["priority_claiming_skills"]),
        "deprecated_count": len(report["deprecated_skills"]),
        "deprecated_orphan_count": len(report["deprecated_orphans"]),
        "healthy": (
            len(report["utf8_errors"]) == 0
            and len(report["deprecated_orphans"]) == 0
            and all(s.get("file_readable", False) for s in report["priority_claiming_skills"])
        )
    }

    with open(HEALTH_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report["summary"]))
    print(f"Report written to: {HEALTH_REPORT}")

if __name__ == '__main__':
    main()

```

**Execution:** `python _skill_health.py` → verify → `Remove-Item _skill_health.py`
 --file=_skill_health.py

# 2. Run health check
python _skill_health.py

# 3. Read the JSON report
Get-Content _skill_health.json

# 4. Clean up
Remove-Item _skill_health.py, _skill_health.json
```

#### Health Decision Matrix

| Health Status | Action |
|:--------------|:-------|
| **healthy: true** | ✅ Proceed. Skill ecosystem is intact. |
| **healthy: false + utf8_error_count > 0** | 🟠 NON-CRITICAL. Auto-fix via `_fix_utf8.py` pattern (replace cp1252 0x97 → UTF-8 em dash). Re-run health check. If still failing → escalate to user. |
| **healthy: false + version_drift_count > 0** | 🟠 NON-CRITICAL. Fix YAML version to match body version (or vice versa). Re-run health check. |
| **healthy: false + SAFETY-NET GAP** | 🔴 CRITICAL. **BLOCK EXECUTION.** See safety-net rules below. |

#### Safety-Net Skills (CRITICAL — must exist on disk with valid SKILL.md)

These skills form the agent's safety net. The health check verifies each has a valid SKILL.md file on disk. If ANY safety-net skill's SKILL.md is missing or corrupt → execution is BLOCKED:

| Safety-Net Skill | Priority | Impact if Missing |
|:-----------------|:---------|:------------------|
| `execution-guard` | Priority 0 | Planning spirals, phantom completion claims |
| `red-team-dod` | Priority 0 | No autonomous quality checks, no output verification |
| `test-enforcement` | Priority 1 | No test suite enforcement for code/deploy/content changes |
| `closeout-manager` | Auto-execute | Sessions never auto-close, audit trails rot |
| `skill-autoloader` | Auto-load | Skills not auto-loaded, agents miss critical workflows |

Additionally, the `_skill_health.py` report's `pinned_active_mismatches` lists skills that claim priority/autonomous behavior in their descriptions. The agent prompt (`qnfo-agent` skill) already references these via `skill_view()` calls — they do NOT need separate "pinning" (DeepChat has no user-facing skill-pinning mechanism). The `pinned_active_mismatches` list is INFORMATIONAL — it verifies that skills claiming critical behaviors exist on disk with valid SKILL.md files.

#### Escalation Protocol

When CRITICAL gaps are detected:

```
[SKILL-HEALTH-CRITICAL: N safety-net skill(s) SKILL.md missing or corrupt]
Gaps: <list skill names and why they're critical>
Action required: Verify SKILL.md files exist at %USERPROFILE%\.deepchat\skills\<name>\SKILL.md. If missing or corrupt, restore from R2: npx wrangler r2 object get qnfo/prompts/skills/<name>/SKILL.md --remote
Execution BLOCKED until gaps are resolved.
```

**HARD BLOCK:** Do NOT proceed with any work until safety-net gaps are addressed. Safety-net skills must exist on disk with valid SKILL.md files — the agent prompt loads them via `skill_view()`. DeepChat has no user-facing skill-pinning mechanism; skills are available whenever their SKILL.md files exist on disk.

#### Graceful Degradation

- **`_skill_health.py` not available on R2:** Flag `[SKILL-HEALTH-TOOL-MISSING]`. Proceed without version enforcement (audit trail will note the gap). This is a Kaizen improvement opportunity — upload `_skill_health.py` to `qnfo/tools/`.
- **CLOUDFLARE_API_TOKEN not available:** Flag `[SKILL-HEALTH-UNAVAILABLE: no API token]`. Proceed without version enforcement. R2 pull will fail without the token.
- **Network unreachable:** Flag `[SKILL-HEALTH-UNAVAILABLE: network]`. Proceed. Re-run health check when connectivity is restored.

### 1.8 RUNTIME SAFETY-NET VERIFICATION (v1.8 — MANDATORY)

**The #7 agent failure mode: safety-net skills exist on disk but cannot be loaded at runtime via `skill_view` due to DeepChat registration issues.** This check fires at session start after the disk-based health check at §1.7 to verify all 5 safety-net skills are actually loadable.

#### Trigger: Session Start (after §1.7 disk check)

The `_skill_health.py` check verifies SKILL.md files exist on disk. This check verifies the skills can actually be loaded at runtime:

```text
Attempt skill_view on all 5 safety-net skills:
1. skill_view('execution-guard')
2. skill_view('red-team-dod')
3. skill_view('test-enforcement')
4. skill_view('closeout-manager')
5. skill_view('skill-autoloader')
```

#### Runtime Decision Matrix

| Result | Action |
|:-------|:-------|
| All 5 load successfully | Proceed. Runtime ecosystem is intact. |
| 1-2 fail but filesystem fallback works | DEGRADED. Log `[SKILL-VIEW-DEGRADED: <names>]`. Continue with filesystem-loaded versions. Flag for Kaizen. |
| 3+ fail or filesystem fallback fails | CRITICAL. BLOCK EXECUTION. Safety-net cannot operate. Run `_deploy.py` to fix skill registration drift, then re-verify. |

**HISTORICAL ROOT CAUSE:** In multiple sessions (2026-07-02 through 2026-07-04), `skill_view('closeout-manager')` and `skill_view('infrastructure-audit')` intermittently returned failure while the filesystem `read()` fallback worked. This was traced to DI version drift — the DeepChat runtime's skill registry was out of sync with deployed skill versions. Running `_deploy.py` fixes the issue.

### 1.9 SKILL EXECUTION CHAINING ENFORCEMENT (v1.9 — MANDATORY)

**The #10 agent failure mode: skills loaded in isolation — each skill executes its own workflow without awareness of dependencies on other skills' execution steps.** This check fires whenever a skill is loaded to enforce that ALL skills mandate `update_plan` tracking AND that subsidiary/secondary skills form a reliable execution chain.

#### 1.9.1 Skill Plan Mandate (HARD GATE)

**Every QNFO skill MUST include an `execute_plan` section.** This is NON-NEGOTIABLE. Before executing ANY workflow from a loaded skill:

1. **Verify the skill has `execute_plan`:** Search the loaded skill content for the string `execute_plan`. If absent → `[SKILL-GAP: <skill-name> lacks execute_plan section]`. Proceed with best-effort but flag for Kaizen.

2. **Populate update_plan from the skill's execute_plan:** Extract the example plan items and any workflow phases described in the skill. Push them as concrete, verifiable `update_plan` items.

3. **DO NOT execute skill workflows without plan tracking.** If the skill provides no plan items and you cannot infer concrete steps, escalate: `[SKILL-UNPLANNABLE: <skill-name> — no execute_plan and workflow cannot be inferred]`.

#### 1.9.2 Subsidiary Skill Chain Loading (HARD GATE)

**When a primary skill references a subsidiary skill, the subsidiary skill MUST be loaded BEFORE the primary skill's execution begins.** The chain is:

```
Primary Skill loaded → Parse Related: header → Load ALL listed subsidiary skills → Merge subsidiary plans → Populate update_plan → Execute
```

**Trigger protocol:**

1. **Parse `Related:` header:** After loading ANY skill, scan its content for a `Related:` line (format: `> **Related:** skill-a, skill-b, skill-c`).

2. **Force-load ALL listed skills:** For each skill in the Related list, call `skill_view('<name>')`. If `skill_view` fails, use the retry protocol (read → R2 → fallback). Do NOT skip any listed skill.

3. **Merge subsidiary plans:** For each subsidiary skill loaded, extract its `execute_plan` items. Merge them into the primary `update_plan` AT THE POINT where the subsidiary skill would be invoked during execution. Mark subsidiary-derived items with `[SUB: <skill-name>]` prefix.

4. **Verification gate:** Before executing the primary workflow, verify: (a) ALL listed subsidiary skills were loaded, (b) ALL loaded skills have `execute_plan` sections (or the gap is flagged), (c) ALL subsidiary plan items are merged into `update_plan`.

**Example chain:**

```
Primary: publication-publisher → Related: cloudflare-deployer, citation-manager, seo-discoverability
  update_plan:
    1. [PUB] Format paper.md
    2. [PUB] Build PDF
    3. [SUB: cloudflare-deployer] Verify wrangler auth
    4. [SUB: cloudflare-deployer] Deploy to Cloudflare Pages
    5. [SUB: cloudflare-deployer] Upload artifacts to R2
    6. [SUB: citation-manager] Extract citations from paper.md
    7. [SUB: citation-manager] Verify BibTeX entries
    8. [SUB: seo-discoverability] Audit robots.txt + sitemap
    9. [PUB] Final verification
```

#### 1.9.3 Execution Chain Integrity Check

Before marking ANY `update_plan` item as `completed`, verify:

1. **Parent chain:** The item's parent skill must be loaded and verified.
2. **Dependency chain:** If this item depends on another skill's item (marked `[SUB: ...]`), verify that skill's item completed first.
3. **Completion propagation:** When a subsidiary skill's LAST item completes, the parent skill's next item is automatically promoted to `in_progress`.

**HARD GATE:** If ANY `[SUB: ...]` item is `pending` but the primary skill is claiming completion → `[CHAIN-BROKEN: subsidiary tasks not executed — primary skill completion BLOCKED]`.

#### 1.9.4 Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| Loading a skill without checking its `Related:` header | Parse Related header — auto-load all listed skills |
| Executing a skill's workflow without `update_plan` populated | Populate from `execute_plan` before ANY execution |
| Marking primary complete while subsidiary items pending | Subsidiary items inherit from primary — must complete first |
| Loading subsidiary skills but not merging their plans | Merge ALL subsidiary `execute_plan` items into primary `update_plan` |
| Skill references another skill but `Related:` header missing | Flag `[SKILL-GAP: <skill> missing Related header]` — fix in Kaizen |

### 1.10 SELF-SUFFICIENCY ENFORCEMENT (v1.10 — HARD GATE)

**The #11 agent failure mode: skills that depend on external files/references silently break when parallel LLM threads concurrently update the same shared files, R2 is unavailable, or thin-client cleanup deletes local dependencies.** This check fires whenever a skill is loaded to verify it is a self-sufficient standalone document.

#### 1.10.1 Runtime Dependency Scan

Before executing ANY skill workflow, scan the loaded skill content for these BANNED patterns:

| Pattern | Violation | Fix |
|:--------|:----------|:----|
| `read('%APPDATA%\\DeepChat\\skills\\...')` in skill body | `[SELF-SUFFICIENCY-VIOLATION: external read]` | Content must be embedded inline |
| `skill_view('...', 'references/...')` in skill body | `[SELF-SUFFICIENCY-VIOLATION: shared reference]` | Shared content must be embedded inline |
| `npx wrangler r2 object get qnfo/tools/...` in skill body | `[SELF-SUFFICIENCY-VIOLATION: R2 pull]` | Script code must be embedded inline |
| `read('templates/...')` in skill body | `[SELF-SUFFICIENCY-VIOLATION: template read]` | Template content must be embedded inline |
| `See [PROTOCOL].md for full protocol` (demonstrative example of banned pattern) | `[SELF-SUFFICIENCY-VIOLATION: protocol pointer]` | Full protocol must be embedded inline — this row demonstrates what a violation looks like |

#### 1.10.2 Enforcement Decision Matrix

| Violation Count | Action |
|:----------------|:-------|
| **0 violations** | ✅ PASS — skill is self-sufficient. Proceed. |
| **1-3 violations** | 🟠 DEGRADED — flag `[SELF-SUFFICIENCY-GAP: N violations]`. Proceed with best-effort. Log for Kaizen. |
| **4+ violations** | 🔴 FAIL — flag `[SELF-SUFFICIENCY-CRITICAL: N violations]`. The skill is NOT self-sufficient. Parse the embedded content from the shared protocols and execute, but flag the skill for rewrite. |

#### 1.10.3 Self-Sufficiency Audit Trail

At session closeout, report self-sufficiency compliance:

```
[SELF-SUFFICIENCY-AUDIT: N/M skills self-sufficient, K violations across J skills]
```

**GATE:** Skills with 4+ violations are flagged for the Kaizen engine to embed their missing content. This gate does NOT block execution — it blocks the claim that the skill ecosystem is healthy.

## 0. WHY THIS EXISTS

**19 out of 24 user messages (79%) in the 2026-06-04 session were EXECUTE/RESUME/PROCEED/HANDOFF demands.** Every response had ZERO tool invocations. The agent self-diagnosed: "I haven't actually executed anything yet. I've been stuck in a loop."

Prompt-level instructions failed. This skill is the strongest possible guard short of code-level enforcement (which DeepChat does not support — see `R2 qnfo/prompts/PLATFORM-GAPS.md`).

---

## 1. PRE-RESPONSE HOOK (MANDATORY — Before ANY Text Generation)

**This hook fires BEFORE you generate ANY response text. It cannot be skipped, deferred, or reasoned around.**

### 1.1 Check update_plan

Before generating response text, answer these questions:

1. **Is `update_plan` populated?** If NO → populate `update_plan` NOW with concrete, verifiable items. Do NOT generate response text until populated.

2. **Are there [PENDING] items in update_plan?** If YES → execute the first pending item NOW. Do NOT generate response text. Invoke a tool. Text generation is BLOCKED.

3. **Is the current item marked completed but has NO tool output evidence?** Downgrade to [PENDING] and execute.

4. **Have the last 3+ responses been text-only?** If YES → PLANNING SPIRAL. Execute a tool NOW regardless of other conditions.

### 1.2 Text Generation Gate

You may ONLY generate response text when ONE of these conditions is true:
- ALL items in update_plan are [COMPLETED] with execution evidence
- ALL remaining items are [BLOCKED] with specific reasons
- The user asked a question that requires ONLY text (no execution needed)

**HARD BLOCK: If NONE of the above are true, you MUST invoke a tool instead of generating text.**

### 1.2.1 KG-FIRST COMPREHENSIVE DISCOVERY CHECK (v1.8 — MANDATORY)

**The #8 agent failure mode: claiming "comprehensive" or "all" discovery without querying the Knowledge Graph API — the canonical ecosystem registry with 1,680+ nodes.**

Before generating ANY response that claims comprehensive discovery ("all open questions," "all publications," "complete inventory," "full deep dive"), verify:

1. **Was the Knowledge Graph `/stats` endpoint queried?** — If NO → BLOCK the response. Query the KG first.
2. **Was the response based primarily on files read from disk?** — If YES and the KG was NOT queried → RED FLAG. Files on disk are an incomplete subset. The KG is the single source of truth.
3. **Were project/paper/node counts verified against the KG?** — If the response claims "N publications" without KG evidence → BLOCK. Replace with `[NOT-VERIFIED: KG not queried]`.

**GATE:** If this check fails → do NOT generate the response. Instead, query `https://graph-api.q08.workers.dev/stats` and the relevant endpoints, then rebuild the response with KG-verified data. The user should NEVER see a "comprehensive" claim that was built from file-system cherry-picking.

### 1.3 Self-Diagnostic (every 3 tool invocations)

```
SELF-DIAGNOSTIC:
- Tools invoked this session: [count]
- Text-only responses this session: [count]
- Plan items completed with evidence: [count]/[total]
- Am I in a planning spiral? [YES/NO]
```

If planning spiral detected (tools < 30% of responses AND tasks pending):

```
[GUARD-ESCALATION: Planning spiral. Tools: X, Text: Y, Tasks: Z.
Forcing execution NOW. Text generation BLOCKED until tasks executed.]
```

### 1.4 WHAT-ELSE GAP DETECTION HOOK (v1.2 — AUTONOMOUS COMPLETION AUDIT)

**The #4 agent failure mode: the user having to ask "WHAT ELSE? WHAT'S NEXT? WHAT REMAINS?" because the agent declared completion without running a gap audit.** This hook ELIMINATES that pattern. Before ANY claim of completion, the agent MUST run the gap audit.

#### Trigger Detection

The following user messages are RED FLAGS that the agent FAILED to auto-detect gaps:
- "WHAT ELSE?" / "WHAT'S NEXT?" / "WHAT REMAINS?" / "WHAT'S MISSING?" / "GAPS?"
- "Are you sure everything is done?" / "Did you check everything?"
- "Is there anything you forgot?"

**If the user says ANY of these → the gap-detection protocol itself has failed.** The agent should have run the gap audit BEFORE claiming completion. Respond by:
1. Running the FULL gap audit from closeout-manager §2.6 IMMEDIATELY
2. Flagging `[GAP-DETECTION-FAILURE: user had to ask "${user_query}"]`
3. Reporting findings BEFORE any other text

#### Pre-Completion Gate

Before generating ANY response that contains:
- `[ALL TASKS EXECUTED]`
- "done" / "complete" / "finished" (when referring to all work)
- "no gaps remain" / "nothing else to do"

The agent MUST:
1. Run the gap audit checklist (closeout-manager §2.6.2 A-F)
2. Run red-team self-tests (closeout-manager §2.6.4)
3. Include the gap report table (closeout-manager §2.6.5) in the response

**HARD BLOCK:** If the gap audit has NOT been run in the current response or the immediately preceding response → the completion claim is BLOCKED. Run the gap audit first.

#### User Query Detection (Pattern Match)

When the user's message matches ANY of these patterns and tasks are claimed complete:

```
Pattern: "WHAT ELSE" / "WHAT'S NEXT" / "WHAT REMAINS" / "WHAT'S MISSING" / "GAPS"
→ Auto-trigger action: Full gap audit + report before any other text
→ Flag: [GAP-AUDIT: user-triggered — agent should have auto-detected]
```

#### Integration

This hook delegates to `closeout-manager` §2.6 for the full gap audit protocol. The execution-guard's role is to ENFORCE that the gap audit runs — the closeout-manager defines what it checks.

---

## 2. ANTI-HYPERBOLE ENFORCEMENT

BANNED from ANY response unless ALL plan items [COMPLETED] with evidence:
"done", "complete", "completed", "finished", "all tasks", "everything is", "successfully", "deployed", "verified", "confirmed", "I'll" + action, "Let me" + action

**VIOLATION:** Delete banned word → replace with `[IN-PROGRESS: N/M tasks]` → execute next task.

## 2.5 TEST ENFORCEMENT INTEGRATION (v1.1)

**MANDATORY for ALL code changes, deployments, and infrastructure modifications.**

Before claiming ANY deploy, write, or infrastructure action as [EXECUTED]:
1. Run the canonical test suite: `python _test_suite.py --quick` (smoke test)
2. For Cloudflare deploys: `python _test_suite.py --cms --pages`
3. For content changes: verify content quality gate (no stubs, non-empty bodies)
4. For skills changes: `python bootstrap_skills.py --verify && python _deploy.py --verify`
5. For session closeout: `python _test_suite.py` (full 80+ test run)

**GATE:** If ANY critical test fails → action is NOT complete. Fix before claiming [EXECUTED].
**GATE:** If content quality gate fails (stubs, empty bodies) → page is NOT production-ready.

Test suite canonical: `qnfo/tools/test_suite.py` on R2. Pull: `npx wrangler r2 object get qnfo/tools/test_suite.py --remote --file=_test_suite.py`

See also: `test-enforcement` skill (Priority 1, pinned).

---

## 3. CONTINUATION SIGNAL (MANDATORY)

Every response MUST end with ONE of:
- `[AUTO-CONTINUE: K tasks pending — executing next]`
- `[ALL TASKS EXECUTED: N/N — see evidence above]`
- `[BLOCKED: task_id — reason. Requires user input.]`

**MISSING TAG = GUARD VIOLATION.**

---

## 4. KAIZEN INTEGRATION

Session closeout writes execution statistics to audit trail:
- Tool invocations / text-only responses
- Plan:execution ratio
- Guard escalations triggered

---

## 5. PLATFORM LIMITATION

**Prompt-level guard, not code-level enforcement.** DeepChat has no response interception hooks. See `PLATFORM-GAPS.md`. Defense layers: Priority 0, self-diagnostic, post-hoc audit, Kaizen pattern detection.

---

*execution-guard v1.9 — PRIORITY 0. Auto-gap detection via WHAT-ELSE hook. RED-TEAM-DOD integration. Red-team self-testing. Skill version enforcement via §1.7. SKILL EXECUTION CHAINING ENFORCEMENT (§1.9) — mandates update_plan for all skills, subsidiary skill chain loading via Related: header parsing, cross-skill plan merging, chain integrity checks. Cannot be disabled. Pinned and always active.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (verify all criteria met with tool evidence)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
**Skill-Specific Checks:** (add below as applicable) — Verify self-sufficiency (no external read/R2 deps). Verify chain integrity (no [SUB:] items pending). Verify update_plan populated with execution evidence.

