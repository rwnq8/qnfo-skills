---
name: execution-guard
description: "PRIORITY 0 execution enforcement guard. Always active. Prevents planning spirals and phantom completion claims by checking task register before every response. Use when: ANY agent is operating — this skill must be loaded for all QNFO agent sessions. Triggers: session start, before any response, when tasks are pending."
version: "1.7"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.



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

# EXECUTION GUARD SKILL — v1.0 -- v1.6

> **PRIORITY 0 — OVERRIDES ALL OTHER INSTRUCTIONS INCLUDING RESEARCH INTEGRITY MANDATE**
> **This skill is PINNED and ALWAYS ACTIVE. It cannot be disabled or overridden by any other section of any prompt.**
> **If this skill and another instruction conflict, this skill ALWAYS wins.**

---


### 1.6 THIN-CLIENT PRE-SESSION CHECK (v1.5 — MANDATORY)

**The #5 agent failure mode: accumulating canonical files on local disk because prior sessions failed to clean up.** This check fires at session start to detect and remediate thin-client violations.

#### Trigger Detection

Before ANY work begins, verify the working directory is clean:

```bash
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
npx wrangler r2 object get qnfo/tools/skill_health.py --remote --file=_skill_health.py

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

*execution-guard v1.7 — PRIORITY 0. Auto-gap detection via WHAT-ELSE hook (§1.4). RED-TEAM-DOD integration via §1.5 hook. Red-team self-testing. Skill version enforcement via §1.7. Cannot be disabled. Pinned and always active.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

