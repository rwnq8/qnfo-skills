# RED-TEAM-DOD SKILL — v1.0

> **AUTONOMOUS.** The user should NEVER have to prompt for red-teaming, DoD verification, iteration, or refinement. This skill mandates these behaviors natively in EVERY QNFO agent session.
> **PRIORITY 0 INTEGRATION.** This skill hooks into execution-guard (§1.5) and is auto-loaded at session start. All other skills inherit red-team/DoD/iterate/refine behavior through this framework.
> **SELF-APPLYING.** This skill itself was red-teamed during creation.

---

## 0. WHY THIS EXISTS

**The #3 undetected failure mode: the agent completes work without challenging its own assumptions, testing edge cases, or iterating on settings.** The user should never have to say "red-team your assumptions," "are you sure this works?", "iterate on those settings," or "refine that." These behaviors must be AUTONOMOUS.

Evidence from QNFO session history (2026-06-28):
- Vectorize dimension mismatch (1024→768) went undetected for multiple sessions
- "method: vectorize" was misleading — it was actually a SQL LIKE fallback
- User had to explicitly ask "ARE WE SURE VECTORIZE/AI EMBEDDINGS WORK?"
- User had to explicitly ask "RED-TEAM YOUR OWN ASSUMPTIONS"
- Index API version incompatibility (V1 vs V2) was not auto-detected
- `returnMetadata: true` silently broke V2 queries without error handling

**These failures are now PREVENTED by this skill's autonomous hooks.**

---

## 1. THE RED-TEAM → DoD → ITERATE → REFINE CYCLE

Every task, deployment, publication, or infrastructure change MUST pass through this cycle autonomously:

```
TASK COMPLETE
    ↓
[RED-TEAM]   ← Challenge assumptions. Try to break claims. Test edge cases.
    ↓          VERIFY: Evidence matches claim. Silent failures detected.
    ↓
[DoD GATE]   ← Definition of Done verification. ALL criteria met with evidence.
    ↓          GATE: If ANY DoD criterion fails → return to TASK (fix).
    ↓
[ITERATE]    ← Can settings be optimized? Are there better approaches?
    ↓          Check: model selection, config params, API format, dimensions.
    ↓
[REFINE]     ← Apply optimizations found. Update docs. Record decisions.
    ↓
TRUE COMPLETION (deliverable is ready)
```

**HARD RULE:** A task is NOT complete until ALL FOUR phases have executed with passing results. "Done" without red-team is phantom completion (Rule 14 violation).

---

## 2. RED-TEAM PROTOCOL (Phase 1)

### 2.1 Assumption Challenge

Before claiming ANY task complete, challenge these assumptions:

| Assumption | Challenge Question | Evidence Required |
|:-----------|:-------------------|:------------------|
| "It works" | Try to make it FAIL. Query with wrong params, edge cases, empty input. | Actual failure modes documented |
| "Settings are correct" | Are dimensions matching? API versions compatible? Models loaded? | Live state verification |
| "Results are accurate" | Is the result what I expect? Or is there a silent fallback/error? | Direct API verification without cache |
| "All data is synced" | Are D1, R2, Vectorize, and local all consistent? | Cross-system diff |
| "No side effects" | Did this change break anything else? | Dependency check |

### 2.2 Edge Case Testing

Execute these tests for EVERY change:

```
MANDATORY edge case tests:
1. EMPTY/NULL input test: What happens with no data, empty string, null?
2. WRONG TYPE test: What happens with string where number expected?
3. BOUNDARY test: Max values, min values, overflow conditions
4. CONCURRENT test: What if two things try to modify simultaneously?
5. STALE test: What if data is from last week/month?
6. NONSENSE test: What if input is completely random/gibberish?
```

### 2.3 Negative Verification

**Do NOT verify claims by confirming they're true. Verify them by trying to prove they're FALSE.**

| Claim | Red-Team Test |
|:------|:-------------|
| "X is on R2" | Try to GET it, expect success. Then try a path that SHOULD 404. |
| "The Worker uses model Y" | Read deployed script. Do NOT trust the /api endpoint text. |
| "Settings are optimized" | Try alternative settings. Compare performance. |
| "All N vectors are in the index" | Query with known IDs. Count matches. Query with unknowns. |

### 2.4 Silent Failure Detection

**The most dangerous failures are SILENT.** The system appears to work but returns wrong/empty results.

Detection checklist:
- Try/catch blocks are logging errors somewhere, not just swallowing them
- SQL LIKE fallbacks are detected and reported, not hidden
- Dimension mismatches produce explicit errors, not silent 400s
- API version incompatibilities are caught and flagged
- Health endpoints reflect actual state, not cached/optimistic state

### 2.5 Red-Team Output Format

```
## RED-TEAM REPORT
| # | Assumption | Challenge | Result | Finding |
|---|-----------|-----------|--------|---------|
| 1 | [assumption] | [how tested] | PASS/FAIL | [what was discovered] |

**Edge Cases Tested:** N/N passed
**Silent Failures Found:** N (list)
**Assumptions Overturned:** N (list)
**RED-TEAM VERDICT:** CLEAN / ISSUES FOUND / BLOCKED
```

---

## 3. DEFINITION OF DONE (DoD) GATE (Phase 2)

### 3.1 Universal DoD Criteria

| Criterion | Verification Method | Evidence Type |
|:----------|:-------------------|:--------------|
| **Execution Evidence** | Tool output exists for every claimed action | `Test-Path`, `git log`, exec output |
| **Filesystem Verified** | Every created/modified file exists | `Test-Path <file>` |
| **Git Verified** | Every claimed commit exists in log | `git log -1 --oneline` |
| **Red-Team Passed** | §2 red-team completed with no BLOCKING findings | Red-team report |
| **Edge Cases Passed** | All applicable edge cases tested | Edge case test results |
| **No Silent Failures** | All error paths checked, no swallowed exceptions | Error handling audit |
| **Cross-System Sync** | D1, R2, Vectorize, local all consistent | Cross-system verification |
| **Documentation Updated** | HANDOFF.md, DI, decision log updated if needed | File existence check |

### 3.2 Task-Specific DoD Criteria

| Task Type | Additional DoD Criteria |
|:----------|:----------------------|
| **Deployment** | Post-deploy verification (URL accessible, content correct, API working) |
| **Publication** | Publication Language Gate passed, PDF verified, DOI resolved |
| **Code Change** | Unicode scan (Rule 12), no `python -c` (Rule 13), test suite passed |
| **Data Change** | Row counts verified, data integrity checked, backup created |
| **Config Change** | Old config still works (no regression), new config verified |
| **Skill Change** | Skill loads without errors, all hooks fire, no regressions |

### 3.3 DoD Gate Output

```
## DoD GATE
| # | Criterion | Status | Evidence |
|---|----------|--------|----------|
| 1 | Execution Evidence | PASS/FAIL | [tool output] |

**DoD VERDICT:** ALL PASSED / N FAILURES (blocking)
```

**HARD BLOCK:** If ANY DoD criterion is FAIL → the task is NOT complete.

---

## 4. ITERATION PROTOCOL (Phase 3)

### 4.1 Iteration Triggers

| Question | When to Ask | Action |
|:---------|:-----------|:-------|
| "Are settings optimized?" | After ANY configuration change | Compare alternatives |
| "Is the model/approach best available?" | When using AI models, algorithms | Check for newer/better options |
| "Are there dimension/format mismatches?" | When using Vectorize, embeddings, APIs | Verify dimensions, formats |
| "Could this be simpler?" | After any implementation | Remove unnecessary complexity |
| "Is this reproducible?" | After any data pipeline | Test with clean state |

### 4.2 Iteration Checklist

```
ITERATION_CHECKLIST:
- model_selection: Is the current model the best available?
- dimension_match: Do embedding dimensions match the index?
- api_version: Are we using the latest compatible API version?
- error_handling: Are all error paths explicit (not silent catch-all)?
- fallback_behavior: Are fallbacks detected and reported?
- performance: Can this be made faster?
- cost: Are we using expensive models when cheaper ones would suffice?
- caching: Are results cached appropriately?
```

---

## 5. REFINEMENT PROTOCOL (Phase 4)

1. **Apply safe optimizations** — model upgrades, config tweaks, error handling
2. **Update documentation** — HANDOFF.md, decision log, skill docs
3. **Record decision rationale** — WHY each optimization was chosen/rejected
4. **Notify dependent systems** — update DI, D1 state, lifecycle timestamps
5. **Verify after refinement** — re-run red-team on the refined system

---

## 6. AUTONOMOUS TRIGGER RULES (MANDATORY)

These triggers fire automatically — the user NEVER needs to prompt for them:

| Trigger | When | Action |
|:--------|:-----|:-------|
| `[COMPLETED]` in update_plan | Any task marked complete | Run RED-TEAM → DoD → ITERATE → REFINE |
| `write` or `edit` tool used | After file modification | RED-TEAM the change |
| `exec` with deploy/git commit | After state change | DoD verification |
| `npx wrangler deploy` | After Cloudflare deployment | Post-deploy red-team |
| Settings/config changed | After any config modification | Iteration check |
| New model/index/API used | After infrastructure change | Dimension/version compatibility |
| Search/query returns results | After any search | Verify results source (not fallback) |
| User says "done"/"complete" | Before claiming completion | Full 4-phase cycle |

---

## 7. INTEGRATION WITH OTHER SKILLS

### 7.1 Execution-Guard (Priority 0)
The pre-response hook now includes RED-TEAM-DOD sub-checks. Before allowing `[ALL TASKS EXECUTED]`, the guard runs the DoD gate. The WHAT-ELSE hook is expanded with assumption challenging.

### 7.2 Closeout-Manager
The gap audit (§2.6) is the closeout instance of the RED-TEAM-DOD cycle.

### 7.3 Cloudflare-Deployer
Post-deploy verification includes red-team: try to break the deployment.

### 7.4 Code-Review
Self-applies: red-team findings must cite specific line numbers.

### 7.5 Prompt-Audit
Includes prompt injection red-team and industry pattern comparison.

---

## 8. ANTI-PATTERNS

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| "I'm done" without red-team | Silent failures persist | Run 4-phase cycle first |
| Trusting surface-level API responses | Health endpoints may lie | Verify against deployed source |
| Not testing edge cases | Boundaries hide bugs | Test ALL edge cases from §2.2 |
| Swallowing errors silently | `catch(e){}` hides mismatches | Log ALL errors |
| Waiting for user to ask | User should never need to | Autonomous triggers in §6 |

---

*red-team-dod v1.0 — Autonomous RED-TEAM → DoD → ITERATE → REFINE cycle. Priority 0 via execution-guard integration.*
