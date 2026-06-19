---
name: closeout-manager
description: Session close-out procedures — autonomous trigger detection, task execution verification, project handoff initialization, audit trail export, R2 state upload, archive operations, draft artifact cleanup, and handoff documentation. Auto-executes at session end without user prompting.
version: "2.3"
---
# CLOSEOUT MANAGER SKILL — v2.3

> **AUTONOMOUS skill.** Do NOT wait for user to say "TERMINATE." Detect completion and auto-initiate closeout.
> Source: `CLOSEOUT-CHECKLIST` template + execution-guard skill

---

## Step 0: AUTONOMOUS TRIGGER DETECTION (MANDATORY — Run First)

Before ANY other closeout step, verify that closeout is warranted:

1. **Completion signal:** All planned tasks for this session are executed (files written, commits made, tests passed).
2. **No blocking items remain:** No unexecuted tasks, no unanswered user questions, no pending PRs awaiting review.
3. **User intent:** If the user has not explicitly said "continue" or asked a new question, AND all tasks are complete → auto-initiate closeout.
4. **ANTI-PATTERN:** Do NOT ask "shall I close out?" or "would you like me to terminate?" Just detect completion and close out.

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
   (Pull from R2 first: `npx wrangler r2 object get qnfo/tools/execution_audit.py --remote --file=_execution_audit.py`)

4. **Report in audit trail:**
   ```
   [EXECUTION-AUDIT: ratio=X/T, tools=Y, text-only=Z, severity=PASS|WARN|FAIL]
   ```

#### GATE
If ratio < 0.3 → closeout BLOCKED. The session did not execute enough. Fix before closing.

### 3. Project Handoff Initialization (MANDATORY — Projects Directory)

Verify and update handoff documents in `qnfo/projects/`:

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

### 4. Audit Trail Export to R2

Write session summary to temp file `YYYY-MM-DD-topic.md` containing:
- Agent name, session date, summary
- Decisions made (with rationale)
- Files changed, commits, issues referenced
- Infrastructure state changes
- Handoff notes for next session

Use `fill_prompt_template("CLOUDFLARE-AUDIT-EXPORT", {...})` for consistent format.

Upload to R2 (v4.95+ compatible):
```bash
npx wrangler r2 object put qnfo/audit/conversations/<file>.md --file=<path>
```

Verify upload:
```bash
npx wrangler r2 object get qnfo/audit/conversations/<file>.md
```

### 5. Update Discovery Index (MANDATORY — Every Session Close-Out)

Every session close-out MUST update the unified Discovery Index on Cloudflare R2:

```bash
# 1. Pull current index
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json

# 2. Add/update entries for:
#    - New projects created this session
#    - Publications generated this session  
#    - Projects archived this session
#    - State changes (active -> complete, etc.)

# 3. Upload updated index
npx wrangler r2 object put qnfo/discovery/index.json --file=_updated_index.json --remote
```

**If index is missing or corrupt:** Rebuild from R2 enumeration + local filesystem + GitHub repo listing. Upload fresh. Flag session as `[DISCOVERY-REBUILT]`.

**Verify:** `npx wrangler r2 object get qnfo/discovery/index.json --remote` must succeed.

### 6. Update Decision Log

If new decisions were made:
```bash
# Download current log
npx wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --file=<temp>

# Append new decisions to temp file

# Upload updated log
npx wrangler r2 object put qnfo/audit/decisions/DECISION-LOG.md --file=<temp>
```

### 7. Update Project State

```bash
# Upload state JSON
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-state-file>
```

### 8. Archive to Local Storage

```bash
Move-Item -Path "<project>" -Destination "qnfo/archive/projects\YYYY\MM\<name>\"
```

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
        Write-Output "WARNING: Only $count prompt templates in app-settings.json (expected 27). Run: python _deploy.py --prompts-only after restart."
        Write-Output "PROMPT-PERSISTENCE: Run 'npx wrangler r2 object get qnfo/tools/deploy.py --remote --file=_deploy.py; python _deploy.py --prompts-only; Remove-Item _deploy.py' after DeepChat restart."
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
- [ ] Step 5: Discovery Index updated (qnfo/discovery/index.json)
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

---

*closeout-manager skill v2.0 — AUTONOMOUS. Detects completion and auto-initiates. Never waits for "TERMINATE."*

---

*closeout-manager v2.3 — AUTONOMOUS. Detects completion and auto-initiates. Execution ratio audit gate at closeout.*
