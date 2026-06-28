---

## 0. WHY THIS EXISTS

QNFO/QWAV production sites were stub content. No test suite existed. This skill mandates testing for every action.

## 1. TEST GATES

| Action | Required Test | Severity |
|:---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.
----|:-------------|:---------|
| Pages deploy | `_test_suite.py --pages` — no stubs, all load | BLOCKING |
| Worker deploy | `_test_suite.py --cms` — all endpoints OK | BLOCKING |
| D1 schema change | `_test_suite.py --d1` — tables accessible | BLOCKING |
| Content change | Content quality: bodies non-empty, DOIs present | BLOCKING |
| Skills edit | `bootstrap_skills.py --verify && _deploy.py --verify` | BLOCKING |
| ANY Cloudflare deploy | `_test_suite.py` full run within 30s | BLOCKING |
| Session closeout | `_test_suite.py` full run + gap audit (closeout-manager §2.6) | MANDATORY |

## 2. CONTENT QUALITY GATE

| Check | Blocking? |
|:------|:--------:|
| Page NOT stub (no "stub", "page stub", "auto-generated") | **YES** |
| Page has `<title>`, `<h1>`, body > 500B | **YES** |
| CMS publication has body (> 100 chars) | **YES** |
| CMS publication has DOI | WARNING |

## 2.5 GAP AUDIT BRIDGE (v1.1)

Test failures discovered by this skill automatically feed into the POST-PHASE GAP AUDIT (closeout-manager §2.6):
- Critical test failures → BLOCKING gaps (prevent completion claims)
- Warning-level failures → HIGH gaps (should fix this session)
- Missing tests → MEDIUM gap (document for next session)

**If test suite has ANY critical failure → the gap audit MUST show BLOCKING severity.**

## 3. CANONICAL TEST SUITE

**R2:** `qnfo/tools/test_suite.py` | **Local:** `_test_suite.py` (ephemeral)

```bash
# Pull: npx wrangler r2 object get qnfo/tools/test_suite.py --remote --file=_test_suite.py
python _test_suite.py                    # All 80+ tests
python _test_suite.py --cms --pages     # Deploy verification
python _test_suite.py --quick           # Smoke test
# Discard: Remove-Item _test_suite.py
```

## 4. DOMAINS COVERED (80+ tests across 9 domains)

CMS (8) | Pages (55) | KG (6) | D1 (8) | Vectorize (3) | R2 (4) | Skills (8) | Content (8+) | Health (3)

## 5. FAILURE HANDLING

- Critical failure → BLOCK deployment, fix before proceeding
- Warning → LOG to audit trail, proceed
- Network timeout → Retry ×2 (5s delay)
- 3× same failure → Flag `[STUCK]`, escalate

## 6. INTEGRATION

- **execution-guard:** DoD adds "Test verified: N/N pass"
- **cloudflare-deployer:** Post-deploy test required
- **closeout-manager:** Full test suite run → gap audit integration (§2.6)
- **qnfo-agent:** §9.11.3 DoD adds test verification criterion

## 7. VERSION HISTORY

| v1.1 | 2026-06-27 | Gap audit bridge (§2.5) — test failures auto-populate closeout-manager gap audit.
| v1.0 | 2026-06-26 | Initial release. 80+ tests, mandatory gates, content quality enforcement. |

---

*test-enforcement v1.1 — PRIORITY 1. Gap-audit bridge (§2.5). Pinned. Mandatory for ALL actions.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

