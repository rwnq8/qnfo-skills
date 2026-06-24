---
name: kaizen-autonomous-update
description: Autonomous system-wide Kaizen improvement protocol — triggers when user says "UPDATE ALL FROM KAIZEN" or when Kaizen engine detects 5+ unapplied improvements. Updates all prompts, templates, skills, agents/subagents, deploys, and commits.
version: "1.1"
---

> **QNFO Custom Skill** — Load via `read('R2 `qnfo/prompts/skills/kaizen-autonomous-update\\SKILL.md')`
> **Template:** `fill_prompt_template("KAIZEN-AUTONOMOUS-UPDATE", {...})`

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
