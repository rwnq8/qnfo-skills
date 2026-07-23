# Anomalous Dimensions γ_φ in the p-Adic OPE

> **Workstream B4 | Tier 2 — Structurally Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `critical-exponents-p-adic-phi4.md` (B3), `p-adic-feynman-propagator.md` (B1), `s-matrix-structural-failure.md` (B5)
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P2

---

## Executive Summary

In Archimedean QFT, anomalous dimensions γ_φ arise from loop corrections: the scaling dimension of a field shifts from its classical (free) value. In p-adic QFT, the operator product expansion (OPE) has a completely different structure because ℚ_p is ultrametric: the OPE CONVERGES everywhere (not just on the light cone). The Vladimirov operator D^α replaces ∂_μ, changing the classical scaling dimension. Loop corrections are structurally different — the p-adic propagator has no UV divergences, so the anomalous dimension may be NON-PERTURBATIVE (determined by the conformal bootstrap on the Bruhat-Tits tree boundary rather than by loop integrals).

---

## 1. Archimedean Structure

The OPE: φ(x)φ(0) ∼ ∑_k C_k(x) O_k(0) as x → 0. The scaling dimension Δ_φ = d/2 − 1 + γ_φ where γ_φ is the ANOMALOUS dimension from loop corrections. In φ⁴ at one loop: γ_φ = ħ²/(12·(4π)⁴) + O(ħ³).

## 2. p-Adic OPE

### 2.1 Convergence Everywhere

In ℚ_p, the ultrametric inequality |x+y|_p ≤ max(|x|_p, |y|_p) means the OPE converges EVEN WHEN OPERATORS ARE AT FINITE SEPARATION — not just in the short-distance limit. This is because p-adic balls are clopen (both open and closed), and local operators localized in disjoint balls STRICTLY COMMUTE. [established]

### 2.2 Free Scaling Dimension

The Vladimirov operator gives the propagator G(x) ∼ |x|_p^{α−d}. The classical scaling dimension: Δ_φ^{(0)} = (d−α)/2. For α = 2 (the "standard" Vladimirov operator, dimension 2): Δ_φ^{(0)} = (d−2)/2 = same as Archimedean for d=4 → Δ_φ^{(0)} = 1.

But **α can take any value** — it's a free parameter of p-adic QFT. Different α → different universality class. [established from Vladimirov-Volovich]

### 2.3 Anomalous Dimension

γ_φ = Δ_φ − (d−2)/2. In the p-adic hierarchical model (Missarov): the β-function has a non-trivial fixed point (determines the critical exponents, B3). The ANOMALOUS dimension at that fixed point is determined by the scaling of the two-point function at criticality:

```
⟨φ(x)φ(0)⟩ ∼ |x|_p^{−2Δ_φ}    [at the critical point]
```

Δ_φ is computed from the p-adic RG fixed point. The value depends on p and differs from the Archimedean value. Since the fixed points are DIFFERENT (B3), the anomalous dimensions are DIFFERENT. [established]

## 3. Bootstrap Determination

On the Bruhat-Tits tree boundary ℙ¹(ℚ_p), the p-adic CFT has well-defined scaling dimensions. The conformal bootstrap on the tree determines Δ_φ from crossing symmetry of the four-point function:

```
⟨O(x₁)O(x₂)O(x₃)O(x₄)⟩ = [p-adic conformal block expansion]
```

The crossing equation constrains Δ_φ to DISCRETE values — the conformal bootstrap is EXACT on the tree (no truncation error). [my conjecture — extension of Gubser et al. p-adic AdS/CFT]

## 4. Difference from Archimedean

| Feature | Archimedean γ_φ | p-Adic γ_φ |
|:--------|:---------------|:-----------|
| Origin | Loop corrections (perturbative) | RG fixed-point structure (non-perturbative) |
| Dependence on π | π² in loop integrals | No π (p-adic propagator) — rational function of p |
| UV divergences | Yes — renormalization needed | No — tree minimum distance provides UV cutoff |
| Bootstrap | Numerical — conformal bootstrap with numerical bounds | Possibly EXACT — p-adic CFT on tree may be exactly solvable |

## 5. Falsifiability

If A_p(s,t) Mellin amplitudes (C1-RT.2) yield scaling dimensions Δ_φ that match NO known CFT → p-adic anomalous dimensions are ruled out for physical systems.

---

*[established] for the form of the Vladimirov propagator and free scaling dimension. [speculative] for exact bootstrap on the tree.*
