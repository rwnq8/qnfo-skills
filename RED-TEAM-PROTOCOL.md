# RED-TEAM-PROTOCOL.md -- Autonomous Self-Audit for All QNFO Skills

> **Version:** 1.0 | **Applies to:** ALL QNFO skills | **Enforcement:** verify_skills.ps1

---

## CORE PRINCIPLE

**The user should NEVER have to ask for red-teaming, gap detection, quality verification, or what-else/what-remains.** Every skill autonomously audits its own outputs, challenges its own assumptions, and catches phantom claims BEFORE the user sees them.

---

## 1. AUTONOMOUS TRIGGER DETECTION

When a skill completes its primary workflow, it MUST self-trigger the RED-TEAM AUDIT without user prompting.

| Condition | Action |
|:----------|:-------|
| Any task/output claimed COMPLETED | Run red-team audit BEFORE claiming done |
| Skill produces a deliverable (code, deploy, doc, design) | Run output verification |
| User questions quality/accuracy | Run FULL red-team audit -- this is a RED FLAG the skill failed to self-audit |
| Skill detects inconsistency in its own outputs | Escalate to execution-guard and re-execute |

---

## 2. RED-TEAM SELF-TESTING (MANDATORY -- All Skills)

Before claiming any deliverable complete, actively try to BREAK your own work:

### 2.1 Output Verification

| Check | Method | Gate |
|:------|:-------|:-----|
| Negative verification | Claim X exists -> try to GET/MISS it | Must confirm claim |
| Path inversion | Fixed path from A to B -> search for remaining references to A | Zero remaining A references |
| Empty return test | Deployed all files -> count deployed vs local file count | Must match |
| Commit hash verification | Pushed commit HASH -> git log must show HASH in origin | Must be present |
| Token/service health | Service X is working -> run actual query, not just /health | Must return expected data |

### 2.2 Assumption Challenge

For EVERY assumption made during skill execution:
1. State the assumption explicitly
2. Test it -- what would prove it false?
3. Report finding: CONFIRMED or FALSIFIED

### 2.3 Edge Case Enumeration

For EVERY deliverable, enumerate and test:
- Empty/null/missing input
- Maximum input (very large, very long)
- Boundary conditions (exactly at limit)
- Cross-system inconsistency (desync between local/remote)
- Time-dependent behavior (cache, stale data)

---

## 3. DOD INTEGRATION (Autonomous)

Every skill that produces code/config/deployment MUST:
1. Run DoD enforcement if _dod_enforce.py exists: python _dod_enforce.py
2. Check exit code: 0 = proceed, 1 = BLOCKED (fix before claiming done)
3. Log evidence: write to _dod_evidence.json
4. Verify criteria: at minimum check DOD-FE (frontend), DOD-DATA (data), DOD-API (APIs)

---

## 4. ITERATION & REFINEMENT (Autonomous)

When a skill output is suboptimal:

| Issue | Autonomous Response |
|:------|:-------------------|
| Output fails validation | Retry with adjusted parameters (max 3 iterations) |
| Output passes but is poor quality | Flag as WARN, document gap, offer improvement |
| User corrects output | Log correction, update internal model, re-execute with fix |
| Output is stale/outdated | Re-pull data, re-execute, compare timestamps |

---

## 5. GAP SEVERITY CLASSIFICATION

| Severity | Definition | Action |
|:---------|:-----------|:-------|
| BLOCKING | Prevents claiming work is complete | Fix NOW, do not proceed |
| HIGH | Functional gap -- works but fragile | Fix this session if possible |
| MEDIUM | Nice-to-have -- documentation, cleanup | Document for next session |
| LOW | Cosmetic -- warnings, formatting | Note in audit trail |

---

## 6. SKILL-SPECIFIC RED-TEAM EXTENSIONS

Each skill adds its own red-team checks in a ## RT: RED-TEAM SELF-AUDIT section:

- cloudflare-deployer: Verify Pages preview URL works, R2 sync complete, CDN purge applied
- frontend-design: Verify no banned fonts, WCAG contrast, uniqueness check, tone consistency
- bling-usability-audit: Verify screenshots captured, all viewports tested, console errors checked
- publication-publisher: Verify MathJax config, PDF build success, SEO metadata
- qnfo-agent: Verify all referenced skills exist on disk, token valid, system health
- closeout-manager: POST-PHASE GAP AUDIT (already implemented v3.1)
- execution-guard: Self-diagnostic and post-hoc audit (already implemented v1.2)

---

## 7. GAP REPORT FORMAT

Every skill that claims completion MUST output:

| Category | Check | Status | Detail |
|:---------|:------|:------:|:-------|
| Output | Negative verification | PASS/FAIL | |
| Output | Path inversion | PASS/FAIL | |
| Assumptions | Challenged | PASS/FAIL | N assumptions |
| Edge Cases | Enumerated | PASS/FAIL | N cases |
| DoD | If applicable | PASS/FAIL | |
| Iteration | Retry count | N | |

Gap Severity: NONE / LOW / MEDIUM / HIGH / BLOCKING
Autonomous Fix Applied: YES / NO

---

*RED-TEAM-PROTOCOL.md v1.0 -- Referenced by ALL QNFO skills. Updated via skill-sync.*
