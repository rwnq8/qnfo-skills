---
name: execution-guard
description: "PRIORITY 0 execution enforcement guard. Always active. Prevents planning spirals and phantom completion claims by checking task register before every response. Use when: ANY agent is operating — this skill must be loaded for all QNFO agent sessions. Triggers: session start, before any response, when tasks are pending."
version: "1.1"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


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

*execution-guard v1.2 — PRIORITY 0. Auto-gap detection via WHAT-ELSE hook (§1.4). Red-team self-testing. Cannot be disabled. Pinned and always active.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

