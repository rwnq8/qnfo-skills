# QNFO DECISION LOG

> **Source:** D1 Knowledge Graph (`qnfo-graph`), label `Decision`, 27 nodes (25 valid + 2 blank)
> **Last reconciled:** 2026-07-12 (Session 17)
> **Total decisions:** 25 active records across ADR-003–DEC-033

---

## DECISION INVENTORY

| ID | Title | Status | Logged |
|:---|:------|:------:|:------:|
| ADR-003 | Markdown-First Architecture | accepted | 2026-06-03 |
| ADR-004 | Subagent Slot IDs in DEFAULT.md Must Match Runtime Platform | accepted | 2026-06-03 |
| ADR-005 | PM Template Catalog Restructured into Active/Deprecated/Legacy Tiers | deprecated | 2026-06-03 |
| ADR-006 | Cross-Project Learnings (CPL) Is Wiki-Based, Not Local File | accepted | 2026-06-03 |
| ADR-007 | ARCHITECTURE.md Is Wiki-Based | accepted | 2026-06-03 |
| ADR-008 | System Prompt Generator v4.7 Scope Boundary Enforced | accepted | 2026-06-03 |
| ADR-009 | Theme Toggle | accepted | 2026-06-03 |
| ADR-012 | Cache-Control Override via _headers for Cloudflare Pages | accepted | 2026-06-03 |
| ADR-013 | DNS CNAME Must Point to Project Subdomain, NOT Deployment Hash | accepted | 2026-06-03 |
| ADR-014 | robots.txt + sitemap.xml as Static Files in Cloudflare Pages | accepted | 2026-06-03 |
| DEC-015 | QC Gates Must Hard-Block in All Execution Modes | accepted | 2026-06-03 |
| DEC-016 | Custom Domain is Canonical Web URL, Not Cloudflare Pages Preview URL | accepted | 2026-06-03 |
| DEC-017 | Single Umbrella Pages Project for All Publications | accepted | 2026-06-03 |
| DEC-018 | TTF Font Embedding Required for All PDFs | accepted | 2026-06-03 |
| DEC-019 | Template Parameter Discovery Gap Requires META Session | accepted | 2026-06-03 |
| DEC-020 | Portfolio Reduction — 17 Active → 12 Active | superseded | 2026-06-03 |
| DEC-021 | Sprint Prioritization — 3-Tier Model | accepted | 2026-06-03 |
| DEC-022 | Sprint Handoff to Projects Agent | accepted | 2026-06-01 |
| DEC-023 | GitHub Fully Deprecated — All References Purged | deprecated | 2026-06-03 |
| DEC-024 | Master Discovery Index v2.0 — Single Source of Truth | accepted | 2026-06-03 |
| DEC-025 | D1 Knowledge Graph Re-Seed from Clean Index | rejected | 2026-06-03 |
| DEC-026 | Infrastructure Reconciliation Gate Required | proposed | 2026-06-03 |
| DEC-032 | qwav-scan-scraper — Permanently Archived | accepted | 2026-06-03 |
| DEC-033 | Portfolio API D1 Recovery — New Database Created | accepted | 2026-06-03 |

### Status Distribution

| Status | Count |
|:-------|:-----:|
| accepted | 20 |
| deprecated | 2 |
| rejected | 1 |
| superseded | 1 |
| proposed | 1 |

---

## SESSION 15 DECISIONS (2026-07-12)

These were created during Session 15 infrastructure audit and referenced in the handoff as
`DEC-2026-07-12-001` and `DEC-2026-07-12-002`. They do not appear under the `Decision` label
in the KG with those exact IDs. Possible explanations:

1. Stored under a different label (e.g., `AuditFinding`, `SessionNote`)
2. Referenced only in the `portfolio-state` D1 `decisions` table (26 records, not directly queried here)
3. Not yet written to the KG

### DEC-2026-07-12-001: Infrastructure Audit Confirmed All Baselines Match
- **Status:** recorded
- **Summary:** Full audit of 6 resource types (D1×5, KV×1, Vectorize×3, Pages×10, Workers×24, Queues×1)
  confirmed all counts match canonical baselines. 24/24 domains live, 0 522-risk, 0 CNAME chains.

### DEC-2026-07-12-002: Skill R2 Sync Restored 10 Key Skills
- **Status:** recorded
- **Summary:** All 55 skills synced to `qnfo/prompts/skills/<name>/SKILL.md` on R2.
  10 safety-net skills verified via `wrangler r2 object get`.

---

## DECISION GAPS

| Gap | Note |
|:----|:-----|
| ADR-001, ADR-002 | Referenced in code but not in KG Decision label |
| ADR-010, ADR-011 | Missing from KG — possibly deleted or never created |
| DEC-027 through DEC-031 | Missing from KG — gap in numbering |
| DEC-2026-07-12-001/002 | Referenced in Session 15 handoff but not in KG Decision label |

---

## RECONCILIATION NOTE

The KG `Decision` label contains 27 nodes (25 valid). The `portfolio-state` D1 `decisions` table
reports 26 records (MASTER-INVENTORY). There is a 1-record discrepancy (25 in KG vs 26 in D1)
that may reflect the Session 15 decisions being in D1 but not yet synced to the KG.

*Log generated 2026-07-12 by QNFO agent during Session 17 Phase 1.*
