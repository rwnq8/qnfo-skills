---
name: closeout-manager
description: Session close-out procedures — autonomous trigger detection, task execution verification, project handoff initialization, audit trail export, R2 state upload, lifecycle timestamp update, archive operations, draft artifact cleanup, and handoff documentation. Auto-executes at session end without user prompting.
version: "3.5"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification — negative verification. (2) Assumption Challenge — state and test every assumption. (3) Edge Case Check — empty/null/max/boundary/desync. (4) DoD Integration — verify all criteria met with tool evidence. (5) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** execution-guard, cloudflare-deployer, knowledge-graph



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('closeout-manager')` or `read()` with filesystem path.
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

# CLOSEOUT MANAGER SKILL — v1.0 — v3.5

> **D1-FIRST. R2 DEPRECATED FOR STRUCTURED DATA (§2.6).** Handoffs, audits, decisions, state files, and the discovery index now live EXCLUSIVELY in D1. R2 is for file artifacts ONLY (PDFs, scripts, templates). R2 flat files (index.json, handoff .md, state .json) are DEPRECATED — never read from R2, never write to R2 for structured records. See `qnfo-agent` §10 for D1 lifecycle integration.
> **LIFECYCLE-AWARE.** This release integrates with the automated lifecycle pipeline — `last_active` timestamps are reset on closeout to prevent premature staleness. Archive paths follow the ultrametric `qnfo/archive/projects/<name>/` convention.
> **AUTONOMOUS skill.** Do NOT wait for user to say "TERMINATE." Detect completion and auto-initiate closeout. Includes POST-PHASE GAP AUDIT — user should NEVER have to ask "WHAT ELSE?"
> Source: `CLOSEOUT-CHECKLIST` template + execution-guard skill + handoff-protocol skill

---

## Autonomous Continuation Protocol (v3.6)

**All 10 closeout steps execute autonomously without user intervention.** The agent MUST:

1. Auto-detect completion signal — no "TERMINATE" prompt needed
2. Run all 10 steps sequentially, advancing with `[AUTO-CONTINUE -> Step N+1]`
3. If a step fails: `[BLOCKED: reason]`, attempt fix (max 3), skip on non-retryable
4. Never ask "shall I close out?" — just detect and execute
5. At completion: present checklist summary with tool evidence for each step

**ANTI-PATTERN:** User should NEVER need to say "TERMINATE" or "CONTINUE."

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Step 0: Verify autonomous trigger (all tasks complete)", "status": "pending"},
  {"step": "Step 1: Verify all git commits", "status": "pending"},
  {"step": "Step 2: Task Execution Verification audit", "status": "pending"},
  {"step": "Step 2.6: POST-PHASE GAP AUDIT (all categories A-F)", "status": "pending"},
  {"step": "Step 3: Project Handoff Initialization", "status": "pending"},
  {"step": "Step 3.1: D1 Handoff Insertion (EXECUTE FIRST)\", \"status\": \"pending\"},
  {"step": "Step 4: Audit Trail Export to D1 + R2", "status": "pending"},
  {"step": "Step 5: Update D1 tables + lifecycle timestamps", "status": "pending"},
  {"step": "Step 9: Clean up temporary files (JIT enforcement)", "status": "pending"},
  {"step": "Step 10: Final CLOSEOUT-CHECKLIST verification", "status": "pending"},
])

---

## Step 0: AUTONOMOUS TRIGGER DETECTION (MANDATORY — Run First)

Before ANY other closeout step, verify that closeout is warranted:

1. **Completion signal:** All planned tasks for this session are executed (files written, commits made, tests passed).
2. **No blocking items remain:** No unexecuted tasks, no unanswered user questions, no pending PRs awaiting review.
3. **User intent:** If the user's last message contains the word "CONTINUE" (case-insensitive), "UPDATE PLAN AND CONTINUE", or asks a new question, auto-closeout is SUPPRESSED. The user is actively engaging and may have deferred tasks or want more work. Only auto-initiate closeout when the user has NOT said "continue" or asked a new question AND all tasks are complete.
4. **ANTI-PATTERN:** Do NOT initiate closeout when the user just said "CONTINUE" — even if all plan items are marked complete. The user may have follow-up tasks beyond the current plan. Only close out when there is a clear termination signal (e.g., "CLOSEOUT", "TERMINATE", silence after completion) OR the user's last message is not a CONTINUE directive and all tasks are genuinely done.
5. **ANTI-PATTERN:** Do NOT ask "shall I close out?" or "would you like me to terminate?" Just detect completion and close out.

**If all tasks are NOT complete:** Do NOT close out. Continue working. Only run closeout when work is genuinely complete.

---
## Session Close-Out Protocol (MANDATORY)

Execute these steps at the end of EVERY session:

### 1. Verify All Commits
```bash
git log -1 --oneline
git branch --show-current
```

### 2. Task Execution Verification (MANDATORY — Before Proceeding)

Verify that ALL planned tasks were actually EXECUTED:

a. **Audit planned vs executed:** Compare the session's task list (from Issue, backlog, or prior HANDOFF) against what was actually done.
b. **File existence check:** For every file claimed as written/edited → `Test-Path <file>` + `Get-Content <file> -First 3`
c. **Git commit check:** For every commit claimed → `git log --oneline` must show the commit hash
d. **Python execution check:** For every script claimed as run → re-execute and verify output matches claim
e. **Unfinished items:** Any planned-but-unexecuted item is a BLOCKER. Either execute it NOW or document it as `[DEFERRED: reason]` in the handoff.

**GATE:** If ANY planned task is unexecuted without documentation → closeout is BLOCKED. Fix before proceeding.

### 2.1 Execution Ratio Audit (v1.0 — MANDATORY at Every Closeout)

**The #1 undetected failure mode: sessions where the agent produced text but never invoked tools.** This audit catches planning spirals before they go unnoticed.

#### Procedure

1. **Estimate plan:execution ratio** from the session:
   - Count tool invocations (write, exec, edit, search, deploy, git commit)
   - Count total responses (including thinking blocks)
   - ratio = tools / (tools + text-only responses)

2. **Enforce ratio thresholds:**
   - ratio >= 0.5: PASS — proceed with closeout
   - ratio 0.3–0.5: WARN — closeout allowed but flag `[EXECUTION-RATIO-WARN]` in audit trail
   - ratio < 0.3: FAIL — closeout BLOCKED. Execute remaining tasks or escalate to user.

3. **Run `execution_audit.py`** if a conversation export is available:
   ```bash
   python _execution_audit.py --latest --json
   ```
   (Pull from R2 first: `
### Embedded Script: execution_audit.py (self-sufficient — no R2 pull needed)

Write the following code to `_execution_audit.py`, execute, then delete:

```python
#!/usr/bin/env python3
"""
execution_audit.py — Post-Hoc Execution Fidelity Analyzer (v1.0)

Analyzes exported DeepChat conversation files to compute plan:execution ratios.
Detects sessions where agents produced text instead of invoking tools.

Usage:
    python execution_audit.py <conversation_export.md>
    python execution_audit.py --dir <exports_directory>
    python execution_audit.py --latest  # Analyze most recent export

Output:
    - EXECUTION RATIO: tool invocations / total responses
    - PLANNING SPIRAL COUNT: sequences of 3+ text-only responses
    - BANNED WORD COUNT: "done"/"complete"/"finished" without evidence
    - CONTINUATION TAG COMPLIANCE: % of responses with [AUTO-CONTINUE]/[ALL TASKS EXECUTED]/[BLOCKED]
    - SEVERITY: PASS / WARN / FAIL

Signals for Kaizen engine:
    - ratio < 0.4: HIGH severity — planning spiral
    - ratio < 0.6: MEDIUM severity — borderline
    - banned words > 5 in session: LOW/MEDIUM severity
"""

import re
import os
import sys
import json
import argparse
from datetime import datetime

# ── Analysis Patterns ─────────────────────────────────────────────
TOOL_INVOCATION_PATTERN = re.compile(
    r'<invoke name="[^"]+">|## (execute|write|edit|exec|process|subagent|deploy|git\b)',
    re.IGNORECASE
)

USER_MESSAGE_PATTERN = re.compile(r'## \S+ (?:用户|User)\b')
ASSISTANT_MESSAGE_PATTERN = re.compile(r'## \S+ (?:助手|Assistant)\b|### \S+ (?:思考|Thinking)')

BANNED_WORDS = [
    r'\b(done)\b(?!.*\[EXECUTED\])',
    r'\b(complete[d]?)\b(?!.*\[EXECUTED\])', 
    r'\b(finished)\b(?!.*\[EXECUTED\])',
    r'\b(successfully)\b',
    r"I'll\s+\w+",
    r"Let me\s+\w+",
]

CONTINUATION_TAG_PATTERN = re.compile(
    r'\[AUTO-CONTINUE|\[ALL TASKS EXECUTED|\[BLOCKED:'
)

EXECUTE_DEMAND_PATTERN = re.compile(
    r'\b(EXECUTE|RESUME|PROCEED|HANDOFF|CONTINUE)\b',
    re.IGNORECASE
)


def analyze_conversation(filepath):
    """Analyze a single conversation export file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find user and assistant turns
    user_turns = []
    assistant_turns = []
    
    # Split by common export formats
    sections = re.split(r'(## 👤 用户|## 🤖 助手|## 👤 User|## 🤖 Assistant)', content)[1:]
    
    current_role = None
    for i in range(0, len(sections), 2):
        role_label = sections[i]
        text = sections[i+1] if i+1 < len(sections) else ''
        if '用户' in role_label or 'User' in role_label:
            user_turns.append(text)
        else:
            assistant_turns.append(text)
    
    total_responses = len(assistant_turns)
    total_user = len(user_turns)
    
    # Count tool invocations
    tool_invocations = 0
    tool_responses = 0
    for text in assistant_turns:
        tools = len(TOOL_INVOCATION_PATTERN.findall(text))
        tool_invocations += tools
        if tools > 0:
            tool_responses += 1
    
    # Count banned words
    banned_count = 0
    for text in assistant_turns:
        for pattern in BANNED_WORDS:
            banned_count += len(re.findall(pattern, text, re.IGNORECASE))
    
    # Count continuation tags
    tag_count = len(CONTINUATION_TAG_PATTERN.findall(content))
    
    # Detect planning spirals (3+ consecutive text-only responses)
    planning_spirals = 0
    consecutive_text_only = 0
    for text in assistant_turns:
        has_tools = bool(TOOL_INVOCATION_PATTERN.search(text))
        if not has_tools:
            consecutive_text_only += 1
            if consecutive_text_only == 3:
                planning_spirals += 1
        else:
            consecutive_text_only = 0
    
    # Count user EXECUTE demands
    execute_demands = 0
    for text in user_turns:
        execute_demands += len(EXECUTE_DEMAND_PATTERN.findall(text[:300]))
    
    # Calculate metrics
    tool_ratio = tool_responses / total_responses if total_responses > 0 else 0
    tag_compliance = tag_count / total_responses if total_responses > 0 else 0
    
    # Determine severity
    if tool_ratio < 0.3:
        severity = "CRITICAL"
    elif tool_ratio < 0.5:
        severity = "HIGH"
    elif tool_ratio < 0.7:
        severity = "MEDIUM"
    else:
        severity = "OK"
    
    return {
        "file": os.path.basename(filepath),
        "total_user_messages": total_user,
        "total_assistant_responses": total_responses,
        "tool_invocations": tool_invocations,
        "tool_responses": tool_responses,
        "text_only_responses": total_responses - tool_responses,
        "execution_ratio": round(tool_ratio, 3),
        "planning_spirals": planning_spirals,
        "banned_words": banned_count,
        "continuation_tag_compliance": round(tag_compliance, 3),
        "user_execute_demands": execute_demands,
        "severity": severity,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze DeepChat exports for execution fidelity")
    parser.add_argument("file", nargs="?", help="Conversation export .md file")
    parser.add_argument("--dir", help="Directory of export files")
    parser.add_argument("--latest", action="store_true", help="Analyze most recent export")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    files = []
    if args.file:
        files = [args.file]
    elif args.dir:
        files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) 
                 if f.endswith('.md') and 'export' in f.lower()]
    elif args.latest:
        downloads = os.path.expanduser(r"~\Downloads")
        candidates = [os.path.join(downloads, f) for f in os.listdir(downloads) 
                      if f.startswith('export_deepchat') and f.endswith('.md')]
        if candidates:
            files = [max(candidates, key=os.path.getmtime)]
    
    if not files:
        print("[ERROR] No export files found. Specify --file, --dir, or --latest")
        sys.exit(1)
    
    results = []
    for f in files:
        if os.path.exists(f):
            try:
                result = analyze_conversation(f)
                results.append(result)
            except Exception as e:
                print(f"[ERROR] Failed to analyze {f}: {e}")
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"\n{'='*60}")
            print(f"EXECUTION AUDIT: {r['file']}")
            print(f"{'='*60}")
            print(f"  User messages:         {r['total_user_messages']}")
            print(f"  Assistant responses:   {r['total_assistant_responses']}")
            print(f"  Tool invocations:      {r['tool_invocations']}")
            print(f"  Text-only responses:   {r['text_only_responses']}")
            print(f"  EXECUTION RATIO:       {r['execution_ratio']:.1%}  [{r['severity']}]")
            print(f"  Planning spirals:      {r['planning_spirals']}")
            print(f"  Banned words:          {r['banned_words']}")
            print(f"  User EXECUTE demands:  {r['user_execute_demands']}")
            print(f"  Tag compliance:        {r['continuation_tag_compliance']:.1%}")
            
            if r['severity'] in ('CRITICAL', 'HIGH'):
                print(f"\n  ⚠️  {r['severity']}: {r['text_only_responses']} text-only responses with {r['tool_invocations']} tool invocations.")
                print(f"  {r['user_execute_demands']} EXECUTE demands were met with {r['text_only_responses']}/{r['total_assistant_responses']} text-only responses.")
            
            print()

if __name__ == "__main__":
    main()

```

**Execution:** `python _execution_audit.py` → verify → `Remove-Item _execution_audit.py`
 --file=_execution_audit.py`)

4. **Report in audit trail:**
   ```
   [EXECUTION-AUDIT: ratio=X/T, tools=Y, text-only=Z, severity=PASS|WARN|FAIL]
   ```

#### GATE
If ratio < 0.3 → closeout BLOCKED. The session did not execute enough. Fix before closing.

### 2.6 POST-PHASE GAP AUDIT (v3.2 — RED-TEAM-DOD INTEGRATION)

**This section is the closeout instance of the RED-TEAM → DoD → ITERATE → REFINE cycle.** See `skill_view('red-team-dod')` for the canonical framework. The closeout-manager executes the cycle at session boundaries; the execution-guard (§1.5) enforces it per-task.

**The #2 undetected failure mode: the user having to ask "WHAT ELSE? WHAT'S NEXT? WHAT REMAINS?" because the agent didn't auto-detect gaps.** This protocol ELIMINATES that pattern. After EVERY major task/phase (not just closeout), the agent MUST run this audit autonomously — the user should NEVER have to ask.

#### 2.6.0 Core Principle

**The default is COMPREHENSIVE COMPLETION, not "task list done."** Finishing the last item on the task list does NOT mean the work is complete. The gap audit is the mechanism that transforms a task-completion claim into a work-completion claim.

#### 2.6.1 Trigger Rules

| Condition | Action |
|:----------|:--------|
| Any task marked [COMPLETED] in update_plan | Run gap audit BEFORE claiming "done" |
| User says "WHAT ELSE?" / "WHAT'S NEXT?" / "WHAT REMAINS?" / "GAPS?" | Run gap audit IMMEDIATELY — this is a RED FLAG that the agent failed to auto-detect |
| Last item in update_plan marked complete | Run FULL gap audit — this is the most dangerous moment for phantom completion |
| Session closeout triggered | Run gap audit as closeout Step 2.5 (before handoff) |
| Any system touched (R2, GitHub, DI, D1) | Run RECOVERY CHECK for that system |

**ANTI-PATTERN:** If the user EVER asks "what else?" and the agent responds without running a gap audit → the gap-detection protocol has FAILED. The user should NEVER need to ask.

#### 2.6.2 Gap Audit Categories (Run ALL — Mandatory)

Execute these checks programmatically. Do NOT rely on memory or assumptions:

**A. TASK REGISTER AUDIT**
```bash
# For EVERY item in update_plan:
# - [COMPLETED] → verify evidence still exists (file exists, commit in log, deploy accessible)
# - [PENDING] → is it genuinely unexecutable, or did we just skip it?
# - [FAILED] → has the failure reason been documented with specific error?
```

**B. CROSS-SYSTEM SYNC VERIFICATION (RED-TEAM: actively try to find desync)**
| Check | Command | Gate |
|:------|:--------|:-----|
| GitHub pushed? | `git log origin/master -1 --oneline` vs local latest | Must match |
| R2 synced? | Pick 3 random files, verify they exist on R2 | All 3 must succeed |
| DI updated? | D1 canonical — query `portfolio-state` and `qnfo-audit` tables | D1 is single source of truth; R2 index DEPRECATED |
| Bootstrap tools on R2? | Verify `qnfo/tools/bootstrap_skills.py` exists on R2 | Must exist |
| DNS resolution? | Test 13+ known active domains resolve HTTP 200 | All must resolve |
| DI-KG synced? | Compare Discovery Index project count against Knowledge Graph project count | Counts must match (within 5%) |
| HTTP redirects? | For every claimed redirect in HANDOFF, curl source URL and verify 301/302 + correct Location | All must redirect |

**C. RECOVERY & REPAIR PATH CHECK**
- Are all bootstrap/repair tools available on R2? (`qnfo/tools/`)
- Are canonical paths correct in scripts? (e.g., SKILLS_DIR pointing to right location)
- If a tool is missing from R2: upload it NOW — do not defer

**D. CONFIGURATION DRIFT DETECTION**
- Do any scripts reference wrong paths? (e.g., `.deepchat\skills` vs `DeepChat\skills`)
- Do any SKILL.md files reference outdated versions or paths in code examples?
- Are there orphaned files from prior sessions? (Run orphan scan)

**E. INFRASTRUCTURE HEALTH WARNINGS**
- `npx wrangler whoami` — token valid?
- Any repeated warnings? (rtk hook, encoding issues)
- Any background sessions still running? `process list`

**E2. PROVENANCE COMPLETENESS (v3.4 — MANDATORY for publication sessions)**
> **GATE (2026-07-05):** If this session involved publication, verify that Zenodo-ready provenance artifacts are complete. This gate prevents publications from being deposited without full project records and conversation history.

| Check | Command | Gate |
|:------|:--------|:-----|
| Conversation history exportable? | `get_conversation_history` tool available | Must succeed |
| Project files present? | `Get-ChildItem` count > 0 (beyond .git/) | Must have files |
| Git state captured? | `git log -1 --oneline` + `git status` accessible | Must succeed |
| README.md generated? | `Test-Path README.md` | Must exist for publication sessions |
| GitHub repo linked in Zenodo metadata? | Zenodo `related_identifiers` contains `isSupplementedBy` → GitHub URL | Must be present for publication sessions |
| Related Zenodo records cross-referenced? | Zenodo `related_identifiers` includes `isNewVersionOf` (prior versions) and `cites` (related papers) with valid DOIs | Must be present for publication sessions |
| Social URLs synced to KG? | `GET https://graph-api.q08.workers.dev/neighbors/paper-<slug>` shows `social_urls` with ≥1 URL (populated by `buffer-integration` Stage 3.5) | Check after social media posting |
| PROVENANCE-BUNDLE.zip for publication sessions? | If publication occurred this session → verify bundle was created and uploaded to R2 alongside paper artifacts | Must exist on R2 |

**RED-TEAM:** If publication occurred but no provenance bundle, README.md, Cloudflare mirror (D1 + KG), or KG location properties (social_urls, zenodo_url, github_url, pages_url) were created → `[BLOCKING: publication without provenance — violation of publication-publisher v3.1 Stage 3.5 + Stage 6.5 + Stage 6.6 gates]`. Fix before closeout: assemble provenance bundle + README, seed D1 + KG with ALL known locations, create new Zenodo version if necessary.

**F. TEST SUITE (if available)**
```bash
python _test_suite.py --quick  # Smoke test
```
If test suite fails → block [ALL TASKS COMPLETE] claim.

#### 2.6.3 Gap Severity Classification

| Severity | Definition | Action Required |
|:---------|:-----------|:----------------|
| **BLOCKING** | Prevents claiming work is complete | Fix NOW, do not proceed |
| **HIGH** | Functional gap — works but fragile | Fix this session if possible |
| **MEDIUM** | Nice-to-have — documentation, cleanup | Document for next session |
| **LOW** | Cosmetic — warnings, formatting | Note in audit trail |

**GATE:** If ANY BLOCKING gap exists → the agent MUST NOT claim [ALL TASKS EXECUTED]. Fix the gap or escalate.

#### 2.6.4 Red-Team Self-Testing (MANDATORY)

Before claiming any work complete, actively try to BREAK your own work:

1. **Negative verification:** "I claim X is on R2" → try to GET it and verify it's NOT there (expecting 404 means the claim is wrong)
2. **Path inversion:** "I fixed path from A to B" → search code for remaining references to A
3. **Empty return test:** "I synced all skills" → list R2 prefix and count, compare against local
4. **Commit hash verification:** "I pushed commit HASH" → `git log origin/master` must contain HASH
5. **Token exhaustion:** "Token is working" → run a PUT and verify it succeeds, not just `whoami`

**RED-TEAM RULE:** If you can't break your own claim, it's probably true. If you CAN break it, the gap audit caught a phantom claim before the user did.

#### 2.6.5 Gap Report Format (REQUIRED in every response that claims completion)

```
## GAP AUDIT
| Category | Check | Status | Detail |
|:---------|:------|:------:|:-------|
| Task Register | All items verified | PASS/FAIL | N/M items |
| GitHub | Commit pushed | PASS/FAIL | hash |
| R2 | Files synced | PASS/FAIL | N/M synced |
| DI | Updated | PASS/FAIL | timestamp |
| Recovery | Tools on R2 | PASS/FAIL | bootstrap_skills.py |
| Drift | Path check | PASS/FAIL | |
| Health | Warnings | PASS/FAIL | |
| Red-Team | Self-test | PASS/FAIL | |

**Gap Severity:** NONE / LOW / MEDIUM / HIGH / BLOCKING
```

#### 2.6.6 Integration with Other Skills

- **execution-guard**: The WHAT-ELSE hook (§1.4) fires this gap audit before allowing any [ALL TASKS EXECUTED] claim
- **handoff-protocol**: The gaps section pulls from this audit's output
- **kaizen-autonomous-update**: Phase 0 audit includes this gap audit as a checklist item
- **infrastructure-audit**: Phase 4 Health Recommendations feed into the infrastructure health check

---

### 3. Project Handoff Initialization (MANDATORY — Projects Directory)

Verify and update handoff documents in `qnfo/projects/` [ephemeral cache; R2 canonical: `qnfo/projects/`]:

a. **Scan all projects:**
```bash
Get-ChildItem -Path "qnfo/projects" -Directory | ForEach-Object {
    $handoff = Join-Path $_.FullName "HANDOFF.md"
    if (Test-Path $handoff) {
        $size = (Get-Item $handoff).Length
        Write-Output "$($_.Name): HANDOFF.md EXISTS ($size bytes)"
    } else {
        Write-Output "$($_.Name): NO HANDOFF.md — MUST CREATE"
    }
}
```

b. **For the CURRENT session's project:** Update `HANDOFF.md` with:
   - Session date, agent, summary of work completed
   - Current state (what's done, what's pending)
   - Next steps for the next agent
   - Blockers or dependencies
   - Branch and commit reference

c. **For any project MISSING HANDOFF.md:** Create one using `fill_prompt_template("HANDOFF", {...})` with at minimum: project name, current state, next steps.

d. **Verify:** Re-run the scan to confirm all projects have HANDOFF.md with non-zero size.

### 3.1 D1 Handoff Insertion (MANDATORY — EXECUTE FIRST v3.3)

**D1 IS THE CANONICAL HANDOFF STORE.** This step MUST run BEFORE any local HANDOFF.md is written. The D1 record is the single source of truth for all subsequent agents.

Write the session handoff to the `qnfo-audit` D1 database `audit_sessions` table as the canonical source:

```bash
npx wrangler d1 execute qnfo-audit --remote --command="
INSERT INTO audit_sessions (session_id, agent, start_time, end_time, tasks_completed, tasks_total, notes)
VALUES ('<session-id>', '<agent-name>', '<ISO-start>', '<ISO-end>', <N-done>, <N-total>, '<summary>. R2: qnfo/silent-radix/<handoff-filename>');
"
```

Also insert into `portfolio-state.handoffs` for lifecycle tracking:

```bash
npx wrangler d1 execute portfolio-state --remote --command="
INSERT INTO handoffs (id, from_agent, to_agent, r2_path, tasks_count, created_at, status, urn, session_id, summary)
VALUES ('H-<date>-<seq>', '<agent-name>', 'urn:qacp:agent:next-session', '<project-name>', <N>, '<ISO-8601>', 'active', 'urn:qnfo:handoff:H-<date>-<seq>', '<session-id>', '<summary>');
"
```

**Verify insertion:**
```bash
npx wrangler d1 execute qnfo-audit --remote --command="SELECT id, session_id, created_at FROM audit_sessions WHERE session_id='<session-id>';"
```

**GATE:** If handoff insertion fails or returns 0 rows ? closeout BLOCKED. Fix D1 connectivity before proceeding.

### 3.5 D1 Handoff Insertion (MANDATORY — D1-FIRST v3.0)

Write the session handoff to the `portfolio-state` D1 database as the canonical source:

```bash
# Generate a URN and insert handoff row
npx wrangler d1 execute portfolio-state --remote --command="
INSERT INTO handoffs (id, from_agent, to_agent, r2_path, tasks_count, created_at, status, urn, session_id, summary)
VALUES ('H-<date>-<seq>', '<agent-name>', 'urn:qacp:agent:next-session', '<project-name>', <N>, '<ISO-8601>', 'active', 'urn:qnfo:handoff:H-<date>-<seq>', '<session-id>', '<summary>');
"
```

**Verify insertion:**
```bash
npx wrangler d1 execute portfolio-state --remote --command="SELECT id, status, urn, created_at FROM handoffs WHERE id='H-<date>-<seq>';"
```

**GATE:** If handoff insertion fails or returns 0 rows → closeout BLOCKED. Fix D1 connectivity before proceeding.

#### 3.2 Local HANDOFF.md (OPTIONAL — Ephemeral Trace Only)

**This is NOT canonical.** The D1 record (§3.1) is the single source of truth. A local `HANDOFF.md` may be written as a human-readable convenience for the current session, but:

1. It MUST be deleted at session closeout (§9)
2. It MUST NOT be considered authoritative by any subsequent agent
3. It MUST NOT be git-tracked or persisted between sessions
4. Any agent encountering a local `HANDOFF.md` from a prior session MUST query D1 instead

**ANTI-PATTERN:** Writing a local `HANDOFF.md` and treating it as the canonical handoff without inserting into D1 first. This is a *fabrication-level offense (Rule 14)* — the file will be deleted at closeout and the handoff data will be LOST.

#### 3.3 Knowledge Graph Handoff Node (RECOMMENDED)

Seed the Knowledge Graph with Handoff and Session nodes for cross-system traceability:

```python
# Seed via graph-api POST /sync
# Handoff node: id=handoff-<id>, label=Handoff
# Session node: id=session-<id>, label=Session
# Edge: Session -[PRODUCED]-> Handoff -[BELONGS_TO]-> Project
```

### 4. Audit Trail Export to D1 + R2 Backup

Write session summary to temp file `YYYY-MM-DD-topic.md` containing:
- Agent name, session date, summary
- Decisions made (with rationale)
- Files changed, commits, issues referenced
- Infrastructure state changes
- Handoff notes for next session

Use `fill_prompt_template("CLOUDFLARE-AUDIT-EXPORT", {...})` for consistent format.

**4.1 Conversation History Preservation (v3.4 — MANDATORY for publication sessions)**

If this session involved research or publication activity, export the full conversation history for provenance:

```bash
# The agent MUST call get_conversation_history for the current session
# Write the output to a timestamped file
# Upload alongside the audit trail to R2

# Export conversation (pseudo-code — agent uses actual get_conversation_history tool):
# history = get_conversation_history(conversationId="<current>", includeSystem=False)

# Write to local file
python _export_session.py --output qnfo/audit/conversations/<YYYY-MM-DD>-session-<slug>.md

# Upload to R2
npx wrangler r2 object put qnfo/audit/conversations/<YYYY-MM-DD>-session-<slug>.md --file=<path>
```

**GATE for publication sessions:** If conversation history cannot be exported → `[BLOCKING: provenance incomplete — conversation history unavailable]`. The session's publications cannot claim full reproducibility. Either: (a) fix conversation export and re-upload, or (b) document the gap explicitly in the publication's PROVENANCE.md as a known limitation.

Upload to R2 (v4.95+ compatible):
```bash
npx wrangler r2 object put qnfo/audit/conversations/<file>.md --file=<path>
```

Verify upload:
```bash
# D1-FIRST: Verify audit in D1 instead of R2: npx wrangler d1 execute qnfo-audit --remote --command "SELECT * FROM chat_sessions ORDER BY created_at DESC LIMIT 1" -y
```

### 5. Update Discovery Index (MANDATORY — Every Session Close-Out)

Every session close-out MUST update the unified Discovery Index on Cloudflare R2:

```bash
# 1. Pull current index
# D1-FIRST: Query D1 directly for discovery instead of pulling R2 index
# Projects: npx wrangler d1 execute qnfo-audit --remote --command "SELECT * FROM discovery_projects" -y
# Resources: npx wrangler d1 execute portfolio-state --remote --command "SELECT * FROM resources" -y
# Handoffs: npx wrangler d1 execute portfolio-state --remote --command "SELECT * FROM handoffs ORDER BY created_at DESC" -y
# Decisions: npx wrangler d1 execute portfolio-state --remote --command "SELECT * FROM decisions ORDER BY logged_at DESC" -y
# R2 qnfo/discovery/index.json is DEPRECATED — D1 is canonical for all structured records.

# 2. Add/update entries for:
#    - New projects created this session
#    - Publications generated this session  
#    - Projects archived this session
#    - State changes (active -> complete, etc.)
#    - last_active timestamps set to now (ISO 8601) ← LIFECYCLE CRITICAL

# 3. Upload updated index
# D1-FIRST: Update D1 tables directly instead of pushing R2 index
# npx wrangler d1 execute portfolio-state --remote --command "UPDATE resources SET ..." -y
# R2 discovery index is DEPRECATED — D1 is canonical.
```

**If index is missing or corrupt:** Rebuild from R2 enumeration + local filesystem + GitHub repo listing. Upload fresh. Flag session as `[DISCOVERY-REBUILT]`.

**Verify:** D1 queries must return current data. R2 discovery index is DEPRECATED — do not verify against it.

### 5.1 Lifecycle Timestamp Update (v2.4 — LIFE-AND-DEATH HARD GATE)

**CRITICAL:** The automated lifecycle pipeline scans `last_active` timestamps daily at 06:00 UTC. If a project's `last_active` is not updated on closeout, it will be marked STALE after 90 days and AUTO-ARCHIVED after 180 days — potentially nuking the project's R2 files without human intervention.

**MANDATORY:** On EVERY session closeout, whether or not the DI is modified:

1. **Set `last_active` to `now` in ISO 8601** for the CURRENT session's project:
```python
from datetime import datetime, timezone
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
di["projects"]["<project-name>"]["last_active"] = now
```

2. **Set `last_active` for any project modified this session** (even indirectly via dependency):
```python
for project in projects_modified_this_session:
    di["projects"][project]["last_active"] = now
```

3. **Upload updated DI** with new timestamps:
```bash
npx wrangler r2 object put qnfo/discovery/index.json --file=<updated> --remote
```

**LIFECYCLE TIMELINE:**
| Days Inactive | Status | Action |
|:-------------:|--------|--------|
| 0–90 | ACTIVE | Normal operation |
| 90–180 | STALE | Flagged by Lifecycle Worker. Project still intact. |
| 180+ | ARCHIVED | R2 files auto-migrated to `qnfo/archive/projects/<name>/`. Worker queued. |

**GATE:** If `last_active` is NOT updated → the lifecycle pipeline will auto-archive the project. This is the #1 cause of "my project disappeared."

### 6. Update Decision Log

If new decisions were made:
```bash
# Download current log
# D1-FIRST: Query decisions from D1 instead of R2: npx wrangler d1 execute portfolio-state --remote --command "SELECT * FROM decisions ORDER BY logged_at DESC" -y

# Append new decisions to temp file

# Upload updated log
npx wrangler r2 object put qnfo/audit/decisions/DECISION-LOG.md --file=<temp>
```

### 7. Update Project State

```bash
# Upload state JSON
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-state-file>
```

### 8. Archive to Local Storage (Ultrametric Path Convention)

```bash
# Move completed project to local archive
Move-Item -Path "<project>" -Destination "qnfo/archive/projects\YYYY\MM\<name>\"
```

**R2 archive path convention** (for projects marked ARCHIVED):
- Old: `qnfo/projects/<name>/`
- New: `qnfo/archive/projects/<name>/`
- Future (ultrametric): `qnfo/archived/<domain>/<program>/<name>/`

### 9. Clean Up Temporary Files — AGGRESSIVE JIT ENFORCEMENT

**HARD RULE:** This machine is a thin client. The ONLY files that persist locally are the DeepChat runtime (`qnfo/prompts/`). Everything else MUST be cleaned up at session closeout. Never use `-ErrorAction SilentlyContinue` — verify every deletion with `Test-Path`.

**Step 9.1: Orphan `_*` file scan and removal**
```bash
Get-ChildItem -File -Name | Where-Object { $_ -match '^_' } | ForEach-Object { Remove-Item $_; Write-Output "CLEANED: $_" }
# VERIFY: No _* files remain
$orphans = Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }
if ($orphans) { Write-Output "FAILED: Orphans remain: $orphans"; exit 1 }
Write-Output "Orphan scan: CLEAN"
```

**Step 9.2: Python cache cleanup**
```bash
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__"; Write-Output "CLEANED: __pycache__" }
```

**Step 9.3: Publication draft artifact cleanup (v2.2 — MANDATORY for publication sessions)**

If this session involved ANY publication activity (PDF generation, Zenodo upload, Cloudflare deploy), execute the following:

```bash
# Remove draft markdowns
Get-ChildItem -Recurse -Filter "*.draft.md" | Remove-Item -Force
# Remove generic-named PDFs (non-versioned)
@('paper.pdf', 'final.pdf', 'output.pdf') | ForEach-Object {
    if (Test-Path $_) { Remove-Item $_ -Force; Write-Output "CLEANED: $_" }
}
# Remove LaTeX build artifacts
Get-ChildItem -Recurse -Include @('*.aux', '*.log', '*.out', '*.toc', '*.bbl', '*.blg') | Remove-Item -Force
# Remove artifact manifests (should be on R2)
if (Test-Path "ARTIFACT-MANIFEST.json") {
    Write-Output "WARNING: ARTIFACT-MANIFEST.json still present — should be on R2"
    Remove-Item "ARTIFACT-MANIFEST.json" -Force
}
# Verify no build artifacts remain
$draft_remaining = Get-ChildItem -Recurse -Include @('*.draft.md', 'paper.pdf', 'final.pdf', 'output.pdf', '*.aux', '*.log') -ErrorAction SilentlyContinue
if ($draft_remaining) {
    Write-Output "FAILED: Draft artifacts remain: $($draft_remaining -join ', ')"
    exit 1
}
Write-Output "Draft artifact cleanup: CLEAN"
```

**GATE:** If ANY draft artifacts remain OR R2 does not contain canonical copies → `[BLOCKED: cleanup incomplete]`. Session closeout cannot proceed. Upload to R2 first, then re-run cleanup.

**Step 9.4: Project file cleanup (outside import-surface)**
- If any project files were pulled from R2 during the session (e.g., in `qnfo/projects/`, `qnfo/`):
  - If modified: re-upload to R2 FIRST, then delete local copy
  - If unmodified: delete local copy immediately (they're stale caches)
- The goal: ZERO project files persist locally between sessions

**Step 9.5: Final verification**
```bash
# Verify DeepChat prompts are persisted (v2.3)
$appSettings = "$env:APPDATA\DeepChat\app-settings.json"
if (Test-Path $appSettings) {
    $json = Get-Content $appSettings -Raw | ConvertFrom-Json
    $count = $json.promptTemplates.Count
    if ($count -lt 27) {
        Write-Output "WARNING: Only $count prompt templates in app-settings.json (expected 27)."
    } else {
        Write-Output "PROMPTS OK: $count templates in app-settings.json"
    }
} else {
    Write-Output "WARNING: app-settings.json not found. Prompts may be lost on restart."
}

# Verify ephemeral files
$remaining = Get-ChildItem -Recurse -File -Name | Where-Object { 
    $_ -match '^_' -and $_ -notmatch '^skills\\' -and $_ -notmatch '^templates\\' -and $_ -notmatch '^agents\\' -and $_ -notmatch '^config\\' -and $_ -notmatch '^audit\\'
}
if ($remaining) { Write-Output "WARNING: Non-import-surface files detected: $remaining" }
```
Only `qnfo/prompts/` files should remain. Everything else is clutter.

### 10. Final Verification — Full Closeout Checklist

Run `fill_prompt_template("CLOSEOUT-CHECKLIST", {"topic": "<session-topic>"})` and verify ALL phases pass. Deliver the completed checklist as part of the closeout summary.

---

## Close-Out Checklist (Summary)

Use `fill_prompt_template("CLOSEOUT-CHECKLIST")` for the full verification checklist:
- [ ] Step 0: Autonomous trigger detection passed (all tasks complete)
- [ ] Step 1: All commits verified
- [ ] Step 2: ALL planned tasks executed (Task Execution Verification)
- [ ] Step 3: ALL projects have HANDOFF.md updated (Project Handoff Init)
- [ ] Step 4: Audit trail exported to R2
- [ ] Step 5: D1 tables updated (portfolio-state.resources, qnfo-audit.discovery_projects) **including last_active timestamps**. R2 discovery index is DEPRECATED.
- [ ] Step 5.1: **Lifecycle timestamps reset** — `last_active` set to now for all projects touched this session
- [ ] Step 6: Decision log updated
- [ ] Step 7: Project state updated
- [ ] Step 8: Archive completed
- [ ] Step 9: Temp files cleaned + Prompt integrity verified (27 templates in app-settings.json)
- [ ] Step 10: Full CLOSEOUT-CHECKLIST passed (all phases)

---

## Handoff Document

When handing off to another agent:
```bash
fill_prompt_template("HANDOFF", {type: "Program->Project", scope: "...", ...})
```

---

## Lifecycle Pipeline Awareness (v2.4)

The automated lifecycle pipeline runs daily at 06:00 UTC (`qnfo-lifecycle` Worker) scanning `last_active` timestamps in the Discovery Index. The closeout procedure is the ONLY mechanism that resets these timestamps. Without it, projects auto-archive.

| Worker | Purpose | Cron |
|--------|---------|------|
| `qnfo-lifecycle` | Scans `last_active`, transitions ACTIVE→STALE→ARCHIVED | Daily 06:00 UTC |
| `qnfo-archive-worker` | Consumes `qnfo-lifecycle-queue`, migrates R2 files | On queue trigger |

## Reference Files

- Close-out checklist: `templates/CLOSEOUT-CHECKLIST.md` (v5.0+)
- Audit export template: `templates/CLOUDFLARE-AUDIT-EXPORT.md`
- Handoff template: `templates/HANDOFF.md`
- Rebuild from scratch: `REBUILD-FROM-SCRATCH.md`

---

## Anti-Patterns (DO NOT DO)

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| Waiting for user to say "TERMINATE" | User expects autonomous closeout | Detect completion → auto-initiate |
| Closing out with unexecuted tasks | Leaves work incomplete | Verify all tasks executed first |
| Skipping project handoff scan | Next agent has stale/absent HANDOFF.md | Scan ALL projects, create/update HANDOFF.md |
| Claiming tasks done without verification | Phantom claims (Rule 14 violation) | Test-Path + Get-Content + git log audit |
| Asking "shall I close out?" | Unnecessary user intervention | Just close out and present summary |
| **Skipping `last_active` update** | Project auto-archives after 180 days | **Reset timestamp EVERY closeout** |
| **Writing handoffs ONLY to R2** | D1 handoffs table sits empty (0 rows) — next agent starts cold | **INSERT into portfolio-state.handoffs D1 table as canonical** |
| **Trusting R2 over D1 for itemized data** | R2 flat files have no schema, no FTS, no verification | **D1 is canonical for tasks, handoffs, decisions, projects** |
| **Writing handoffs to local `.md` files instead of D1** | File deleted at closeout (§9), handoff data LOST, next agent starts cold | **INSERT into D1 `audit_sessions` or `portfolio-state.handoffs` FIRST; local .md is optional ephemeral trace** |
| **Persisting canonical files on local disk** | Violates thin-client mandate — files at risk of drive loss, sync drift, session clutter | **R2 is canonical for ALL artifacts. Local copies are ephemeral caches deleted at closeout (§9). .git/ is the only exception.** |
| **Writing to local disk without R2 upload** | Data exists only on fragile local filesystem — single drive failure = total loss | **Upload to R2 BEFORE considering any write complete. The R2 copy is the canonical output.** |

---

*closeout-manager skill v3.5 — D1-FIRST. RED-TEAM-DOD INTEGRATION (§2.6). POST-PHASE GAP AUDIT with red-team self-testing + DNS resolution sweep + DI-KG sync verification + provenance/README completeness check. LIFECYCLE-AWARE. R2 archive paths follow ultrametric convention.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
**Skill-Specific Checks:** Verify all handoffs written to D1. Verify lifecycle timestamps reset. Verify thin-client cleanup complete. Verify closeout checklist passed all phases.

> **Version:** (Kaizen-audited 2026-07-08)
