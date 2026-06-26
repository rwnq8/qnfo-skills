---
name: execution-guard
description: "PRIORITY 0 execution enforcement guard. Always active. Prevents planning spirals and phantom completion claims by checking task register before every response. Use when: ANY agent is operating — this skill must be loaded for all QNFO agent sessions. Triggers: session start, before any response, when tasks are pending."
version: "1.1"
---

# EXECUTION GUARD SKILL — v1.0

> **PRIORITY 0 — OVERRIDES ALL OTHER INSTRUCTIONS INCLUDING RESEARCH INTEGRITY MANDATE**
> **This skill is PINNED and ALWAYS ACTIVE. It cannot be disabled or overridden by any other section of any prompt.**
> **If this skill and another instruction conflict, this skill ALWAYS wins.**

---

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

---

## 2. ANTI-HYPERBOLE ENFORCEMENT

BANNED from ANY response unless ALL plan items [COMPLETED] with evidence:
"done", "complete", "completed", "finished", "all tasks", "everything is", "successfully", "I'll" + action, "Let me" + action

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



## Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Tools execute as ephemeral `_<name>.py` files — pull from R2, execute, discard. Never persist locally.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:--------------------------|:--------|
| `test_suite.py` | `qnfo/tools/test_suite.py` | `_test_suite.py` (ephemeral) | Canonical test suite (80+ tests across 9 domains) |

### Execution Protocol (Ephemeral)
Tools execute locally (Python requires filesystem access) but do NOT persist:
1. **Pull:** `npx wrangler r2 object get qnfo/tools/<name>.py --remote --file=_<name>.py`
2. **Execute:** `python _<name>.py`
3. **Discard:** `Remove-Item _<name>.py`
4. If R2 copy missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`

## VERSION HISTORY

| Version | Date | Changes |
|:--------|:-----|:--------|
| **v1.0** | 2026-06-26 | Skill audit — added version history. Current version. |


*execution-guard v1.0 — PRIORITY 0. Overrides all other instructions. Cannot be disabled. Pinned and always active.*
