---
name: github-cloudflare-sync
version: "1.2"
description: "AUTONOMOUS bidirectional sync between GitHub Issues/Milestones/Projects and Cloudflare D1 qnfo-audit. GitHub is CANONICAL for skills repo and project files/archives (ADR-001 REVOKED 2026-07-14). Priority 1 — auto-loads at session start when GITHUB_TOKEN is available. Runs sync verification, drift detection, and auto-remediation without user prompting. Use when user says 'sync GitHub,' 'sync issues,' 'cross-reference GitHub and D1,' 'check GitHub alignment,' or when infrastructure-audit detects GitHub↔D1 drift."
related: infrastructure-audit, kaizen-autonomous-update, execution-guard, closeout-manager
category: infrastructure
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification — negative verification. (2) Assumption Challenge — state and test every assumption. (3) Edge Case Check — empty/null/max/boundary/desync. (4) DoD Integration — verify all criteria met with tool evidence. (5) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** infrastructure-audit, kaizen-autonomous-update, execution-guard, closeout-manager

---

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** during response generation. Loading is triggered automatically via `skill_view('github-cloudflare-sync')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` detects task patterns and handles all skill loading.
**Pinning:** This skill is [Priority 1 — auto-loads at session start when GITHUB_TOKEN env var is present].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\github-cloudflare-sync\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get qnfo/prompts/skills/github-cloudflare-sync/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: github-cloudflare-sync]` and best-effort knowledge

---

# GITHUB-CLOUDFLARE SYNC SKILL — v1.0

> **AUTONOMOUS BIDIRECTIONAL SYNC. DRIFT DETECTION. AUTO-REMEDIATION. GAP-AUDIT INTEGRATION. CREATED 2026-07-11.**
> Key finding: 55 QNFO skills exist; ZERO handle GitHub↔Cloudflare sync. This skill fills that gap.

---



## Full-Stack Integration (FSI v1.0)

*This skill is part of the QNFO full-stack architecture per `FULL-STACK-INTEGRATION.md` (R2: `qnfo/FULL-STACK-INTEGRATION.md`).*

GitHub issues MUST stay synced with D1 qnfo-audit.tasks. Drift > 5 triggers auto-remediation.

**Cross-system enforcement:** Run `python scripts/safety_gate.py --check` before any D1/R2 mutation.

## execute_plan (MANDATORY — Before Any Execution)

### Execution Protocol

1. **Populate update_plan** with this skill's workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (D1 query results, GitHub API responses, curl output)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

```text
update_plan([
  {"step": "[P1-T1] Verify GITHUB_TOKEN and CLOUDFLARE_API_TOKEN available", "status": "pending"},
  {"step": "[P1-T2] Pull all GitHub issues from QNFO/QWAV via REST API", "status": "pending"},
  {"step": "[P1-T3] Pull GitHub milestones and map to D1 phases", "status": "pending"},
  {"step": "[P1-T4] Query D1 qnfo-audit.tasks for all github-sourced tasks", "status": "pending"},
  {"step": "[P1-T5] Cross-reference: detect drift (GH≠D1)", "status": "pending"},
  {"step": "[P1-T6] Auto-remediate: upsert missing/divergent tasks to D1", "status": "pending"},
  {"step": "[P1-T7] Update github_labels, github_state columns on changed tasks", "status": "pending"},
  {"step": "[P1-T8] Write sync report to D1 project_ledger for audit trail", "status": "pending"},
  {"step": "[P1-T9] Generate sync summary with counts and drift report", "status": "pending"},
])
```

---

## Autonomous Continuation Protocol (v1.0)

**All 9 sync phases execute autonomously without user intervention.** The agent MUST:

1. After ANY phase marked [EXECUTED] with tool evidence, immediately proceed to the next phase
2. Before advancing: tag `[AUTO-CONTINUE -> Phase N+1]` in the response
3. If a phase fails: tag `[BLOCKED: reason]`, skip to next, aggregate failures
4. At completion of all phases: tag `[SYNC-COMPLETE: N inserts, M updates, K drifts detected]`
5. Never wait for user confirmation between sync phases

**ANTI-PATTERN:** User should NEVER need to say "CONTINUE" between sync phases.

---

## Purpose

The #1 cause of GitHub↔Cloudflare task drift is agents working in only one system and forgetting to update the other. This skill automates bidirectional synchronization between GitHub Issues (QNFO/QWAV) and Cloudflare D1 (`qnfo-audit.tasks`), ensuring both systems always reflect the same project/task state.

## When to Use

| Trigger | Action |
|:--------|:-------|
| Session startup | Auto-run if GITHUB_TOKEN is available (checks for drift) |
| "Sync GitHub" / "Sync issues" / "Sync projects" | Full bidirectional sync |
| "Check GitHub alignment" / "Cross-reference GitHub and D1" | Drift detection only |
| Infrastructure audit detects GitHub↔D1 drift | Full sync + auto-remediate |
| After bulk issue changes on GitHub | Pull changes into D1 |
| Before claiming project completion | Verify all related GitHub issues are closed |
| Kaizen update session startup | Run as Phase 0 pre-flight check |

---

## Bi-directional Sync Protocol

### Phase 1: Token Validation (GATE)

**GATE:** Before ANY sync operation, verify both tokens are available and valid.

```python
# Self-contained sync script — no external dependencies
import urllib.request, json, os, ssl, sys
from datetime import datetime, timezone

# === CONFIG (all values embedded — no external reads) ===
GITHUB_REPO = "QNFO/QWAV"
GITHUB_API = "https://api.github.com/repos/" + GITHUB_REPO
CF_ACCOUNT = "edb167b78c9fb901ea5bca3ce58ccc4b"
D1_DB_ID = "35e2e573-92f3-46ac-83c6-22f6429fc5e5"
D1_QUERY_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/d1/database/{D1_DB_ID}/query"

GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")

def validate_tokens():
    """Verify both tokens are present and working."""
    errors = []
    
    # Test GitHub token
    if not GH_TOKEN:
        errors.append("GITHUB_TOKEN not set in environment")
    else:
        try:
            req = urllib.request.Request(f"{GITHUB_API}/issues?per_page=1",
                headers={"Authorization": f"Bearer {GH_TOKEN}",
                         "Accept": "application/vnd.github.v3+json",
                         "User-Agent": "QNFO-GH-CF-Sync/1.0"})
            resp = urllib.request.urlopen(req, timeout=10,
                context=ssl.create_default_context())
            data = json.loads(resp.read())
            if not isinstance(data, list):
                errors.append(f"GitHub token test failed: {data.get('message', 'unknown')}")
            else:
                print(f"[OK] GitHub token valid — repo accessible")
        except Exception as e:
            errors.append(f"GitHub token test failed: {e}")
    
    # Test Cloudflare token
    if not CF_TOKEN:
        errors.append("CLOUDFLARE_API_TOKEN not set in environment")
    else:
        try:
            req = urllib.request.Request(D1_QUERY_URL,
                headers={"Authorization": f"Bearer {CF_TOKEN}",
                         "Content-Type": "application/json"},
                method="POST",
                data=json.dumps({"sql": "SELECT 1"}).encode())
            resp = urllib.request.urlopen(req, timeout=10,
                context=ssl.create_default_context())
            data = json.loads(resp.read())
            if not data.get("success"):
                errors.append(f"D1 token test failed: {data.get('errors', [])}")
            else:
                print(f"[OK] Cloudflare token valid — D1 accessible")
        except Exception as e:
            errors.append(f"D1 token test failed: {e}")
    
    if errors:
        print(f"[BLOCKED] {len(errors)} token validation failures:")
        for e in errors:
            print(f"  - {e}")
        return False
    return True
```

### Phase 2: Pull GitHub Issues (Full API Scan)

**ALL issues — both open and closed.** Paginated with 100-per-page.

```python
def pull_github_issues():
    """Pull ALL issues (open + closed) from GitHub API with pagination."""
    all_issues = []
    ctx = ssl.create_default_context()
    
    for state in ["open", "closed"]:
        page = 1
        while True:
            url = f"{GITHUB_API}/issues?state={state}&per_page=100&page={page}"
            req = urllib.request.Request(url,
                headers={"Authorization": f"Bearer {GH_TOKEN}",
                         "Accept": "application/vnd.github.v3+json",
                         "User-Agent": "QNFO-GH-CF-Sync/1.0"})
            try:
                resp = urllib.request.urlopen(req, timeout=15, context=ctx)
                issues = json.loads(resp.read())
                if not issues:
                    break
                for issue in issues:
                    # Skip pull requests (GitHub API returns PRs as issues too)
                    if "pull_request" in issue:
                        continue
                    all_issues.append({
                        "number": issue["number"],
                        "title": issue["title"],
                        "state": issue["state"],
                        "labels": [l["name"] for l in issue.get("labels", [])],
                        "body": (issue.get("body") or "")[:500],
                        "created_at": issue["created_at"],
                        "updated_at": issue["updated_at"],
                        "closed_at": issue.get("closed_at"),
                        "html_url": issue["html_url"],
                        "milestone": issue.get("milestone", {}).get("title") if issue.get("milestone") else None,
                        "milestone_number": issue.get("milestone", {}).get("number") if issue.get("milestone") else None,
                        "comments": issue.get("comments", 0),
                        "assignee": issue.get("assignee", {}).get("login") if issue.get("assignee") else None,
                    })
                page += 1
            except Exception as e:
                print(f"[WARN] GitHub API page {page} (state={state}) failed: {e}")
                break
    
    open_count = sum(1 for i in all_issues if i["state"] == "open")
    closed_count = sum(1 for i in all_issues if i["state"] == "closed")
    print(f"GitHub: {len(all_issues)} total issues ({open_count} open, {closed_count} closed)")
    return all_issues
```

### Phase 3: Pull GitHub Milestones

```python
def pull_github_milestones():
    """Pull all milestones from GitHub."""
    ctx = ssl.create_default_context()
    url = f"{GITHUB_API}/milestones?state=all&per_page=100"
    req = urllib.request.Request(url,
        headers={"Authorization": f"Bearer {GH_TOKEN}",
                 "Accept": "application/vnd.github.v3+json",
                 "User-Agent": "QNFO-GH-CF-Sync/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        milestones = json.loads(resp.read())
        result = []
        for m in milestones:
            result.append({
                "number": m["number"],
                "title": m["title"],
                "state": m["state"],
                "description": m.get("description", ""),
                "open_issues": m["open_issues"],
                "closed_issues": m["closed_issues"],
                "created_at": m["created_at"],
                "updated_at": m["updated_at"],
            })
        print(f"GitHub: {len(result)} milestones")
        return result
    except Exception as e:
        print(f"[WARN] GitHub milestones pull failed: {e}")
        return []
```

### Phase 4: Query D1 for Existing GitHub-Sourced Tasks

```python
def query_d1_tasks():
    """Query D1 for all tasks sourced from GitHub."""
    ctx = ssl.create_default_context()
    sql = """
    SELECT id, github_issue_number, title, status, priority, phase, project,
           github_state, github_labels, source, created_at, updated_at
    FROM tasks WHERE source = 'github'
    ORDER BY github_issue_number
    """
    req = urllib.request.Request(D1_QUERY_URL,
        headers={"Authorization": f"Bearer {CF_TOKEN}",
                 "Content-Type": "application/json"},
        method="POST",
        data=json.dumps({"sql": sql}).encode())
    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read())
        if data.get("success"):
            results = data.get("result", [{}])[0].get("results", [])
            print(f"D1: {len(results)} GitHub-sourced tasks")
            return {r["github_issue_number"]: r for r in results}
        else:
            print(f"[WARN] D1 query failed: {data.get('errors', [])}")
            return {}
    except Exception as e:
        print(f"[WARN] D1 query failed: {e}")
        return {}
```

### Phase 5: Drift Detection (Cross-Reference)

```python
def detect_drift(github_issues, d1_tasks):
    """Cross-reference GitHub issues against D1 tasks. Returns drift report."""
    gh_numbers = {i["number"] for i in github_issues}
    d1_numbers = set(d1_tasks.keys())
    
    drift = {
        "missing_in_d1": [],      # GitHub issues with no D1 task
        "missing_in_github": [],  # D1 tasks referencing non-existent GitHub issues
        "state_mismatch": [],     # open/closed state doesn't match
        "title_changed": [],      # Title differs
        "labels_changed": [],     # Labels differ
        "in_sync": [],            # Perfectly synced
    }
    
    # Check GitHub → D1
    for issue in github_issues:
        num = issue["number"]
        if num not in d1_numbers:
            drift["missing_in_d1"].append(num)
        else:
            d1_task = d1_tasks[num]
            synced = True
            d1_status = d1_task.get("status", "")
            gh_status = issue["state"]
            
            # State check (pending/in_progress = open, closed/completed = closed)
            d1_is_open = d1_status in ("pending", "in_progress")
            gh_is_open = gh_status == "open"
            if d1_is_open != gh_is_open:
                drift["state_mismatch"].append({
                    "number": num,
                    "gh_state": gh_status,
                    "d1_status": d1_status
                })
                synced = False
            
            # Title check
            if d1_task.get("title", "") != issue["title"]:
                drift["title_changed"].append({
                    "number": num,
                    "gh_title": issue["title"],
                    "d1_title": d1_task.get("title", "")
                })
                synced = False
            
            # Labels check
            d1_labels = json.loads(d1_task.get("github_labels", "[]"))
            gh_labels = issue["labels"]
            if set(d1_labels) != set(gh_labels):
                drift["labels_changed"].append({
                    "number": num,
                    "gh_labels": gh_labels,
                    "d1_labels": d1_labels
                })
                synced = False
            
            if synced:
                drift["in_sync"].append(num)
    
    # Check D1 → GitHub (orphaned D1 references)
    for num in d1_numbers - gh_numbers:
        if num > 0:
            drift["missing_in_github"].append(num)
    
    return drift
```

### Phase 6: Auto-Remediation (D1 Upsert)

```python
def upsert_task_to_d1(issue, d1_tasks):
    """Insert or update a D1 task from a GitHub issue."""
    num = issue["number"]
    title = issue["title"].replace("'", "''")
    gh_state = issue["state"]
    labels = issue["labels"]
    d1_status = "pending" if gh_state == "open" else "closed"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Map GitHub labels to D1 priority
    label_upper = {l.upper() for l in labels}
    if "P0" in label_upper: priority = "P0"
    elif "P1" in label_upper: priority = "P1"
    elif "P2" in label_upper: priority = "P2"
    elif "P3" in label_upper: priority = "P3"
    else: priority = "P2"
    
    # Map to phase
    phase = None
    if "PHASE 2" in title.upper() or "P2." in title.upper(): phase = "Phase 2"
    elif "PHASE 3" in title.upper() or "P3." in title.upper(): phase = "Phase 3"
    elif "PHASE 4" in title.upper() or "P4." in title.upper(): phase = "Phase 4"
    elif "HANDOFF" in title.upper(): phase = "Handoff"
    
    # Map to project name
    project = "qwav"
    project_keywords = {
        "secrets": "secrets-store", "ai gateway": "ai-gateway",
        "email": "email-agent", "queues": "research-pipeline",
        "citation": "citation-graph", "pdf builder": "pdf-builder",
        "ask qwav": "ask-qwav", "consistency": "consistency-engine",
        "qnfo.org": "qnfo-hub", "agent swarm": "agent-swarm",
        "compute cloud": "qwav-compute-cloud", "peer review": "automated-peer-review",
        "reproducibility": "reproducibility-as-code", "concept graph": "concept-graph",
        "ultrametric playground": "ultrametric-playground", "qwav-scan": "qwav-scan",
        "living paper": "living-paper", "monitoring": "platform-monitoring",
        "security": "security-headers", "dns redirect": "dns-redirect",
        "google site": "google-site-auditor", "archive": "pm-mirror-builder",
        "pytest": "test-infrastructure", "license": "portfolio-license-audit",
        "wiki": "wiki-migration", "discussion": "discussions-setup",
    }
    for keyword, proj in project_keywords.items():
        if keyword in title.lower():
            project = proj
            break
    
    labels_json = json.dumps(labels)
    existing = d1_tasks.get(num)
    
    ctx = ssl.create_default_context()
    
    if existing:
        # UPDATE
        d1_id = existing["id"]
        sql = f"""
        UPDATE tasks SET
            title = '{title}',
            status = '{d1_status}',
            priority = '{priority}',
            phase = {f"'{phase}'" if phase else "NULL"},
            project = '{project}',
            github_state = '{gh_state}',
            github_labels = '{labels_json}',
            updated_at = '{now}'
        WHERE github_issue_number = {num}
        """
        action = "updated"
    else:
        # INSERT — generate ID from issue number and title
        prefix = "GH"
        if "HANDOFF" in title.upper(): prefix = "GH-HND"
        elif any(p in title.upper() for p in ["P3.", "PHASE 3"]): prefix = "GH-P3"
        elif any(p in title.upper() for p in ["P4.", "PHASE 4"]): prefix = "GH-P4"
        elif any(p in title.upper() for p in ["P2.", "PHASE 2"]): prefix = "GH-P2"
        elif any(p in title.upper() for p in ["P1.", "PHASE 1"]): prefix = "GH-P1"
        elif "P0" in title.upper(): prefix = "GH-P0"
        elif "SPINOFF" in title.upper(): prefix = "GH-SPN"
        elif "INVESTIGATION" in title.upper(): prefix = "GH-INV"
        elif "BLOCKER" in title.upper(): prefix = "GH-BLK"
        elif "MASTER" in title.upper(): prefix = "GH-PRG"
        elif "PROJECT STATE" in title.upper(): prefix = "GH-PRG"
        
        d1_id = f"{prefix}-{num:03d}"
        body = (issue.get("body") or "")[:500].replace("'", "''")
        
        sql = f"""
        INSERT INTO tasks (id, project, title, status, priority, phase, description,
                          github_issue_number, github_state, github_labels, source,
                          created_at, updated_at)
        VALUES (
            '{d1_id}', '{project}', '{title}', '{d1_status}', '{priority}',
            {f"'{phase}'" if phase else "NULL"}, '{body}',
            {num}, '{gh_state}', '{labels_json}', 'github',
            '{now}', '{now}'
        )
        """
        action = "inserted"
    
    req = urllib.request.Request(D1_QUERY_URL,
        headers={"Authorization": f"Bearer {CF_TOKEN}",
                 "Content-Type": "application/json"},
        method="POST",
        data=json.dumps({"sql": sql}).encode())
    try:
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(resp.read())
        if data.get("success"):
            return action, d1_id
        else:
            return "failed", str(data.get("errors", []))
    except Exception as e:
        return "failed", str(e)
```

### Phase 7: Sync Report + Audit Trail

```python
def write_sync_report(drift, results, d1_tasks):
    """Write sync results to D1 project_ledger and generate summary."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    summary = {
        "timestamp": now,
        "github_issues_total": len(drift.get("in_sync", [])) + len(drift.get("missing_in_d1", [])) + len(drift.get("state_mismatch", [])),
        "d1_tasks_total": len(d1_tasks),
        "in_sync": len(drift.get("in_sync", [])),
        "missing_in_d1": len(drift.get("missing_in_d1", [])),
        "state_mismatch": len(drift.get("state_mismatch", [])),
        "title_changed": len(drift.get("title_changed", [])),
        "labels_changed": len(drift.get("labels_changed", [])),
        "missing_in_github": len(drift.get("missing_in_github", [])),
        "remediated": {"inserted": results.get("inserted", 0), "updated": results.get("updated", 0)},
    }
    
    # Write to D1 project_ledger
    evidence = json.dumps(summary)
    ctx = ssl.create_default_context()
    sql = f"""
    INSERT INTO project_ledger (project_id, session_id, phase, task_id, action, evidence, timestamp)
    VALUES ('GH-CF-SYNC', 'kaizen-2026-07-11', 0, 'SYNC-001', 'completed', '{evidence}', '{now}')
    """
    req = urllib.request.Request(D1_QUERY_URL,
        headers={"Authorization": f"Bearer {CF_TOKEN}",
                 "Content-Type": "application/json"},
        method="POST",
        data=json.dumps({"sql": sql}).encode())
    try:
        urllib.request.urlopen(req, timeout=10, context=ctx)
        print("[OK] Sync report written to D1 project_ledger")
    except Exception as e:
        print(f"[WARN] Failed to write sync report: {e}")
    
    return summary
```

---

## Full Sync Runner (Main Entry Point)

```python
def run_full_sync():
    """Execute the complete 7-phase bidirectional sync."""
    print("=" * 60)
    print("GitHub ↔ Cloudflare D1 Bidirectional Sync v1.0")
    print("=" * 60)
    
    # Phase 1: Validate tokens
    print("\n[P1] Token Validation...")
    if not validate_tokens():
        return {"error": "token_validation_failed"}
    
    # Phase 2: Pull GitHub issues
    print("\n[P2] Pulling GitHub Issues...")
    github_issues = pull_github_issues()
    if not github_issues:
        return {"error": "no_github_issues"}
    
    # Phase 3: Pull GitHub milestones (optional)
    print("\n[P3] Pulling GitHub Milestones...")
    milestones = pull_github_milestones()
    
    # Phase 4: Query D1
    print("\n[P4] Querying D1 Tasks...")
    d1_tasks = query_d1_tasks()
    
    # Phase 5: Drift detection
    print("\n[P5] Detecting Drift...")
    drift = detect_drift(github_issues, d1_tasks)
    print(f"  In sync: {len(drift['in_sync'])}")
    print(f"  Missing in D1: {len(drift['missing_in_d1'])}")
    print(f"  State mismatch: {len(drift['state_mismatch'])}")
    print(f"  Title changed: {len(drift['title_changed'])}")
    print(f"  Labels changed: {len(drift['labels_changed'])}")
    print(f"  Missing in GitHub: {len(drift['missing_in_github'])}")
    
    # Phase 6: Auto-remediate
    results = {"inserted": 0, "updated": 0, "failed": 0}
    if drift["missing_in_d1"] or drift["state_mismatch"] or drift["title_changed"] or drift["labels_changed"]:
        print(f"\n[P6] Auto-Remediating {len(drift['missing_in_d1']) + len(drift['state_mismatch'])} issues...")
        
        for issue in github_issues:
            num = issue["number"]
            needs_sync = (
                num in drift["missing_in_d1"] or
                any(m["number"] == num for m in drift["state_mismatch"]) or
                any(t["number"] == num for t in drift["title_changed"]) or
                any(l["number"] == num for l in drift["labels_changed"])
            )
            if needs_sync:
                action, d1_id = upsert_task_to_d1(issue, d1_tasks)
                results[action] = results.get(action, 0) + 1
                if action != "failed":
                    print(f"  #{num} → {action}: {d1_id}")
                else:
                    print(f"  #{num} → FAILED: {d1_id}")
        
        # Refresh D1 after batch update
        d1_tasks = query_d1_tasks()
    else:
        print("\n[P6] No remediation needed — all tasks in sync")
    
    # Phase 7: Write report
    print("\n[P7] Writing Sync Report...")
    summary = write_sync_report(drift, results, d1_tasks)
    
    print("\n" + "=" * 60)
    print("SYNC COMPLETE")
    print("=" * 60)
    for key, val in summary.items():
        print(f"  {key}: {val}")
    
    return summary

if __name__ == "__main__":
    run_full_sync()
```

---

## Agent-Side Sync Protocol (Using curl + wrangler)

### When Python is available:
```bash
# Write the sync script, execute, discard
python _github_cf_sync.py
Remove-Item _github_cf_sync.py
```

### When only curl + wrangler are available (simplified drift check):
```bash
# Phase 1: Count GitHub issues
curl -s -H "Authorization: Bearer $env:GITHUB_TOKEN" \
  "https://api.github.com/repos/QNFO/QWAV/issues?state=open&per_page=1" \
  | grep -o '"open_issues_count":[0-9]*'

# Phase 2: Count D1 GitHub-sourced tasks
npx wrangler d1 execute qnfo-audit --remote \
  --command "SELECT github_state, COUNT(*) FROM tasks WHERE source='github' GROUP BY github_state" --json

# Phase 3: If counts differ → full sync needed
```

### Sync Decision Matrix

| Condition | Action |
|:----------|:-------|
| GitHub open = D1 pending, GitHub closed = D1 closed | ✅ In sync — no action |
| GitHub open > D1 pending | 🔴 Drift detected — pull + upsert missing |
| GitHub closed > D1 closed | 🟠 Drift detected — update status |
| D1 has tasks not in GitHub | 🟡 Orphaned D1 references — flag for review |
| Token not available | ⚠️ Degraded — skip sync, flag [GH-SYNC-UNAVAILABLE] |

---

## GITHUB_TOKEN Handling

### Where GITHUB_TOKEN Lives

| Location | Purpose |
|:---------|:--------|
| `$env:GITHUB_TOKEN` (PowerShell) | Agent session — ephemeral |
| Cloudflare Secrets Store | Worker-side access: `env.MY_SECRETS.GITHUB_TOKEN` |
| Worker `wrangler.toml` binding | `[[secrets_store]] binding = "MY_SECRETS"` |

### Token Scopes Needed

| Scope | Reason |
|:------|:------|
| `repo` | Read/write issues, milestones, labels |
| `read:org` | Read organization projects |
| `read:user` | Validate token identity |

**Current token owner:** `rwnq8` (verified 2026-07-11)

---

## D1 Schema Reference (Already Deployed)

The `qnfo-audit.tasks` table already has these GitHub-sync columns:

| Column | Type | Purpose |
|:-------|:-----|:--------|
| `github_issue_number` | INTEGER | GitHub issue number (indexed for lookup) |
| `github_state` | TEXT | `open` or `closed` |
| `github_labels` | TEXT | JSON array: `["handoff","task"]` |
| `source` | TEXT | `github` or `local` |

**GATE:** These columns MUST exist before sync runs. They were added 2026-07-11.

---

## Integration with Other Skills

| Skill | Integration Point |
|:------|:-----------------|
| `infrastructure-audit` §Phase 1.8 | Runs GitHub↔D1 drift check as part of startup audit |
| `execution-guard` §1.4 | GitHub issue state factored into gap detection |
| `kaizen-autonomous-update` §Phase 0 | GitHub sync runs as pre-flight check |
| `closeout-manager` | Session closeout verifies no un-synced GitHub issues |

---

## Output Format

```
# GitHub ↔ Cloudflare D1 Sync Report
**Date:** 2026-07-11 | **Sync:** Bidirectional | **Token:** rwnq8

## Counts
| Source | Open/Pending | Closed | Total |
|:-------|:------------|:-------|:------|
| GitHub | 44 | 35 | 79 |
| D1 (github) | 44 | 35 | 79 |
| D1 (local) | 0 | 80 | 80 |

## Drift Detected
| Type | Count | Action |
|:-----|:------|:------|
| Missing in D1 | 0 | — |
| State mismatch | 0 | — |
| Title changed | 0 | — |
| Labels changed | 0 | — |

## Remediation
| Action | Count |
|:-------|:------|
| Inserted | 0 |
| Updated | 0 |

**Verdict:** ✅ ALL IN SYNC — no drift detected
```

---

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. **Output Verification** — Verify D1 counts exactly match GitHub API counts
2. **Assumption Challenge** — Test: "Does the token still work? Is GitHub API reachable? Are D1 columns present?"
3. **Edge Case Check** — Empty GitHub (0 issues), empty D1 (0 tasks), all-closed, token expired
4. **DoD Integration** — sync report written to project_ledger, all drift remediated
5. **Iteration** — retry on transient API failures, max 3

ANTI-PATTERN: User should NEVER ask about quality.

> **Version:** v1.0 (2026-07-11 — Initial creation. Fills the #1 infrastructure gap: 55 skills, zero handle GitHub↔Cloudflare bidirectional sync.)
