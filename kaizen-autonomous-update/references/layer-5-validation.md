# Layer 5: Validation — Closed-Loop Improvement Architecture

> **Phase 2.1 Deliverable.** Documents the implementation path for the validation layer — the missing feedback loop between applying an improvement and measuring whether it worked.

---

## Current State: Layer 5 is Empty

Improvements are applied (Layers 1-4) but NEVER validated. The system cannot answer:
- "Did reducing temperature from 0.6 to 0.3 reduce phantom claims?"
- "Did adding deep-research cross-links increase research pipeline throughput?"
- "Did fixing js-yaml warnings prevent any actual loading failures?"

## Architecture: Before/After Metric Comparison

```
APPLY IMPROVEMENT → RECORD BEFORE METRIC → WAIT N SESSIONS → RECORD AFTER METRIC → COMPARE
                                                                                      │
                                                    ┌─────────────────────────────────┘
                                                    ▼
                                            DELTA > +10%? → KEEP
                                            DELTA < -10%? → ROLLBACK
                                            BETWEEN?      → FLAG FOR HUMAN REVIEW
```

## Implementation Plan

### Step 1: D1 Table — kaizen_validation

```sql
CREATE TABLE IF NOT EXISTS kaizen_validation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    improvement_id TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    before_value REAL,
    after_value REAL,
    delta_pct REAL,
    sample_size INTEGER,
    verdict TEXT,  -- KEPT, ROLLED_BACK, INCONCLUSIVE
    applied_at TEXT DEFAULT (datetime('now')),
    validated_at TEXT,
    commit_sha TEXT
);
```

### Step 2: Validation Tool — validate_improvement.py

```python
# Pull from R2: qnfo/tools/validate_improvement.py
def validate(improvement_id, metric_name, wait_sessions=5):
    before = pull_metric_before_improvement(improvement_id, metric_name)
    after = pull_metric_after_wait(improvement_id, metric_name, wait_sessions)
    delta = (after - before) / before * 100
    if delta > 10:
        return 'KEPT', delta
    elif delta < -10:
        rollback(improvement_id)
        return 'ROLLED_BACK', delta
    return 'INCONCLUSIVE', delta
```

### Step 3: Metrics That Matter

| Improvement Type | Metric | Source | Wait Period |
|:-----------------|:-------|:-------|:------------|
| Temperature reduction | phantom_claims / session | closeout-manager §2.7 | 5 sessions |
| Prompt restructure | execution_ratio | closeout-manager §2.7 | 3 sessions |
| Skill cross-link | cross_link_effectiveness | closeout-manager §2.7.1 | 5 sessions |
| js-yaml fix | skill load failures (from agent.db) | bootstrap_skills.py --health | 3 sessions |
| Infrastructure change | Worker error rate | infrastructure-audit | 3 sessions |

### Step 4: Integration with Kaizen Engine

After every improvement application:
1. Record in D1 `kaizen_improvements` table
2. Schedule validation after N sessions
3. closeout-manager §2.7 checks pending validations at session end
4. If N sessions elapsed: run validation, report verdict

## Co-Occurrence Data (Phase 2.2)

From the 318-session baseline, verified co-occurring pairs:

| Rank | Skill A | Skill B | Sessions | Verified? |
|:----:|:--------|:--------|:--------:|:---------:|
| 1 | closeout-manager | qnfo-agent | 171 | ✅ CORE |
| 2 | closeout-manager | execution-guard | 152 | ✅ CORE |
| 3 | qnfo-agent | execution-guard | 152 | ✅ CORE |
| 4 | closeout-manager | red-team-dod | 135 | ✅ STRONG |
| 5 | closeout-manager | cloudflare-deployer | 132 | ✅ STRONG |
| 6 | closeout-manager | infrastructure-audit | 93 | ✅ VERIFIED |
| 7 | qnfo-agent | red-team-dod | 93 | ✅ VERIFIED |
| 8 | qnfo-agent | cloudflare-deployer | 93 | ✅ VERIFIED |
| 9 | qnfo-agent | infrastructure-audit | 87 | ✅ VERIFIED |
| 10 | execution-guard | red-team-dod | 83 | ✅ VERIFIED |

**Key finding:** The session lifecycle pipeline (closeout → qnfo-agent → execution-guard → red-team-dod) dominates with 135-171 co-occurrences. This validates that Related: headers in this pipeline are NOT metadata theater — they reflect actual session behavior.

## Cross-Link Effectiveness Schema (Phase 2.4)

```sql
CREATE TABLE IF NOT EXISTS cross_link_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_skill TEXT NOT NULL,
    to_skill TEXT NOT NULL,
    session_count INTEGER DEFAULT 0,
    triggered_count INTEGER DEFAULT 0,
    trigger_rate REAL,
    effectiveness VARCHAR,  -- STRONG, WEAK, DEAD
    last_updated TEXT DEFAULT (datetime('now'))
);
```

**Classification:**
- trigger_rate ≥ 70% → STRONG (keep link)
- trigger_rate 30-70% → WEAK (monitor)
- trigger_rate < 30% → DEAD (flag for removal)

---

> **Version:** v1.0 — Phase 2.1 + 2.4 Architecture. Implementation deferred to next session.
