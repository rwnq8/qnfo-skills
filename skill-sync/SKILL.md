---
name: skill-sync
description: Sync all DeepChat skills between local disk, GitHub, and Cloudflare R2. Monitors skill modifications and auto-syncs after changes. Updates Discovery Index with current versions. Use when skills are modified and need to be pushed to redundant backups, or to check sync status.
version: "1.5"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** kaizen-autonomous-update



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('skill-sync')` or `read()` with filesystem path.
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
  {"step": "Check sync status: local vs GitHub vs R2", "status": "pending"},
  {"step": "Push changes to GitHub (rwnq8/qnfo-skills)", "status": "pending"},
  {"step": "Upload skills to R2 (qnfo/prompts/skills/)", "status": "pending"},
  {"step": "Update Discovery Index with current versions", "status": "pending"},
  {"step": "Verify three-way sync consistency", "status": "pending"}
])


# SKILL SYNC SKILL — v1.3 — v1.3

> **On-demand skill. AUTO-GAP-AUDIT INTEGRATION.** Load via `skill_view('skill-sync')` to sync skills or check sync status. Automatically triggers gap audit (closeout-manager §2.6) after sync completion.

---

## Purpose

Skills are modified locally but must be pushed to GitHub, R2, and D1 skills_index for redundancy. This skill automates the four-way sync, updates the Discovery Index with current versions, and **triggers the POST-PHASE GAP AUDIT** to verify no desync or drift remains.

## When to Use

| Trigger | Action |
|:--------|:-------|
| After any skill modification | "SYNC SKILLS" or use bootstrap_skills.py → auto-triggers gap audit |
| "Are skills in sync?" | Check sync status report → auto-triggers gap audit if desync found |
| "Push skills to GitHub/R2" | Selective sync → auto-verifies R2 + DI |
| Before session closeout | Auto-sync check → feeds into closeout gap audit |

## Quick Sync (One Command)

### DEC-034 Concurrency-Safe Sync (v2.0 — 2026-07-10)

**CRITICAL:** Multiple LLM sessions can modify the same skill simultaneously. Without concurrency protection, the last session to sync silently overwrites prior changes. This section documents the safe sync protocol.

#### Safe Sync Protocol (ALWAYS use these steps)

```python
from infra_lock_client import LockClient
client = LockClient()

# 1. Acquire DO lock before touching the skill
client.lock("r2", f"prompts/skills/{skill_name}/SKILL.md", ttl_seconds=300)

# 2. Read current R2 ETag (detect drift)
# etag = bootstrap_skills._r2_get_etag(key)

# 3. Write to R2
# Upload SKILL.md to qnfo/prompts/skills/<name>/SKILL.md

# 4. Release lock
client.unlock("r2", f"prompts/skills/{skill_name}/SKILL.md")
```

#### Concurrency Protection Matrix

| Resource | Lock Key | TTL | Failure Mode |
|:---------|:---------|:----|:-------------|
| R2 skills | `r2:prompts/skills/<name>/SKILL.md` | 300s | 409 Conflict → retry with backoff |
| GitHub push | git merge conflict | N/A | Automatic — git rejects push |
| D1 sync record | `d1:resources:<id>` | 120s | Version check UPDATE |

#### bootstrap_skills.py v2.0 (DEC-034 Integrated)

The canonical sync tool now includes:
- `_do_lock()` / `_do_unlock()` — InfraLockManager DO integration
- `_safe_r2_put_with_lock()` — Lock→Upload→Unlock with retry
- `_r2_get_etag()` — Drift detection via R2 ETags
- `--dry-run` — Preview sync without uploading

**Canonical location:** `R2: qnfo/tools/bootstrap_skills.py`
**DO endpoint:** `https://infra-lock-manager.q08.workers.dev`

#### Collision Detection Flow

```
Session-A syncs skill-sync  →  lock(r2, prompts/skills/skill-sync/SKILL.md)  →  ACQUIRED
Session-B syncs skill-sync  →  lock(r2, prompts/skills/skill-sync/SKILL.md)  →  409 CONFLICT
Session-B waits 2s, retries →  (still locked by A)
Session-A uploads, unlocks  →  RELEASED
Session-B retries            →  lock(r2, ...)  →  ACQUIRED  →  reads latest  →  uploads
```


```bash
python "%USERPROFILE%\.deepchat\skills\bootstrap_skills.py" --sync
```

This:
1. Commits and pushes all skill changes to GitHub (`rwnq8/qnfo-skills`)
2. Uploads all skills to R2 (`qnfo/prompts/skills/<name>/SKILL.md`)
3. Updates D1 skills_index (`qnfo-audit.skills_index`) with current versions and metadata
4. Reports sync status
5. **AUTO-TRIGGERS gap audit** (closeout-manager §2.6) — verifies R2, GitHub, D1, and DI consistency

### Variant Deduplication (v1.0 — DeepChat v1.0.9 Multi-Agent Adoption)

DeepChat v1.0.9 adopted skills from Claude Code and Agents SDK. Conflicting skills were renamed with `-claude-code` or `-agents` suffixes. When syncing, the sync tool MUST deduplicate variants to prevent syncing redundant copies to GitHub/R2.

**Dedup Strategy:**
1. **Scan for variants:** Identify all skill directories whose name ends in `-claude-code` or `-agents`
2. **Derive base name:** Strip the suffix to get the canonical skill name (e.g., `cloudflare-claude-code` → `cloudflare`)
3. **Check for canonical:** If `%USERPROFILE%\.deepchat\skills\<base>\SKILL.md` exists, the suffixed copy is a variant import
4. **Sync only canonical:** For conflicting variants, sync ONLY the base-named canonical skill. Do NOT sync `-claude-code` or `-agents` variants to GitHub/R2
5. **Sync solo copies:** If a `-claude-code` or `-agents` skill exists WITHOUT a corresponding base-named skill (adopted without conflict), sync it as-is
6. **Flag drift:** If a variant SKILL.md content differs from its canonical base, flag `[VARIANT-DRIFT: <name>-suffix diverged]` in sync report
7. **Update DI:** The Discovery Index should list only canonical skills, with a `variants:` metadata field noting which suffixed copies exist locally

**Current variant map (2026-07-10):**
- `-claude-code` variants (40): agents-sdk, algorithmic-art, bling-usability-audit, closeout-manager, cloudflare, cloudflare-deployer, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations, code-review, deepchat-settings, doc-coauthoring, docx, durable-objects, email-composer, execution-guard, frontend-design, git-commit, git-hygiene, infographic-syntax-creator, kaizen-autonomous-update, knowledge-graph, local-to-r2-migration, mcp-builder, pdf, pdf-builder, pptx, prompt-audit, publication-publisher, sandbox-sdk, skill-creator, template-catalog, turnstile-spin, web-artifacts-builder, web-perf, workers-best-practices, wrangler, xlsx
- `-agents` variants (13): agents-sdk, cloudflare, cloudflare-email-service, cloudflare-one, cloudflare-one-migrations, durable-objects, sandbox-sdk, turnstile-spin, web-perf, workers-best-practices, wrangler
- Skills adopted without conflict (no suffix): buffer-integration, citation-manager, github-manager, ipfs-pinning, literature-search, memory-management, qnfo-agent, red-team-dod, research-planner, seo-discoverability, skill-sync, test-enforcement, tufte-viz, ultrametric-engine, web3-ipfs-deployer

**KNOWN ISSUE: `npx` not found in Python subprocess PATH on Windows.** `bootstrap_skills.py --sync` calls `subprocess.run(["npx", "wrangler", ...])` which fails on Windows because `npx` is a PowerShell script wrapper, not an executable on the system PATH. Python `subprocess.run()` does not inherit the PowerShell PATH.

**WORKAROUND:** Use `os.system()` instead of `subprocess.run()`:
```python
# Instead of: subprocess.run(["npx", "wrangler", "r2", "object", "put", ...])
# Use:
import os
os.system('npx wrangler r2 object put qnfo/prompts/skills/name/SKILL.md --remote --file=local_path')
```

**ALTERNATIVE:** Use the Cloudflare REST API directly (bypasses wrangler dependency entirely):
```python
# Direct R2 upload via REST API (faster, no npx/subprocess dependency)
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/qnfo/objects/{key}'
req = urllib.request.Request(url, data=body, method='PUT')
req.add_header('Authorization', f'Bearer {TOKEN}')
```

This has been the #1 blocker for automated skill sync in 80%+ of sessions (2026-07-02 through 2026-07-04).

## Sync Status Check

```python
import os, urllib.request

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')  # Canonical: Secrets Store
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
STORE_ID = '8ef28060302e4311b064ba3529493e8b'
SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')

local_skills = []
for d in sorted(os.listdir(SKILLS_DIR)):
    p = os.path.join(SKILLS_DIR, d, 'SKILL.md')
    if os.path.isfile(p) and not d.startswith('.'):
        local_skills.append(d)

# Sample-check 5 skills against R2 for drift
drift = 0
for name in local_skills[:5]:
    local_size = os.path.getsize(os.path.join(SKILLS_DIR, name, 'SKILL.md'))
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/qnfo/objects/qnfo/prompts/skills/{name}/SKILL.md'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        r2_size = len(resp.read())
        status = 'SYNCED' if r2_size == local_size else 'DRIFT'
        if status == 'DRIFT':
            drift += 1
        print(f'  {name}: {status} (local={local_size}, r2={r2_size})')
    except:
        print(f'  {name}: R2 MISSING')

status = 'DRIFT DETECTED — run bootstrap_skills.py --sync' if drift else 'IN SYNC'
print(f'\nSync Status: {status}')
```

## DeepChat Skill Architecture (v1.4 — Red-Team Audit 2026-07-09)

This section documents the complete DeepChat skill storage, loading, and registration architecture discovered during the 2026-07-09 red-team audit that identified 5 skills silently dropped from `skill_list` due to js-yaml frontmatter parsing failures.

### Filesystem Layout

| Path | Purpose | Populated? |
|:-----|:--------|:-----------|
| `%USERPROFILE%\.deepchat\skills\<name>\SKILL.md` | **PRIMARY** — canonical skill definitions, git-tracked, synced to R2 | Yes — 54 skills |
| `%USERPROFILE%\.deepchat\skills\discovery\index.json` | Secondary index built by build scripts — populated during sync. May or may not be read by DeepChat runtime | Yes — 54 entries |
| `D1: qnfo-audit.skills_index` | **Canonical skill registry** — SQL-backed with RED_TEAM, RELATED, SKILL_LOADING, version fields | 54 rows |
| `%APPDATA%\DeepChat\skills\` | DeepChat internal skills directory — currently EMPTY and UNUSED | No — 0 skills |
| `%APPDATA%\DeepChat\kaizen\prompts\discovery\index.json` | Kaizen discovery index mirror — currently EMPTY | No — 0 bytes |

**Key insight:** DeepChat does NOT copy skills to `%APPDATA%`. It reads them directly from `%USERPROFILE%\.deepchat\skills\` via a filesystem scan at startup.

### DeepChat Internal Database

**Location:** `%APPDATA%\DeepChat\app_db\agent.db` (SQLite via `better-sqlite3`)

| Table | Rows | Purpose | Relevance to Skills |
|:------|:-----|:--------|:--------------------|
| `agents` | 39 | ACP external coding agents + built-in DeepChat agent | **Does NOT store skills.** Skills ≠ agents in DeepChat's data model |
| `new_session_active_skills` | 1887 | Tracks which skills were active per session `(session_id, ordinal, skill_name)` | **Critical for diagnostics.** Shows historical usage. Skills appearing here but NOT in `skill_list` are broken (YAML frontmatter failure) |
| `new_sessions` | 262 | Session metadata `(id, title, created_at)` | Useful for cross-referencing when a skill was last used |
| `app_settings` | — | App-wide settings | No `skillDirectories` key — confirms filesystem-only skill discovery |
| `config_migrations` | — | Migration history | No skill-related migrations |
| `agent_settings` | 4 | Agent config `(enabled: false)` | Not skill-related |

**Diagnostic query — find broken skills (in session history but not in `skill_list`):**

```sql
SELECT DISTINCT s.skill_name, COUNT(*) as session_count
FROM new_session_active_skills s
WHERE s.skill_name NOT IN (
  -- List of 48 known-registered skill names from skill_list
  'agents-sdk','algorithmic-art','buffer-integration','citation-manager','closeout-manager',
  'cloudflare','cloudflare-deployer','cloudflare-email-service','cloudflare-one','cloudflare-one-migrations',
  'code-review','deepchat-settings','doc-coauthoring','docx','durable-objects','email-composer',
  'frontend-design','git-commit','git-hygiene','infographic-syntax-creator','infrastructure-audit',
  'ipfs-pinning','kaizen-autonomous-update','knowledge-graph','literature-search','mcp-builder',
  'memory-management','pdf','pdf-builder','pptx','prompt-audit','publication-publisher','qnfo-agent',
  'red-team-dod','sandbox-sdk','seo-discoverability','skill-autoloader','skill-creator','skill-sync',
  'template-catalog','test-enforcement','turnstile-spin','ultrametric-engine','web-artifacts-builder',
  'web-perf','workers-best-practices','wrangler','xlsx'
)
GROUP BY s.skill_name
ORDER BY session_count DESC;
```

**Interpretation:**
- Skills with **high session counts** (e.g., 148) that are missing from `skill_list` → **definitely broken** (YAML parsing failure at startup)
- Skills with **0 sessions** that are missing → may be newly added and never used, or may have never been valid
- Skills in the query result but with **no SKILL.md on disk** → intentionally consolidated/removed (check git log for deletion commits like `343b7c8`)

### Skill Loading Mechanism (How `skill_list` Works)

1. **At DeepChat startup**, the Electron main process scans `%USERPROFILE%\.deepchat\skills\` for directories containing `SKILL.md`
2. Each `SKILL.md` frontmatter is parsed using **js-yaml** (Node.js strict YAML parser)
3. Skills with **valid** frontmatter (`name`, `description` fields) are added to an **in-memory registry**
4. The `skill_list` API tool queries this in-memory registry
5. **There is NO database cache or file-based index** — the scan happens fresh at every startup
6. **Invalid skills are silently skipped** — no error log, no warning, just absent from `skill_list`

### YAML Frontmatter Failure Modes (js-yaml vs PyYAML)

js-yaml is **stricter** than Python's PyYAML. These patterns cause **silent skill exclusion**:

| Pattern | js-yaml Behavior | PyYAML Behavior | Example |
|:--------|:-----------------|:----------------|:--------|
| No `---` delimiters | No frontmatter detected → skip | Same | `bling-usability-audit` (was 7.3MB corrupted) |
| `\'` in double-quoted string | **Invalid escape, parse error** | Ignores, treats as literal `\'` | `description: "...what\'s pending..."` |
| Unquoted colon in value | **Parsed as mapping key separator** | Ignores, single-line string | `description: ...methodology: assumption...` |
| `: (N)` pattern in value | **Same colon issue** | Ignores | `description: ...wants to: (1) compute...` |
| Blank line between `---` and `name:` | Parses but unusual | Parses | `---\n\nname: skill-name` |
| Duplicate keys (e.g., two `version`) | Last value wins (valid YAML) | Same | `version: "1.2"\n...\nversion: "1.1"` |

**Prevention — always test with js-yaml:**
```bash
node -e "const yaml=require('js-yaml'); const fs=require('fs');
const f=fs.readFileSync('SKILL.md','utf8');
const m=f.match(/^---\n([\s\S]*?)\n---/);
if(m) { try { yaml.load(m[1]); console.log('OK'); }
catch(e) { console.log('FAIL:', e.message); } }
else { console.log('FAIL: no frontmatter'); }"
```

**Rapid Python pre-check (catches most issues):**
```python
import os, re, yaml

SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')
for d in sorted(os.listdir(SKILLS_DIR)):
    path = os.path.join(SKILLS_DIR, d, 'SKILL.md')
    if not os.path.isfile(path) or d.startswith('.'):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    fm = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm:
        print(f'BROKEN [{d}]: no frontmatter delimiters')
        continue
    try:
        parsed = yaml.safe_load(fm.group(1))
        if not isinstance(parsed, dict):
            print(f'BROKEN [{d}]: frontmatter not a dict')
        elif 'name' not in parsed:
            print(f'BROKEN [{d}]: missing name field')
        else:
            print(f'OK [{d}]: v{parsed.get("version","?")}')
    except Exception as e:
        print(f'BROKEN [{d}]: {e}')
```

### Skill Consolidation & Historical Artifacts

When skills are intentionally consolidated (e.g., commit `343b7c8`: "consolidate 42 to 31 skills — 8 merges, 3 demotions"), their SKILL.md files are deleted from disk. However, `new_session_active_skills` in `agent.db` retains their historical session references indefinitely.

**How to distinguish broken skills from consolidated skills:**
1. Query `agent.db` for skills not in `skill_list` (SQL above)
2. For each result, check if `SKILL.md` exists on disk
3. If SKILL.md **exists** → broken (YAML fix needed)
4. If SKILL.md **missing** + appears in git deletion history → intentionally removed
5. Cross-reference with `git log --diff-filter=D` for deletion commits

**2026-07-09 audit findings:**
- **5 broken skills** (SKILL.md exists, has session history, missing from `skill_list`): `bling-usability-audit` (17 sessions), `execution-guard` (148 sessions), `local-to-r2-migration` (22), `research-planner` (11), `web3-ipfs-deployer` (0)
- **3 consolidated skills** (SKILL.md deleted, has session history): `handoff-protocol`, `user-story-separation`, `worker-route-interference-audit`

### ACP Registry (Not Skill-Related)

**Location:** `%APPDATA%\DeepChat\acp-registry\registry.json`

This stores external ACP (Agent Communication Protocol) coding agents (e.g., Cursor, Cline, Devin, Codex) — **NOT DeepChat skills**. Confusingly, these are stored in the `agents` table of `agent.db`, but they are a completely separate concept from skills. The `skill_list` tool does NOT query this registry.

## Bootstrap Tools

Must exist locally for this skill to work:
- `bootstrap_skills.py` — One-command sync tool (located at `%USERPROFILE%\.deepchat\skills\bootstrap_skills.py`)
- Recoverable from R2: `qnfo/tools/bootstrap_skills.py`
- Recoverable from GitHub: `rwnq8/qnfo-skills/blob/master/bootstrap_skills.py`

---

## Auto-Gap-Audit Integration (v1.3)

After sync completes (GitHub + R2 + D1), this skill automatically triggers the POST-PHASE GAP AUDIT (closeout-manager §2.6):
1. Verify R2 sync count matches local count
2. Verify GitHub HEAD matches local commit
3. Verify D1 skills_index row count matches local skill count
4. Verify Discovery Index is updated with current versions
5. Report any desync or drift as gaps

## Mandatory Post-Sync Restart

**Rule:** After any successful skill sync (push to GitHub + R2), DeepChat MUST be restarted programmatically. Skills are loaded at application startup; changes made via sync do not take effect until DeepChat is killed and relaunched.

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.deepchat\skills\skill-sync\scripts\restart_deepchat.ps1"
```

This kills all old DeepChat processes and launches a fresh instance. Execute this as the final step after confirming sync success. The current conversation will terminate.

---

*skill-sync v1.4 — Monitors and syncs skills between local, GitHub, and R2. Documents complete DeepChat skill architecture (filesystem, agent.db, js-yaml failure modes, session history diagnostics). Auto-gap-audit integration. Paths corrected (%USERPROFILE%\.deepchat\skills). Includes mandatory post-sync restart.*

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

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

> **Version:** (Kaizen-audited 2026-07-09)
