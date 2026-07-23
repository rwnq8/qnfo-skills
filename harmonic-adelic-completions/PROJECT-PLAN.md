# Project Plan: Harmonic-Adelic Completions

**Project:** Red-team p-adic/adélic re-evaluation of Harmonic Paradigm core concepts
**Slug:** harmonic-adelic-completions
**Status:** Phase 0 — Init
**Date:** 2026-07-23
**Author:** DeepChat Research Agent

---

## 1. Charter

The Harmonic Paradigm V1.0–V4.0 (2026) proposed the harmonic oscillator as the "universal IR attractor of quantum theory," spanning an 8-rung ladder from transmon anharmonicity through QED fine-structure constant to quantum gravity. V4.0 formally closed out the program, retracting the logistic β-function ansatz but leaving unresolved: were the remaining falsification pillars (equal-ln(μ)-spacing order-statistics test, power-law vs logarithmic IR approach) tested exclusively over ℝ when V1.0's own bibliography cited Vladimirov-Volovich-Zelenov p-adic QFT (1994) and Ostrowski (1918)?

This project is a **red-team followup** scoped to three questions:

1. **What is "harmonic" adélically?** Vladimirov's p-adic fractional derivative produces eigenfunctions on the Bruhat-Tits tree with eigenvalues spaced by powers of p in the p-adic norm — fundamentally different from the Archimedean E_n = ℏω(n+1/2) equal-spacing. Is there a genuinely adelic concept of "harmonic" with completions at every place, or is "harmonic oscillator" an Archimedean-only construct borrowed by the p-adic community by analogy?

2. **Is the IR attractor property place-specific?** The HP's core flow α(μ→0) → 0 toward the harmonic IR fixed point was tested exclusively over ℝ. The β-function mechanics (differentiation with respect to ln(μ), μ ∈ ℝ) are inherently Archimedean. Does a p-adic renormalization group even have a well-defined β-function, and if so, does it have the same leading-order class (quadratic) at every Ostrowski place?

3. **RS-1 α⁻¹ p-adic evaluation.** The decomposition α⁻¹(0) ≈ 137 = H_5 numerator (137/60) + Δ_adelic + Δ_RG yields a rational core (137) with well-defined p-adic valuations. Is the near-integer coincidence α⁻¹ ≈ 137.036 cosmetic or does it reflect a genuine adelic product-formula condition ∏_v |·|_v = 1 constraining the rational core?

## 1.2 Core Claim Lock

**Original HP claim** (from V1.0, Note 3 researcher motivation):
> "Ostrowski's theorem... the harmonic oscillator is universal across completions."

**Reformulated for falsifiability:**
> "The harmonic oscillator's IR attractor property — specifically, the leading-order β-function behavior (quadratic near the Gaussian fixed point) — is independent of the choice of Ostrowski completion. If this is true, then a p-adic β-function defined via the Vladimirov fractional derivative must yield the same leading-order class as the Archimedean one."

**Disconfirmation condition:** If the p-adic Vladimirov operator D_p^α yields eigenvalues proportional to |k|_p^α (ultrametric spacing), while the Archimedean Laplacian yields k² (continuous spacing), then the "harmonic" structure itself is place-dependent — the equal-spacing property that makes the harmonic oscillator an IR attractor is specific to the ∞-place.

## 2. WBS

| Phase | Description | Gate |
|:------|:------------|:-----|
| 0 | Init — scaffold, claim lock | Repo created, branch confirmed |
| 1 | Vladimirov oscillator spectrum extraction | Exact eigenvalue structure from VVZ 1994 |
| 2 | "Harmonic" concept — place-dependent audit | Table: Archimedean vs p-adic "harmonic" properties |
| 3 | IR attractor place-independence evaluation | β-function viability at each place |
| 4 | RS-1 α⁻¹ p-adic evaluation | Product formula test, cosmetic vs non-cosmetic |
| 5 | Synthesis red-team memo | Gate memo in artifacts/ |

## 3. Deliverable Registry

| Deliverable | Path | Type |
|:------------|:-----|:-----|
| Project Plan | PROJECT-PLAN.md | Planning |
| Gate Memo | artifacts/gate-memo-harmonic-adelic.md | Analysis |
| Notebook: Vladimirov oscillator | notebooks/vladimirov-p-adic-oscillator.md | Computation |
| Notebook: RS-1 p-adic | notebooks/rs1-p-adic-evaluation.md | Computation |

## 4. Risk Register

| # | Risk | Severity | Mitigation |
|:--|:-----|:---------|:-----------|
| R1 | VVZ 1994 not accessible for direct extraction | High | Use QNFO Ultrametric QG paper (§3.4 Vladimirov operator) as proxy |
| R2 | p-adic RG β-function not defined in literature | Medium | Define explicitly; acknowledge gap if no consensus exists |
| R3 | RS-1 evaluation reduces to trivial statement (all rationals satisfy product formula) | Medium | Distinguish trivial rational-core property from non-trivial physical constraint |
| R4 | Confirmation bias — over-interpreting weak p-adic signals | Medium | Red-team each finding; require falsifiability statement |

## 5. Success Criteria

1. Vladimirov oscillator spectrum explicitly compared to Archimedean E_n = ℏω(n+1/2)
2. Three-place comparison table: Archimedean, p-adic (fixed p), adelic
3. RS-1 α⁻¹ decomposition classified as cosmetic or potentially non-cosmetic with specific evidence
4. Falsifiability conditions stated for any non-cosmetic classification

## 6. Version History

| Version | Date | Description |
|:--------|:-----|:------------|
| v0.1 | 2026-07-23 | Phase 0 init |
