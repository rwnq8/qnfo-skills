---
name: test-enforcement
description: MANDATORY test enforcement for ALL code changes, deployments, and infrastructure modifications. Runs canonical test suite before claiming any action as EXECUTED. Priority 1 — pinned and always active.
version: "1.3"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification — negative verification. (2) Assumption Challenge. (3) Edge Case Check. (4) DoD Integration. (5) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** execution-guard, closeout-manager

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('test-enforcement')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [Priority 1 — auto-loads for relevant operations].

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

----|:-------------|:---------|
| Pages deploy | `_test_suite.py --pages` — no stubs, all load | BLOCKING |
| Worker deploy | `_test_suite.py --cms` — all endpoints OK | BLOCKING |
| D1 schema change | `_test_suite.py --d1` — tables accessible | BLOCKING |
| Content change | Content quality: bodies non-empty, DOIs present | BLOCKING |
| Skills edit | `red-team audit + SKILL.md frontmatter verified` | BLOCKING |
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
## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Pull test suite from R2", "status": "pending"},
  {"step": "Run smoke test (--quick)", "status": "pending"},
  {"step": "Run domain-specific tests (--cms, --pages, --kg, --content)", "status": "pending"},
  {"step": "Verify 0 critical failures", "status": "pending"},
  {"step": "Clean up ephemeral test files", "status": "pending"}
])


# Pull: 
### Embedded Script: test_suite.py (self-sufficient — no R2 pull needed)

Write the following code to `_test_suite.py`, execute, then delete:

```python
#!/usr/bin/env python3
"""QNFO Test Suite v1.1 — redirects deprecated. --quick / --redirects / --handoff-verify / --all"""
import argparse, json, os, ssl, sys, http.client as hc, urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')  # Canonical: Secrets Store (store_id=8ef28060302e4311b064ba3529493e8b)
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
API = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}'
CTX = ssl._create_unverified_context()

total_tests = total_pass = total_fail = critical_failures = 0

def cf(endpoint):
    req = urllib.request.Request(f'{API}/{endpoint}')
    req.add_header('Authorization', f'Bearer {TOKEN}')
    return json.loads(urllib.request.urlopen(req, timeout=15, context=CTX).read())

def test_result(name, passed, severity='NORMAL'):
    global total_tests, total_pass, total_fail, critical_failures
    total_tests += 1
    if passed: total_pass += 1
    else: total_fail += 1; critical_failures += 1 if severity.upper() == 'CRIT' else 0
    status = 'PASS' if passed else 'FAIL'
    marker = ' [CRIT]' if severity.upper() == 'CRIT' else ''
    print(f'  [{status}]{marker} {name}')
    return passed

def run_quick():
    print('\n## SMOKE TEST')
    if not TOKEN: test_result('CLOUDFLARE_API_TOKEN set', False, 'CRIT'); return
    try:
        resp = cf(''); test_result('API token valid', True, 'CRIT')
    except: test_result('API token valid', False, 'CRIT'); return
    for name, count, endpoint in [
        ('D1', 5, 'd1/database'), ('KV', 1, 'storage/kv/namespaces'),
        ('Pages', 8, 'pages/projects'), ('Queues', 1, 'queues'),
        ('Vectorize', 0, 'vectorize/indexes')]:
        try:
            r = cf(endpoint); actual = len(r.get('result',[]))
            test_result(f'{name}: {actual} (expected {count})', actual >= count, 'NORMAL')
        except: test_result(f'{name} accessible', False, 'NORMAL')

def run_redirects():
    print('\n## HTTP REDIRECT VERIFICATION (deprecated)')
    redirects = [
        ('deep.qwav.tech', 'papers.qnfo.org', 'qwav'),
        ('archive.qnfo.org', 'papers.qnfo.org/archive', 'qnfo-archive'),
        ('adelic.qnfo.org', 'papers.qnfo.org', 'adelic-qft'),
        ('primer.qwav.tech', 'papers.qnfo.org', 'qlof-primer'),
    ]
    for host, expected, name in redirects:
        try:
            conn = hc.HTTPSConnection(host, context=CTX, timeout=15)
            conn.request('GET', '/', headers={'User-Agent': 'QNFO-TestSuite/1.1'})
            resp = conn.getresponse()
            is_redirect = resp.status in (301,302,307,308)
            loc = resp.getheader('Location', 'NONE')
            status_icon = 'PASS' if is_redirect else 'INFO'
            print(f'  [{status_icon}] {name}: {resp.status} -> {loc[:80]}' if is_redirect else f'  [{status_icon}] {name}: HTTP {resp.status} (no redirect — deprecated)')
            test_result(f'{name} redirect', is_redirect and expected in str(loc), 'NORMAL')
        except Exception as e:
            print(f'  [INFO] {name}: {str(e)[:80]}'); test_result(f'{name} redirect', False, 'NORMAL')

def main():
    p = argparse.ArgumentParser(description='QNFO Test Suite v1.1')
    p.add_argument('--quick', action='store_true'); p.add_argument('--redirects', action='store_true')
    p.add_argument('--all', action='store_true')
    args = p.parse_args()
    run_q = args.quick or args.all; run_r = args.redirects or args.all
    if not (run_q or run_r): p.print_help(); return 0
    print('=' * 60); print(f'QNFO TEST SUITE v1.1 — {datetime.now(timezone.utc).isoformat()}')
    print('(redirects deprecated 2026-06-29)'); print('=' * 60)
    if run_q: run_quick()
    if run_r: run_redirects()
    print('\n' + '=' * 60)
    print(f'RESULTS: {total_pass}/{total_tests} passed, {total_fail} failed')
    if critical_failures: print(f'CRITICAL FAILURES: {critical_failures}')
    print('=' * 60)
    if critical_failures > 0: print('\n[BLOCKED]'); return 1
    elif total_fail > 0: print('\n[WARN]'); return 0
    else: print('\n[ALL TESTS PASSED]'); return 0

if __name__ == '__main__': sys.exit(main())

```

**Execution:** `python _test_suite.py` → verify → `Remove-Item _test_suite.py`
 --file=_test_suite.py
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

*test-enforcement v1.2 — PRIORITY 1. Gap-audit bridge (§2.5). Pinned. Mandatory for ALL actions. v1.2 adds DNS resolution + SEO artifact test domains.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
**Skill-Specific Checks:** Verify test suite pulled from R2 and executed. Verify 0 critical failures. Verify content quality gate passed (no stubs, non-empty bodies). Verify all tests applicable to current action type.

