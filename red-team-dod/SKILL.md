---
name: red-team-dod
description: AUTONOMOUS red-team + Definition of Done enforcement protocol. Runs output verification, assumption challenges, edge case checks, DoD integration, and iteration for EVERY agent response. The user should NEVER prompt for quality checks.
version: "1.3"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** execution-guard, closeout-manager
### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('red-team-dod')` or `read()` with filesystem path.
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

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan (WBS Naming Convention — per execution-guard §1.4.1)

update_plan([
  {"step": "[P1-T1] Verify all claims with negative verification", "status": "pending"},
  {"step": "[P1-T2] Challenge every assumption with counter-evidence", "status": "pending"},
  {"step": "[P1-T3] Test all applicable edge cases (empty/null/max/boundary)", "status": "pending"},
  {"step": "[P2-T1] Run DoD gate — all criteria met with tool evidence", "status": "pending"},
  {"step": "[P3-T1] Iterate: check for optimization opportunities", "status": "pending"},
  {"step": "[P4-T1] Refine: apply improvements, update documentation", "status": "pending"}
])


# RED-TEAM-DOD SKILL — v1.3

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
- returnMetadata silently broke V2 queries without error handling

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

## 2. RED-TEAM PROTOCOL (Phase 1 — Execute After EVERY Task)

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

1. EMPTY/NULL input test: What happens with no data, empty string, null?
2. WRONG TYPE test: What happens with string where number expected?
3. BOUNDARY test: Max values, min values, overflow conditions
4. CONCURRENT test: What if two things try to modify simultaneously?
5. STALE test: What if data is from last week/month?
6. NONSENSE test: What if input is completely random/gibberish?
7. **DNS CROSS-REFERENCE test (v1.1):** For every CNAME→`.pages.dev`, is the domain registered on the target Pages project? Does any CNAME chain to a `.pages.dev` through another domain? Does any CNAME point to a non-existent Worker? (See infrastructure-audit §0.8-§0.10)

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

---

## 3. DEFINITION OF DONE (DoD) GATE (Phase 2 — After Red-Team)

### 3.1 Universal DoD Criteria

| Criterion | Verification Method | Evidence Type |
|:----------|:-------------------|:--------------|
| **Execution Evidence** | Tool output exists for every claimed action | Test-Path, git log, exec output |
| **Filesystem Verified** | Every created/modified file exists | Test-Path file |
| **Git Verified** | Every claimed commit exists in log | git log -1 --oneline |
| **Red-Team Passed** | Phase 1 red-team completed with no BLOCKING findings | Red-team report |
| **Edge Cases Passed** | All applicable edge cases tested | Edge case test results |
| **No Silent Failures** | All error paths checked, no swallowed exceptions | Error handling audit |
| **Cross-System Sync** | D1, R2, Vectorize, local all consistent | Cross-system verification |
| **Documentation Updated** | HANDOFF.md, DI, decision log updated if needed | File existence check |

### 3.2 Task-Specific DoD Criteria

| Task Type | Additional DoD Criteria |
|:----------|:----------------------|
| **Deployment** | Post-deploy verification (URL accessible, content correct, API working). **For DNS/domain changes: run infrastructure-audit §0.8 cross-reference — all CNAME→`.pages.dev` must have matching domain registrations, 0 522-RISK.** |
| **Publication** | Publication Language Gate passed, PDF verified, DOI resolved |
| **Code Change** | Unicode scan (Rule 12), no python -c (Rule 13), test suite passed |
| **Data Change** | Row counts verified, data integrity checked, backup created |
| **Config Change** | Old config still works (no regression), new config verified |
| **Skill Change** | Skill loads without errors, all hooks fire, no regressions |
| **Infrastructure Audit** | All §0.8-§0.11 gates pass: 0 522-RISK, 0 CNAME chains, 0 DEAD-WORKER, 0 EMPTY-ZONE. 30 domains resolve HTTP 200. Resource counts within baselines. |

---

## 4. ITERATION PROTOCOL (Phase 3 — After DoD)

### 4.1 Iteration Triggers

| Question | When to Ask | Action |
|:---------|:-----------|:-------|
| "Are settings optimized?" | After ANY configuration change | Compare alternatives |
| "Is the model/approach best available?" | When using AI models, algorithms | Check for newer/better options |
| "Are there dimension/format mismatches?" | When using Vectorize, embeddings, APIs | Verify dimensions, formats |
| "Could this be simpler?" | After any implementation | Remove unnecessary complexity |
| "Is this reproducible?" | After any data pipeline | Test with clean state |

### 4.2 Iteration Checklist

- model_selection: Is the current model the best available?
- dimension_match: Do embedding dimensions match the index?
- api_version: Are we using the latest compatible API version?
- error_handling: Are all error paths explicit (not silent catch-all)?
- fallback_behavior: Are fallbacks detected and reported?
- performance: Can this be made faster?
- cost: Are we using expensive models when cheaper ones would suffice?
- caching: Are results cached appropriately?

---

## 5. REFINEMENT PROTOCOL (Phase 4 — After Iteration)

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
| [COMPLETED] in update_plan | Any task marked complete | Run RED-TEAM to DoD to ITERATE to REFINE |
| write or edit tool used | After file modification | RED-TEAM the change |
| exec with deploy/git commit | After state change | DoD verification |
| npx wrangler deploy | After Cloudflare deployment | Post-deploy red-team |
| Settings/config changed | After any config modification | Iteration check |
| New model/index/API used | After infrastructure change | Dimension/version compatibility |
| Search/query returns results | After any search | Verify results source (not fallback) |
| User says "done"/"complete" | Before claiming completion | Full 4-phase cycle |

---

## 7. INTEGRATION WITH OTHER SKILLS

### 7.1 Execution-Guard (Priority 0)
The pre-response hook now includes RED-TEAM-DOD sub-checks (Section 1.5). Before allowing [ALL TASKS EXECUTED], the guard runs the DoD gate.

### 7.2 Closeout-Manager
The gap audit (Section 2.6) is the closeout instance of the RED-TEAM-DOD cycle.

### 7.3 Cloudflare-Deployer
Post-deploy verification includes red-team: try to break the deployment. **Specifically: verify all CNAME→`.pages.dev` domains have matching Pages project registrations (522 prevention).** See infrastructure-audit §0.8.

### 7.4 Code-Review
Self-applies: red-team findings must cite specific line numbers.

### 7.5 Prompt-Audit (demoted to skill-creator/references/)
Includes prompt injection red-team and autonomous trigger on any prompt modification. See `skill-creator/references/prompt-audit-checklist.md`.

---

## 8. ANTI-PATTERNS (DO NOT DO)

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| "I'm done" without red-team | Silent failures persist | Run 4-phase cycle first |
| Trusting surface-level API responses | Health endpoints may report wrong data | Verify against deployed source |
| Not testing edge cases | Boundaries hide bugs | Test ALL edge cases from Section 2.2 |
| Swallowing errors silently | catch(e){} hides mismatches | Log ALL errors |
| Waiting for user to ask | User should never need to | Autonomous triggers in Section 6 |

---

## 9. PHASE-AWARE ITERATION — CROSS-PHASE CONTINUATION (v1.3)

**The #7 undetected failure mode: completing RED-TEAM→DoD→ITERATE→REFINE on one phase's tasks and stopping — without checking whether the PROJECT has more phases.** This section adds the cross-phase continuation check that integrates with execution-guard's Phase-Aware Auto-Expansion Protocol (§1.4).

### 9.1 Phase Completion Signal

After the 4-phase cycle (RED-TEAM→DoD→ITERATE→REFINE) completes for the current project phase:

1. **Check `_wbs_state.json`** (see execution-guard §1.5): does `current_phase < total_phases`?
2. **If YES** → The project has more phases. DO NOT generate completion text.
3. **Auto-populate Phase N+1** tasks into `update_plan` using `[P(N+1)-T1]`, `[P(N+1)-T2]`, ... naming convention.
4. **Execute Phase N+1 immediately** — invoke a tool. Do NOT wait for user prompt.
5. **If NO (all phases complete)** → Proceed to session closeout (closeout-manager skill).

### 9.2 Phase Boundary Red-Team

Between every phase transition, run an autonomous phase-boundary check:

```
[PHASE-BOUNDARY RED-TEAM: Phase N → Phase N+1]
1. OUTPUT VERIFICATION: Did Phase N produce ALL expected artifacts?
2. ASSUMPTION CHALLENGE: Are dependencies for Phase N+1 satisfied?
3. EDGE CASES: Are there partial/incomplete outputs from Phase N that Phase N+1 depends on?
4. DoD INTEGRATION: Do ALL Phase N tasks pass their DoD gates?
5. ITERATION: Could Phase N have been executed better? What did we learn?

[GATE: PASS → auto-transition to Phase N+1, update D1 wbs_state (or _wbs_state.json fallback)]
[GATE: FAIL → fix Phase N gaps before transitioning. Document gap in handoff if unfixable.]
```

### 9.3 Autonomous Trigger: Phase Completion

Add this trigger to the §6 Autonomous Trigger Rules table:

| Trigger | When | Action |
|:--------|:-----|:-------|
| **ALL [PX-*] items completed** | Current phase fully done | Run §9.2 Phase Boundary Red-Team, then auto-expand Phase N+1 |

### 9.4 Anti-Phase-Stall Detection

If the agent has completed all tasks in the current phase AND has generated response text but has NOT auto-expanded to the next phase:

1. **Detection pattern:** `update_plan` shows all `[PX-*]` items `completed`, but response is text-only AND D1 `wbs_state` (or `_wbs_state.json` fallback) shows `current_phase < total_phases`
2. **Action:** This is a PHASE STALL — equivalent to a planning spiral. Force execution: auto-populate Phase N+1 NOW.
3. **Log:** `[PHASE-STALL-DETECTED: Phase N complete, Phase N+1 pending. Auto-expanding.]`

### 9.5 Integration with Execution-Guard

This section IS the red-team-dod implementation of execution-guard §1.5 (Phase-Aware Auto-Expansion Protocol). When execution-guard detects a phase completion and queries D1 `wbs_state` (or `_wbs_state.json` fallback), red-team-dod's Phase Boundary Red-Team (§9.2) fires before the auto-expansion. This ensures every phase transition is quality-gated.

---

*v1.0 deprecated 2026-07-01. Replaced by v1.1 with DNS cross-reference edge case and Infrastructure Audit DoD criteria.*

*red-team-dod v1.3 — Autonomous RED-TEAM to DoD to ITERATE to REFINE cycle plus Phase-Aware Iteration (§9). Priority 0 via execution-guard integration. v1.2 added Phase-Aware Iteration with cross-phase continuation, phase boundary red-team, and anti-phase-stall detection. v1.1 added DNS cross-reference edge case + Infrastructure Audit DoD criteria.*

> **Version:** (Kaizen-audited 2026-07-11)

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
