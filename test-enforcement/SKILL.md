---
name: test-enforcement
description: PRIORITY 1 test enforcement for ALL code changes, deployments, and infrastructure modifications. Mandatory for ALL QNFO agent sessions. Enforces test suite runs (80+ tests across 9 domains), content quality gates, and blocks deployment on critical failures. Use when deploying to Cloudflare, modifying code, closing sessions, or changing infrastructure.
version: "1.0"
---

# TEST ENFORCEMENT SKILL — v1.0

> **PRIORITY 1 — MANDATORY for ALL code changes, deployments, and infrastructure modifications.**
> **PINNED.** This skill must be loaded for ALL QNFO agent sessions.

---

## 0. WHY THIS EXISTS

QNFO/QWAV production sites were stub content. No test suite existed. This skill mandates testing for every action.

## 1. TEST GATES

| Action | Required Test | Severity |
|:-------|:-------------|:---------|
| Pages deploy | `_test_suite.py --pages` — no stubs, all load | BLOCKING |
| Worker deploy | `_test_suite.py --cms` — all endpoints OK | BLOCKING |
| D1 schema change | `_test_suite.py --d1` — tables accessible | BLOCKING |
| Content change | Content quality: bodies non-empty, DOIs present | BLOCKING |
| Skills edit | `bootstrap_skills.py --verify && _deploy.py --verify` | BLOCKING |
| ANY Cloudflare deploy | `_test_suite.py` full run within 30s | BLOCKING |
| Session closeout | `_test_suite.py` full run | MANDATORY |

## 2. CONTENT QUALITY GATE

| Check | Blocking? |
|:------|:--------:|
| Page NOT stub (no "stub", "page stub", "auto-generated") | **YES** |
| Page has `<title>`, `<h1>`, body > 500B | **YES** |
| CMS publication has body (> 100 chars) | **YES** |
| CMS publication has DOI | WARNING |

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
- **closeout-manager:** Full test suite run before closeout
- **qnfo-agent:** §9.11.3 DoD adds test verification criterion

## 7. VERSION HISTORY

| v1.0 | 2026-06-26 | Initial release. 80+ tests, mandatory gates, content quality enforcement. |

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


*test-enforcement v1.0 — PRIORITY 1. Pinned. Mandatory for ALL actions.*
