---
name: kaizen-autonomous-update
description: Autonomous system-wide Kaizen continuous improvement protocol. Updates all prompts, templates, skills, agents/subagents, deploys, and commits. Use when user says "UPDATE ALL FROM KAIZEN," "system update," "update all skills," "continuous improvement," "Kaizen update," "auto-update," "upgrade everything," "refresh all settings," or when Kaizen engine detects 5+ unapplied improvements.
version: "1.4"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** closeout-manager, skill-sync, github-cloudflare-sync


> **QNFO Custom Skill** — Load via `read('R2 `qnfo/prompts/skills/kaizen-autonomous-update\\SKILL.md')`
> **Template (DEPRECATED v2026-07-11):** Templates no longer maintained. All 7-phase Kaizen protocols are inline in this skill document.

---


### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('kaizen-autonomous-update')` or `read()` with filesystem path.
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
## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

### DEC-034 Lock-Before-Edit Protocol (v1.3 — 2026-07-10)

**CRITICAL:** Before modifying ANY skill file, acquire an InfraLockManager DO lock. This prevents multi-session write collisions where two sessions edit the same skill and one silently overwrites the other's changes.

#### Protocol

```python
from infra_lock_client import LockClient, LockCollision

client = LockClient()

# 1. Lock before editing
try:
    client.lock("r2", f"prompts/skills/{skill_name}/SKILL.md", ttl_seconds=600)
except LockCollision:
    # Another session is editing this skill — wait and retry
    time.sleep(3)
    client.lock("r2", f"prompts/skills/{skill_name}/SKILL.md", ttl_seconds=600)

# 2. Edit the skill

# 3. Sync (bootstrap_skills.py handles R2 upload + unlock)
# python bootstrap_skills.py --sync

# 4. Unlock (bootstrap_skills.py does this automatically)
```

#### Resource Lock Matrix for Kaizen Updates

| Phase | Resources Modified | Lock Required |
|:------|:-------------------|:-------------|
| Phase 1 (prompts) | Prompt templates | `r2:prompts/*` |
| Phase 3 (skills) | Skill SKILL.md files | `r2:prompts/skills/*/SKILL.md` |
| Phase 4 (agents) | Agent configs | `d1:agents:*` |
| Phase 6 (deploy) | Workers, R2 | `worker:*` + `r2:*` |

**DO endpoint:** `https://infra-lock-manager.q08.workers.dev`
**Client:** `infra_lock_client.py` (in infra-lock-manager workspace)


update_plan([
  {"step": "Phase 0: Pull Discovery Index + run Kaizen audit", "status": "pending"},
  {"step": "Phase 1: Update system prompts", "status": "pending"},
  {"step": "Phase 2: Audit and clean templates", "status": "pending"},
  {"step": "Phase 3: Update skill version headers", "status": "pending"},
  {"step": "Phase 4: Update agent configs", "status": "pending"},
  {"step": "Phase 5: Update subagent prompts", "status": "pending"},
  {"step": "Phase 6: Dry-run deploy + git commit", "status": "pending"},
  {"step": "Phase 7: Upload Kaizen report to R2", "status": "pending"},
  {"step": "Phase 8: Verify hooks and scheduled tasks", "status": "pending"},
  {"step": "Phase 9: Restart DeepChat (mandatory — terminal boundary)", "status": "pending"},
])

### Autonomous Continuation Protocol (v1.3)

**Phases 0-8 execute autonomously without user intervention.** The agent MUST:

1. After ANY phase marked [EXECUTED] with tool evidence, immediately proceed to the next phase
2. Before advancing: tag `[AUTO-CONTINUE -> Phase N+1]` in the response
3. At completion of all phases 0-8: tag `[PHASES-0-8-COMPLETE]`
4. Phase 9 (restart) is the ONLY manual boundary — execute as terminal step
5. If a phase fails: tag `[BLOCKED: reason]`, skip to next phase, report in Kaizen report
6. If ALL phases 0-8 complete but restart cannot execute: tag `[HANDOFF: restart pending]` with details
7. Never wait for user confirmation between phases 0-8

**ANTI-PATTERN:** User should NEVER need to say "CONTINUE" between phases 0-8. The agent autonomously chains all phases.

---

## Purpose

Autonomous system-wide Kaizen continuous improvement protocol. Executes comprehensive audit of ALL DeepChat settings — prompts, templates, skills, agents, subagents — applies improvements, deploys changes, and commits with full audit trail.

## When to Use

| Trigger | Example |
|:--------|:--------|
| User issues Kaizen update command | "UPDATE ALL FROM KAIZEN", "UPDATE ALL DEEPCHAT SETTINGS FROM KAIZEN" |
| Kaizen engine finds 5+ unapplied improvements | Auto-triggered threshold |
| System consistency audit finds 3+ drift items | Proactive maintenance |
| After major architecture changes | Ensures all components stay synchronized |
## Protocol (7 Phases)

Execute the complete 7-phase execution protocol documented below (templates deprecated v2026-07-11 — all protocols inline):

| Phase | Description | Key Output |
|:------|:-----------|:-----------|
| **0. Pre-Flight** | Discovery Index pull, Kaizen audit, comprehensive Python audit, **GitHub↔D1 sync check** | Gap report + drift report |
| **1. System Prompts** | Update DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md | Version bumps |
| **2. Templates** | Audit staleness, merge duplicates, deprecate unused | Clean template set |
| **3. Skills** | Version headers, tool docs, read-based loading patterns | Versioned skills |
| **4. Agent Configs** | Tool lists, subagent slots, system prompt references | Updated configs |
| **5. Subagent Prompts** | Research Integrity, DoD criteria, anti-patterns | Updated subagents |
| **6. Deploy & Commit** | Dry-run, deploy skills + hooks, git commit with verification | Deployed + committed |
| **7. R2 Upload** | Kaizen report to R2, Discovery Index update, cleanup | Audit trail |
| **8. Hooks & Scheduled Tasks** | Verify hook scripts deployed, scheduled tasks registered | Hook health report |
| **9. Restart DeepChat** | **MANDATORY:** Kill all DeepChat processes + relaunch fresh instance | DeepChat restarted |

## Comprehensive Audit Script

The Phase 0 comprehensive audit (`_kaizen_system_audit.py`) checks:

1. **Version consistency** — every prompt, template, skill, agent has a version
2. **Required section presence** — Rules 1-6, 12-14, Research Integrity, Web Research Protocol, File Lifecycle, Publication Language Gate, Git Protocol, Cloudflare-Native, Discovery Index Step 0, Kaizen §9.5
3. **Cross-reference integrity** — QWAV→DEFAULT section refs, agent→system prompt refs
4. **Skill completeness** — version, tools, read-based loading, trigger conditions
5. **Template staleness** — every template must be referenced somewhere
6. **Guardrail completeness** — all essential guardrails present
7. **Kaizen engine health** — conversation search, R2 integration
8. **GAP AUDIT (v1.2 — per closeout-manager §2.6):** Run the full POST-PHASE GAP AUDIT (A-F categories) as part of Phase 0. Any BLOCKING gaps → halt the Kaizen update. Document all gaps in the Kaizen report.
9. **GITHUB↔D1 DRIFT CHECK (v1.1 — 2026-07-11):** When `GITHUB_TOKEN` is available, run the lightweight drift check from `github-cloudflare-sync` skill. If GitHub open/closed counts differ from D1 pending/closed counts → flag `[GH-CF-DRIFT: N issues out of sync]` and auto-remediate before proceeding to Phase 1.
10. **VARIANT DEDUPLICATION (v1.0 — DeepChat v1.0.9):** Skills adopted from external agents (Claude Code, Agents SDK) that conflicted with existing DeepChat skills were renamed with `-claude-code` or `-agents` suffixes. The canonical variant is the base-named skill (e.g., `cloudflare`, not `cloudflare-claude-code`). When updating skills, ONLY update the canonical (base-named) variant. Do NOT independently update `-claude-code` or `-agents` suffixed copies — these are imports of the canonical version and will be overwritten on next skill-sync. If a suffixed copy has diverged, flag it as `[VARIANT-DRIFT: <name>-claude-code diverged from <name>]` and report in the Kaizen report.

## Related Skills

| Skill | When to Use |
|:------|:-----------|
| `git-hygiene` | If git operations fail during update |
| `closeout-manager` | After update completes, for session close-out |
| `template-catalog` | To verify template entries after cleanup |
| `cloudflare-deployer` | If R2/wrangler operations fail |
| `publication-publisher` | If the update report needs formal publication |

## Phase 9: Mandatory Restart

After all Kaizen phases complete (0-8), DeepChat MUST be restarted. System prompts, templates, skills, agents, and subagents are all loaded at application startup; none of the Kaizen changes take full effect until DeepChat is killed and relaunched.

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.deepchat\skills\kaizen-autonomous-update\scripts\restart_deepchat.ps1"
```

This is the **final mandatory step** of any Kaizen update. Execute after Phase 8 completes and all verification passes.

## Safety Rules

1. **NEVER work on main branch** — always `feature/kaizen-autonomous-update`
2. **Read before write** — never edit a file from memory
3. **One component at a time** — update → verify → commit before next
4. **Never delete PERMANENT files** — only EPHEMERAL files
5. **Version ALL changes** — every edit = version bump + VERSION HISTORY
6. **Filesystem verify after every write** — `Test-Path` + `Get-Content -First 5`
7. **Git verify after every commit** — `git log -1 --oneline`
8. **Anti-Phantom Rule 14** — never claim an action without tool evidence
## 2.5.1 Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Tools execute as ephemeral `_<name>.py` files — pull from R2, execute, discard. Never persist locally.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:----------------------|:--------|
| `kaizen_engine.py` | `qnfo/tools/kaizen_engine.py` | `qnfo/tools/kaizen_engine.py` | `_kaizen_engine.py` (ephemeral) | Kaizen engine — audit, apply, deploy |
| `deploy.py` | `qnfo/tools/deploy.py` | `qnfo/tools/deploy.py` | `_deploy.py` (ephemeral) | Deploys changes to DeepChat runtime |
| `system_audit.py` | `qnfo/tools/system_audit.py` | `qnfo/tools/system_audit.py` | `_system_audit.py` (ephemeral) | Cross-file consistency audit |

### Execution Protocol (Ephemeral)
Tools execute locally (Python requires filesystem access) but do NOT persist:
1. **Pull:** `npx wrangler r2 object get qnfo/tools/<name>.py --remote --file=_<name>.py`
2. **Execute:** `python _<name>.py`
3. **Discard:** `Remove-Item _<name>.py`
4. If R2 copy missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`

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

> **Version:** v1.1 (Kaizen-audited 2026-07-11 — GitHub↔D1 sync added to Phase 0 pre-flight)
