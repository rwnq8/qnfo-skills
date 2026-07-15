# Red-Team Audit: Systematic Skills Loading & Usage v2.0

> **Based on empirical data from 318 sessions, 58 skills, co-occurrence analysis, and health dashboard.**

## Data Foundation

| Metric | Value |
|:-------|:------|
| Total skills | 58 |
| Validation status | 58/58 clean (0 warnings, 0 broken) |
| Health status | 47 HEALTHY, 11 DEGRADED, 0 CRITICAL |
| Skills with 0 loads | 5 |
| Top pipeline: session lifecycle | 73% |
| Top pipeline: research | 16% |

## Finding 1: Research Pipeline Starved [CRITICAL]

closeout-manager (232 loads, 73%) vs deep-research (0 loads, 0%). The system manages itself 4-5× more than it does research. Fix: expand deep-research intake triggers beyond "Forecast:" to "analyze," "evaluate," "assess the field."

## Finding 2: Cross-Link Metadata Theater [CRITICAL]

21 skills reference deep-research in Related: headers. deep-research has 0 loads. 100% of cross-links are unvalidated. Fix: wait for usage data, then prune links with <10% trigger rate after 30 days.

## Finding 3: 25 Skills Are Consolidation Candidates [SIGNIFICANT]

25 of 58 (43%) have <10 sessions across 318 total. Fix: merge Cloudflare platform skills into single `cloudflare-platform` skill.

## Finding 4: No Session Type Classification [SIGNIFICANT]

We know which skills load but not WHY. Fix: add session_type to D1 audit_sessions at closeout.

## Finding 5: No Cost Model for Skill Loading [SIGNIFICANT]

qnfo-agent alone (190K chars) exceeds 64K context budget. Fix: trim qnfo-agent; add token cost to health dashboard.

## Finding 6: Layer 5 Validation Gap [SIGNIFICANT]

D1 tables created but never populated. Fix: deploy kaizen_validation + cross_link_metrics tables; wire validate_improvement.py to closeout-manager.

## Finding 7: Skill Effectiveness Unknown [MODERATE]

We know load counts but not success/failure rates. Fix: add skill_effectiveness metric to closeout-manager §2.7.

> **Version:** v1.0 — Phase 2.2 deliverable. Red-team audit of systematic skills loading and usage.
