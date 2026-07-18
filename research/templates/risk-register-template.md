# Risk Register Template

> Used in `PROJECT-PLAN.md` Phase 0 (Project Initialization). Minimum 5 risks required at project init; update at every phase closeout.

| ID | Risk | Phase(s) Affected | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-01 | Prior art / duplicate research already exists in QNFO corpus or externally | 1 | Medium | High | Mandatory Due Diligence Gate (KG + D1 + Vectorize + external search) before Phase 2 launch | Agent | open |
| R-02 | Citations cannot be verified / DOIs missing | 3 | Medium | Medium | BibTeX audit script (`_citation_audit.py`), auto-generate missing DOIs via `doi.org` | Agent | open |
| R-03 | Core claim is logically invalid or unfalsifiable as originally stated | 0, 4 | Low | High | Core Claim Lock step (Phase 0.3) -- reformulate before any downstream work | Agent | open |
| R-04 | Zenodo API failure / draft duplication on retry | 5 | Medium | Low | Exponential backoff retry (1s/4s/16s), recover existing draft via `GET /deposit/depositions?q=<title>` instead of recreating | Agent | open |
| R-05 | PDF renders with Unicode replacement characters (broken math/symbols) | 5 | Medium | High | Mandatory `_check_pdf.py` verification gate before Zenodo upload | Agent | open |
| R-06 | Single point of failure in content distribution (one IPFS pinner down) | 8 | Low | Medium | 4-D Distribution mandate: >=3 independent pinning services (Pinata + Lighthouse + Arweave/Filebase) | Agent | open |
| R-07 | Publication contains internal/project language leaking into public output | 5 | Medium | High | Publication Language Gate scan (blocking) before "publication-ready" declaration | Agent | open |
| R-08 | Scope creep -- project WBS grows without corresponding PROJECT-PLAN.md updates | 0-8 | Medium | Medium | Phase Closeout Protocol requires re-verification of WBS at every phase tag | Agent | open |

**Likelihood/Impact scale:** Low / Medium / High
**Status values:** `open` -> `mitigated` -> `realized` -> `closed`

**Instructions:** Add project-specific risks beyond this baseline set. Review and update status at every Phase Closeout. A risk marked `realized` requires an incident note in the project's HANDOFF.md or closeout summary.
