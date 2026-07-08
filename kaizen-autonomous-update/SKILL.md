---
name: kaizen-autonomous-update
description: Autonomous system-wide Kaizen continuous improvement protocol. Updates all prompts, templates, skills, agents/subagents, deploys, and commits. Use when user says "UPDATE ALL FROM KAIZEN," "system update," "update all skills," "continuous improvement," "Kaizen update," "auto-update," "upgrade everything," "refresh all settings," or when Kaizen engine detects 5+ unapplied improvements.
version: "1.2"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** closeout-manager, skill-sync


> **QNFO Custom Skill** — Load via `read('R2 `qnfo/prompts/skills/kaizen-autonomous-update\\SKILL.md')`
> **Template:** `fill_prompt_template("KAIZEN-AUTONOMOUS-UPDATE", {...})`

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
  {"step": "Phase 9: Restart DeepChat (mandatory)", "status": "pending"},
])

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

Fill the `KAIZEN-AUTONOMOUS-UPDATE` template using `fill_prompt_template`. The template contains the complete 7-phase execution protocol:

| Phase | Description | Key Output |
|:------|:-----------|:-----------|
| **0. Pre-Flight** | Discovery Index pull, Kaizen audit, comprehensive Python audit | Gap report |
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

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

