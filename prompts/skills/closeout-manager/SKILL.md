---
name: closeout-manager
version: "3.0"
description: Session close-out procedures — autonomous trigger detection, task execution verification, project handoff initialization, audit trail export, R2 state upload, archive operations, draft artifact cleanup, and handoff documentation. Auto-executes at session end without user prompting.
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before closing any session, autonomously run: (1) Task Execution Verification — all update_plan items marked complete with tool evidence. (2) WBS Completion Gate — verify no project phases remain. (3) Execution Ratio Audit. (4) 

---

> **Related:** execution-guard, red-team-dod, kaizen-autonomous-update, github-cloudflare-sync, skill-sync, knowledge-graph, infrastructure-audit

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('closeout-manager')` or `read()` with filesystem path, 
and auto-triggered on user keywords `CLOSEOUT`/`closeout`/`finalize`.
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

## Task Register Audit (MANDATORY before closeout)

Before finalizing closeout, audit the session task register:

1. **Count total tasks:** Sum all tasks across all update_plan snapshots
2. **Count completed:** Tasks marked [completed] with tool evidence
3. **Count skipped/blocked:** Tasks marked [BLOCKED] or [DEFERRED] with documented reasons
4. **Execution ratio:** completed / total (target: >= 0.90)
5. **Gap analysis:** Any task claimed complete without tool evidence MUST be re-verified

**Execution Ratio Thresholds:**

| Ratio | Action |
|:------|:-------|
| >= 0.95 | PROCEED. Excellent execution discipline. |
| 0.90 - 0.94 | PROCEED with note. Acceptable but review skipped tasks. |
| 0.75 - 0.89 | WARN. Significant gap. Document all skipped tasks with reasons. |
| < 0.75 | BLOCKED. Too many unexecuted tasks. Re-open session. |

## Escalation Path

If the closeout protocol encounters any BLOCKING condition:

1. **Document the blocker** — what condition failed, what evidence exists
2. **Auto-retry** — attempt the failing step once more with corrected approach
3. **Escalate to user** — present the blocker with:
   - The specific condition that failed
   - Evidence collected
   - Attempted remediation
   - Recommended next action
4. **Never silently bypass** a closeout gate

## Session Handoff

If the session is closing out with pending or deferred work:

1. **Generate continuation prompt** — compact summary of:
   - What was accomplished (with evidence)
   - What remains pending (with priority)
   - Current state snapshot (R2 paths, git branch, D1 state)
   - First executable action for next session
2. **Write to handoff artifact** — `_handoff_YYYYMMDDHHMM.md` in working directory
3. **Archive to D1** — `INSERT INTO handoffs (session_id, project_id, phase_completed, summary, pending_work, next_action, r2_handoff_path) VALUES (?, ?, ?, ?, ?, ?, ?)` via D1 REST API

## D1 Reference Protocol (v3.7 ARCHITECTURAL DECISION: Dynamic records → D1, Static files → R2)

**R2 is for static files only** (SKILL.md, PDFs, papers, images, tools). Dynamic/accumulating/live records MUST use D1 for queryability, indexing, and cross-referencing.

### Dynamic Records → D1 (`qnfo-audit` database)

| Artifact | D1 Table | Insert Pattern |
|:---------|:---------|:---------------|
| Skills index | `skills_index` | `INSERT OR REPLACE INTO skills_index (name, version, ...) VALUES (?, ?, ...)` |
| Audit trail | `audit_trail` | `INSERT INTO audit_trail (session_id, project_id, phase, task_id, action, evidence) VALUES (?, ?, ?, ?, ?, ?)` |
| Project ledger | `project_ledger` | `INSERT INTO project_ledger (project_id, session_id, phase, task_id, action, evidence) VALUES (?, ?, ?, ?, ?, ?)` |
| Handoff docs | `handoffs` | `INSERT INTO handoffs (session_id, project_id, phase_completed, summary, pending_work) VALUES (?, ?, ?, ?, ?)` |
| Decisions | `decisions` | `INSERT INTO decisions (project_id, skill_name, category, decision, rationale) VALUES (?, ?, ?, ?, ?)` |
| WBS state | `wbs_state` | `INSERT OR REPLACE INTO wbs_state (project_id, current_phase, total_phases, phase_data) VALUES (?, ?, ?, ?)` |

**D1 API endpoint:** `POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{DB_ID}/query`

**Verification:** `SELECT COUNT(*) FROM <table> WHERE session_id = ?` — returns row count, instant.

### Static Files → R2 (`qnfo` bucket)

**R2 remains correct for:** SKILL.md snapshots, published papers, bootstrap tools, SEO metadata, publication artifacts. These are immutable or rarely-updated static files.

| Artifact | R2 Path | When |
|:---------|:--------|:-----|
| Skills backup | `qnfo/prompts/skills/<name>/SKILL.md` | After any skill modification |
| Publication PDF | `qnfo/papers/<doi>.pdf` | After publication |
| Bootstrap tools | `qnfo/tools/<script>.py` | After tool updates |

### Architecture Rule

**If a record is updated more than once or needs to be queried across sessions → D1. If it's a versioned static file → R2.**


Gap Detection. (5) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask for quality.


# CLOSEOUT MANAGER SKILL — v3.0

> **AUTONOMOUS skill.** Do NOT wait for user to say "TERMINATE." Detect completion and auto-initiate closeout.
> Source: `CLOSEOUT-CHECKLIST.md` + DEFAULT.md §10 + QWAV-DEFAULT.md close-out checklist

---

## Step 0: AUTONOMOUS TRIGGER DETECTION (MANDATORY — Run First)

Before ANY other closeout step, verify that closeout is warranted:

1. **Completion signal:** All planned tasks for this session are executed (files written, commits made, tests passed).
2. **No blocking items remain:** No unexecuted tasks, no unanswered user questions, no pending PRs awaiting review.
3. **User intent:** If the user has not explicitly said "continue" or asked a new question, AND all tasks are complete → auto-initiate closeout.
4. **ANTI-PATTERN:** Do NOT ask "shall I close out?" or "would you like me to terminate?" Just detect completion and close out.

**If all tasks are NOT complete:** Do NOT close out. Continue working. Only run closeout when work is genuinely complete.

---



## Tools Required

This skill is designed for use with QNFO agent tools. When loaded by a DEFAULT.md agent, the full tool suite (read, write, edit, exec, process, brave_web_search, YoBrowser, subagent_orchestrator) is available.

## QNFO Custom Skill Note

This is a QNFO custom skill deployed via `_deploy.py` (R2: `qnfo/tools/deploy.py`). It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:

```
read('%APPDATA%\DeepChat\skills\closeout-manager\SKILL.md')
```



## 2.5.1 Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Tools are pulled to local disk on demand for execution only — this is an ephemeral cache, not permanent storage. Delete and re-pull from R2 any time.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:----------------------|:--------|
| `deploy.py` | `qnfo/tools/deploy.py` | `_deploy.py` (R2: `qnfo/tools/deploy.py`) (cache) | Deploys skill files to DeepChat runtime |
| `system_audit.py` | `qnfo/tools/system_audit.py` | `_system_audit.py` (R2: `qnfo/tools/system_audit.py`) (cache) | Cross-file consistency and version drift audit |

### Execution Protocol (Ephemeral)
Tools execute locally (Python requires filesystem access) but do NOT persist:
1. **Copy embedded script:** `Copy-Item scripts/<name>.py _<name>.py` (scripts are self-contained in skill directory)
2. **Execute:** `python _<name>.py`
3. **Discard:** `Remove-Item _<name>.py`
4. If script not embedded in skill directory: flag `[SKILL-GAP: script <name>.py not embedded in skill directory]`




---

### Step 0.1: WBS COMPLETION GATE (v3.6 -- MANDATORY, RUN BEFORE STEP 0)

**The #2 closeout anti-pattern: triggering closeout because update_plan is empty, when the PROJECT has more phases remaining.** An empty plan window does NOT mean the project is done -- it means the current phase completed. Step 0.1 prevents premature closeout by checking the project-level WBS.

#### 0.1.1 Query D1 WBS State

Before proceeding to Step 0, query the D1 `wbs_state` table: `SELECT * FROM wbs_state WHERE project_id = ?` (see D1 Reference Protocol for API details). If no row returns, the session uses flat planning (no phases). Proceed to Step 0 normally. If a row EXISTS, read it and apply the gate.

#### 0.1.2 Phase Completion Verification

Extract from D1 `wbs_state` row: current_phase, total_phases, and phase_data (JSON with statuses).

**GATE LOGIC:**

| Condition | Action |
|:----------|:-------|
| current_phase < total_phases AND next-phase tasks not completed | **CLOSEOUT BLOCKED.** Project has more phases. Auto-expand Phase N+1. Execute. |
| current_phase < total_phases BUT current_phase tasks incomplete | **CLOSEOUT BLOCKED.** Fix and execute before closeout. |
| current_phase == total_phases AND all phase tasks completed | **PROCEED.** All project phases complete. Continue to Step 0 closeout. |
| D1 query failed or no project_id record exists | **FALLBACK.** Treat as non-phased session. Proceed normally. |

#### 0.1.3 CLOSEOUT-AS-ESCAPE Detection (v3.6)

If closeout is initiated when D1 `wbs_state` shows current_phase < total_phases:
- This is a **CLOSEOUT-AS-ESCAPE** violation -- equivalent to Rule 14 phantom claim.
- The agent is attempting to close out the session as a way to avoid executing the next phase.
- **BLOCK the closeout. Auto-expand Phase N+1. Execute immediately.**

#### 0.1.4 Cross-Skill Integration

This gate integrates with execution-guard Section 1.5 (Phase-Aware Auto-Expansion Protocol — now reading from D1 `wbs_state` instead of local `_wbs_state.json`) and red-team-dod Section 9 (Phase-Aware Iteration).
**HARD RULE:** Closeout is ONLY warranted when ALL project phases are complete OR every remaining phase is truly blocked with documented reasons. 'The current plan window is empty' is NEVER sufficient grounds for closeout.


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
   (Script is self-contained in skill directory: `Copy-Item scripts/execution_audit.py _execution_audit.py`)

4. **Report in audit trail:**
   ```
   [EXECUTION-AUDIT: ratio=X/T, tools=Y, text-only=Z, severity=PASS|WARN|FAIL]
   ```

#### GATE
If ratio < 0.3 → closeout BLOCKED. The session did not execute enough. Fix before closing.

### 3. Project Handoff Initialization (MANDATORY — Projects Directory)

Verify and update handoff documents in the workspace projects:

a. **Scan all projects:**
```bash
Get-ChildItem -Path ".\projects" -Directory | ForEach-Object {
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

c. **For any project MISSING HANDOFF.md:** Create one directly with at minimum: project name, current state, next steps. (HANDOFF template deprecated v2026-07-11 — create inline.)

d. **Verify:** Re-run the scan to confirm all projects have HANDOFF.md with non-zero size.

### 4. Audit Trail Export to R2

Write session summary to temp file `YYYY-MM-DD-topic.md` containing:
- Agent name, session date, summary
- Decisions made (with rationale)
- Files changed, commits, issues referenced
- Infrastructure state changes
- Handoff notes for next session

Use the following consistent format (CLOUDFLARE-AUDIT-EXPORT template deprecated v2026-07-11):

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

### 6. Auto-Sync Skills — Skill Sync Verification (MANDATORY — v3.0)

**GATE:** Before closeout, verify all local skills synced to GitHub + R2 + D1 skills_index. User must NEVER need to say "sync skills."

**Quick drift check:**

```bash
python -c "
import os, urllib.request, json, ssl
SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\\.deepchat\\skills')
TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
local = [d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, 'SKILL.md')) and not d.startswith('.')]
print(f'Local: {len(local)} skills')
ctx = ssl.create_default_context()
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/qnfo/objects?prefix=qnfo/prompts/skills/&limit=200'
req = urllib.request.Request(url)
req.add_header('Authorization', f'Bearer {TOKEN}')
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10, context=ctx).read())
    r2_names = set()
    for obj in data.get('result', {}).get('objects', []):
        parts = obj.get('key', '').split('/')
        if len(parts) >= 4: r2_names.add(parts[3])
    print(f'R2: {len(r2_names)} skill dirs')
    missing = [s for s in local if s not in r2_names]
    if missing: print(f'[DRIFT] Missing from R2: {missing}')
    else: print('[OK] R2 sync: all present')
except Exception as e: print(f'[WARN] R2 check: {e}')
"
```

**If drift:** auto-run `python "%USERPROFILE%\.deepchat\skills\bootstrap_skills.py" --sync`. If sync fails after 2 retries → BLOCKING.

### 7. Auto-Sync Knowledge Graph — Seed Session Entities (MANDATORY — v3.0)

Every session creates/modifies entities that MUST be in the Knowledge Graph.

**Procedure — Quick health check:**

```bash
python -c "
import urllib.request, json, ssl
KG = 'https://graph-api.q08.workers.dev'
ctx = ssl.create_default_context()
r = urllib.request.Request(f'{KG}/stats', headers={'User-Agent': 'QNFO-Closeout/3.0'})
kg = json.loads(urllib.request.urlopen(r, timeout=10, context=ctx).read())
print(f'KG: {kg.get(\"totalNodes\")}n / {kg.get(\"totalEdges\")}e')
kp = kg.get('labelCounts', {}).get('Paper', 0)
print(f'Paper nodes: {kp}')
# Check D1 living-paper
try:
    r2 = urllib.request.Request('https://qnfo-data-api.q08.workers.dev/v2/stats',
        headers={'User-Agent': 'QNFO-Closeout/3.0'})
    d1 = json.loads(urllib.request.urlopen(r2, timeout=10, context=ctx).read())
    dp = d1.get('living_paper',{}).get('papers',0) if isinstance(d1.get('living_paper',{}),dict) else 0
    diff = abs(dp - kp)
    if diff <= 5: print(f'[OK] Paper-KG sync: diff={diff}')
    elif diff <= 20: print(f'[WARN] Paper-KG DESYNC: diff={diff}')
    else: print(f'[BLOCKING] Paper-KG SEVERE DESYNC: diff={diff}')
except: print('[WARN] D1 stats unavailable')
"
```

**If session created entities:** Auto-seed via `POST https://graph-api.q08.workers.dev/sync` with bulk action.

**GATE:** Paper-KG diff > 20 → BLOCKING. Diff 5-20 → flag handoff. Seed fail → MEDIUM.

### 8. Auto-Sync GitHub Issues — GitHub↔D1 Drift Check (MANDATORY — v3.0)

GitHub Issues (QNFO/QWAV) and D1 must stay synchronized.

**Quick drift check:**

```bash
python -c "
import urllib.request, json, os, ssl
GH = os.environ.get('GITHUB_TOKEN',''); CF = os.environ.get('CLOUDFLARE_API_TOKEN','')
if not GH or not CF: print('[GH-SYNC-SKIPPED]'); exit()
ctx = ssl.create_default_context()
r = urllib.request.Request('https://api.github.com/repos/QNFO/QWAV',
    headers={'Authorization': f'Bearer {GH}', 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'QNFO-Closeout/3.0'})
gh = json.loads(urllib.request.urlopen(r, timeout=10, context=ctx).read())
go = gh.get('open_issues_count', 0)
ACCT='edb167b78c9fb901ea5bca3ce58ccc4b'; DB='35e2e573-92f3-46ac-83c6-22f6429fc5e5'
du = f'https://api.cloudflare.com/client/v4/accounts/{ACCT}/d1/database/{DB}/query'
dr = urllib.request.Request(du, headers={'Authorization':f'Bearer {CF}','Content-Type':'application/json'},
    method='POST', data=json.dumps({'sql':\"SELECT COUNT(*) as cnt FROM tasks WHERE source='github' AND github_state='open'\"}).encode())
dd = json.loads(urllib.request.urlopen(dr, timeout=10, context=ctx).read())
do = dd.get('result',[{}])[0].get('results',[{}])[0].get('cnt',0)
print(f'GH open:{go} D1 pending:{do}')
if go != do: print(f'[DRIFT] Run skill_view(\"github-cloudflare-sync\") -> run_full_sync()')
else: print('[OK] GitHub-D1 in sync')
"
```

**GATE:** Drift → immediately run `github-cloudflare-sync` full sync. Fail after 2 retries → BLOCKING.

### 9. Auto-Sync Zenodo — Verify Published DOIs (MANDATORY — v3.0)

Every published Zenodo DOI must have a KG `ZenodoRecord` node.

```bash
python -c "
import urllib.request, json, os, ssl
ZT = os.environ.get('ZENODO_TOKEN','')
if not ZT: print('[ZENODO-SYNC-SKIPPED]'); exit()
ctx = ssl.create_default_context()
h = {'Authorization': f'Bearer {ZT}'}
r = urllib.request.Request('https://zenodo.org/api/deposit/depositions?size=50&sort=-modified', headers=h)
deps = json.loads(urllib.request.urlopen(r, timeout=15, context=ctx).read())
pub = [{'doi':d['doi'],'t':d.get('title','')[:50]} for d in deps if d.get('submitted') and d.get('doi')]
print(f'Zenodo published: {len(pub)}')
# Get KG ZenodoRecord DOIs
k = urllib.request.Request('https://graph-api.q08.workers.dev/nodes?label=ZenodoRecord',
    headers={'User-Agent':'QNFO-Closeout/3.0'})
kgz = json.loads(urllib.request.urlopen(k, timeout=10, context=ctx).read())
kdois = set()
for n in kgz.get('nodes',[]):
    d = n.get('properties',{}).get('doi','')
    if d: kdois.add(d)
miss = [p for p in pub if p['doi'] not in kdois]
if miss:
    for m in miss: print(f'[ZENODO-KG-GAP] {m[\"doi\"]}: {m[\"t\"]}')
    print(f'[ACTION] Seed {len(miss)} ZenodoRecord nodes to KG via POST /sync')
else: print(f'[OK] All {len(pub)} Zenodo DOIs in KG ({len(kdois)} total)')
"
```

**Auto-remediate:** Seed missing DOIs via `POST /sync` with ZenodoRecord + PUBLISHED_AS edge. Fail → MEDIUM (flags handoff).

### 10. Auto-Sync Cloudflare Resources — Infrastructure Health Check (MANDATORY — v3.0)

Cloudflare resources must be cross-referenced against baselines and KG.

**Quick health check:**

```bash
python -c "
import urllib.request, json, os, ssl
T = os.environ.get('CLOUDFLARE_API_TOKEN','')
if not T: print('[CF-SYNC-SKIPPED]'); exit()
A='edb167b78c9fb901ea5bca3ce58ccc4b'; ctx=ssl.create_default_context()
def cf(e):
    u=f'https://api.cloudflare.com/client/v4/accounts/{A}/{e}'; r=urllib.request.Request(u)
    r.add_header('Authorization',f'Bearer {T}')
    return json.loads(urllib.request.urlopen(r,timeout=10,context=ctx).read())
res={'D1':len(cf('d1/database').get('result',[])),'KV':len(cf('storage/kv/namespaces').get('result',[])),
'Vec':len(cf('vectorize/v2/indexes').get('result',[])),'Pages':len(cf('pages/projects').get('result',[])),
'Workers':len(cf('workers/scripts').get('result',[])),'Queues':len(cf('queues').get('result',[]))}
bl={'D1':5,'KV':1,'Vec':3,'Pages':10,'Workers':33,'Queues':1}
for r,c in res.items():
    b=bl[r]; f='DRIFT' if abs(c-b)>0 else 'OK'
    print(f'  {r}: {c} (bl {b}) [{f}]')
    if abs(c-b)>2: print(f'[VIOLATION] {r}:{c} vs bl {b}')
# Lifecycle
try:
    l=urllib.request.Request('https://qnfo-lifecycle.q08.workers.dev/health',headers={'User-Agent':'Mozilla/5.0'})
    lh=json.loads(urllib.request.urlopen(l,timeout=5,context=ctx).read())
    print(f'  Lifecycle: {lh.get(\"status\",\"?\")}')
except: print('  [WARN] Lifecycle Worker unreachable')
# R2
try:
    r2=urllib.request.Request(f'https://api.cloudflare.com/client/v4/accounts/{A}/r2/buckets/qnfo',
        headers={'Authorization':f'Bearer {T}'})
    rd=json.loads(urllib.request.urlopen(r2,timeout=10,context=ctx).read())
    print(f'  R2: {\"OK\" if rd.get(\"success\") else \"UNREACHABLE\"}')
except: print('  [WARN] R2 check failed')
"
```

**GATE:** Resources >2 outside baseline → flag for full infrastructure audit. Lifecycle down → MEDIUM. R2 unreachable → BLOCKING.

### 11. Update Decision Log

If new decisions were made:
```bash
# Download current log
npx wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --file=<temp>

# Append new decisions to temp file

# Upload updated log
npx wrangler r2 object put qnfo/audit/decisions/DECISION-LOG.md --file=<temp>
```

### 12. Update Project State

```bash
# Upload state JSON
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-state-file>
```

### 13. Archive to Local Storage

```bash
Move-Item -Path "<project>" -Destination ".\archive\projects\YYYY\MM\<name>\"
```

### 14. Clean Up Temporary Files — AGGRESSIVE JIT ENFORCEMENT

**HARD RULE:** This machine is a thin client. The ONLY files that persist locally are the import surface (`%APPDATA%\DeepChat\skills\`). Everything else MUST be cleaned up at session closeout. Never use `-ErrorAction SilentlyContinue` — verify every deletion with `Test-Path`.

**Step 14.1: Orphan `_*` file scan and removal**
```bash
Get-ChildItem -File -Name | Where-Object { $_ -match '^_' } | ForEach-Object { Remove-Item $_; Write-Output "CLEANED: $_" }
# VERIFY: No _* files remain
$orphans = Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }
if ($orphans) { Write-Output "FAILED: Orphans remain: $orphans"; exit 1 }
Write-Output "Orphan scan: CLEAN"
```

**Step 14.2: Python cache cleanup**
```bash
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__"; Write-Output "CLEANED: __pycache__" }
```

**Step 14.3: Publication draft artifact cleanup (v2.2 — MANDATORY for publication sessions)**

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

**Step 14.4: Project file cleanup (outside import-surface)**
- If any project files were pulled from R2 during the session (e.g., in workspace projects/ or workspace QWAV/):
  - If modified: re-upload to R2 FIRST, then delete local copy
  - If unmodified: delete local copy immediately (they're stale caches)
- The goal: ZERO project files persist locally between sessions

**Step 14.5: Final verification**
```bash
$remaining = Get-ChildItem -Recurse -File -Name | Where-Object { 
    $_ -match '^_' -and $_ -notmatch '^skills\\' -and $_ -notmatch '^templates\\' -and $_ -notmatch '^agents\\' -and $_ -notmatch '^config\\' -and $_ -notmatch '^audit\\'
}
if ($remaining) { Write-Output "WARNING: Non-import-surface files detected: $remaining" }
```
Only `%APPDATA%\DeepChat\skills\` files should remain. Everything else is clutter.

### 15. Final Verification — Full Closeout Checklist

Execute the Close-Out Checklist below and verify ALL phases pass. Deliver the completed checklist as part of the closeout summary. (CLOSEOUT-CHECKLIST template deprecated v2026-07-11 — checklist is inline below.)

---

## Close-Out Checklist (Summary)

Full verification checklist (CLOSEOUT-CHECKLIST template deprecated — checklist inline):
- [ ] Step 0: Autonomous trigger detection passed (all tasks complete)
- [ ] Step 0.1: WBS Completion Gate passed (all project phases verified complete)
- [ ] Step 1: All commits verified
- [ ] Step 2: ALL planned tasks executed (Task Execution Verification)
- [ ] Step 2.1: Execution Ratio Audit passed (ratio >= 0.5)
- [ ] Step 3: ALL projects have HANDOFF.md updated (Project Handoff Init)
- [ ] Step 4: Audit trail exported to R2
- [ ] Step 5: Discovery Index updated (qnfo/discovery/index.json)
- [ ] Step 6: Skills auto-synced (local → GitHub → R2 → D1) — NO DRIFT
- [ ] Step 7: Knowledge Graph auto-synced (Paper-KG diff ≤ 5, session entities seeded)
- [ ] Step 8: GitHub Issues auto-synced (GH↔D1 no drift)
- [ ] Step 9: Zenodo auto-synced (all published DOIs in KG)
- [ ] Step 10: Cloudflare resources auto-synced (baselines verified, Lifecycle healthy, R2 OK)
- [ ] Step 11: Decision log updated
- [ ] Step 12: Project state updated
- [ ] Step 13: Archive completed
- [ ] Step 14: Temp files cleaned
- [ ] Step 15: Full CLOSEOUT-CHECKLIST passed (all phases)

---

## Handoff Document

When handing off to another agent:
```bash
# Create handoff directly (HANDOFF template deprecated v2026-07-11 — use inline format):
# Parameters: type, scope, current_state, next_steps, blockers, branch, commit
# See closeout-manager skill for full handoff protocol.
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
| **Skipping auto-sync steps (v3.0)** | KG, GitHub, Zenodo, or CF drift goes undetected | Steps 6-10: verify Skills, KG, GitHub, Zenodo, and CF Resources every closeout |
| **Closing out with system drift** | Next session starts with stale state | GATE: all 5 auto-sync checks (Steps 6-10) must pass or be flagged |
| **Waiting for user to say "sync X"** | User should never manage system state | Every closeout auto-verifies: Skills, KG, GitHub↔D1, Zenodo↔KG, CF resources |

---

*closeout-manager skill v3.0 — AUTONOMOUS. Detects completion and auto-initiates. Never waits for "TERMINATE." Auto-syncs Knowledge Graph, GitHub Issues, Zenodo DOIs, Cloudflare Resources, and Skills on every closeout. Integrates gumbo-style syn-fork pipeline for all ecosystem primitives. User NEVER needs to remind the system to maintain itself.*

---

*closeout-manager v3.0 — MANDATORY AUTO-SYNC. 5-dimensional sync: Skills (local↔GitHub↔R2↔D1), Knowledge Graph (session entities + Paper-KG gap), GitHub Issues (GH↔D1 drift), Zenodo (published DOI↔KG), Cloudflare Resources (baselines + Lifecycle + R2 health). Git-on-Cloudflare investigation documented in §Appendix A.**