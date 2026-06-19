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

*execution-guard v1.0 — PRIORITY 0. Overrides all other instructions. Cannot be disabled. Pinned and always active.*
