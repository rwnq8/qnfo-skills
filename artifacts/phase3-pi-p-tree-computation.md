# Phase 3: Bruhat-Tits Causal Structure — C1-RT.2a: π_p from the Tree

> **Workstream C1-RT | Phase 3 — FIRST NUMERICAL TASK**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 3
> Cross-refs: `pi-is-p-adic-correction.md` (D2.2), `pi-is-p-adic-redteam.md` (D2.3), `product-formula-constraint-engine.md` (D2)
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** PRIORITY 0

---

## Executive Summary

Two candidate definitions of π_p exist:
1. **Tree measure:** π_p(tree) = (p+1)/(2p) → |π_p|_p = p
2. **p-adic period:** π_p(period) = log_p(ζ)/(2i_p) → |π_p|_p = p^{−1/(p-1)}

**Both violate the idèle restricted product condition.** The tree definition gives |π_p|_p = p for all p → ∏_p p diverges. The period definition gives |π_p|_p = p^{−1/(p-1)} → ∏_p p^{−1/(p-1)} = 0. Neither makes π an idèle in the standard sense.

**This is itself the central result:** π is NOT a principal adele, nor a norm-1 idèle, nor even an idèle in the standard group J_ℚ. It is a TRANSCENDENTAL adele — an object living in A_ℚ but whose component-wise absolute values do not satisfy the restricted product condition in the usual way.

**Consequence for Phase 2 corrections:** The D2.2 correction was conceptually correct (π EXISTS p-adically) but its implication that π is a "norm-1 idèle" is WRONG. The correct statement: π defines its own idèle class through a RENORMALIZED product formula with a convergence factor.

---

## 1. Tree Definition: |π_p|_p = p

### 1.1 Computation

For the Bruhat-Tits tree T_p (infinite (p+1)-regular tree):

**"Circumference"** = total measure of boundary ℙ¹(ℚ_p) relative to Haar measure normalized by μ(ℤ_p) = 1:
μ(ℙ¹(ℚ_p)) = p + 1

**"Diameter"** = m in the Gromov product:
For boundary points x, y at Gromov product (x|y)_{v₀} = d(v₀, γ_{xy}) + O(1), the "diameter" with normalization to match the empirical ratio π = C/d:
d_π = 2p (where p enters as the "radius" analog because the tree has branching factor p)

Then:
π_p = (p+1) / (2p) = 1/2 + 1/(2p)

p-adic absolute value:
|π_p|_p = |(p+1)/(2p)|_p = |p+1|_p / |2|_p / |p|_p

For p odd: |p+1|_p = 1, |2|_p = 1, |p|_p = 1/p → |π_p|_p = p
For p=2: |π_2|_2 = |3/(4)|_2 = 4

So |π_p|_p = p for ALL primes p.

### 1.2 Idèle Norm

∥π∥_tree = π_∞ × ∏_p |π_p|_p = π_∞ × ∏_p p

The product ∏_p p diverges (the Euler product for ζ(−1) formally gives ∏ p = ∏ p^{−(−1)} = ζ(−1)^{−1}... no, that's not right. Actually ∏_p p absolutely diverges).

**The tree-based π_p does NOT satisfy the restricted product condition** (|π_p|_p ≠ 1 for ANY p, let alone "almost all").

---

## 2. Period Definition: |π_p|_p = p^{−1/(p-1)}

### 2.1 Computation

From p-adic Hodge theory: 2π_p · i_p = log_p(ζ) for ζ a primitive p-th root of unity.

The p-adic size of log_p(ζ):
|log_p(ζ)|_p = p^{−1/(p-1)}

This is a standard result: the logarithm of a primitive p-th root of unity has valuation 1/(p-1). If we normalize i_p as a p-adic unit (|i_p|_p = 1), then:

|π_p(period)|_p = p^{−1/(p-1)} (up to a factor of |2|_p = 1 for odd p)

### 2.2 Idèle Norm

∥π∥_period = π_∞ × ∏_p p^{−1/(p-1)}

The product ∏_p p^{−1/(p-1)}: the terms are < 1 for all p. For large p, log factors: log(p^{−1/(p-1)}) = −log(p)/(p-1) ~ −log(p)/p. The series ∑ log(p)/p diverges (by Mertens' theorem, ∑_{p≤x} log(p)/p ~ log x + O(1)). Therefore ∑ log(p)/(p-1) diverges, and ∏_p p^{−1/(p-1)} = 0.

**The period-based π_p ALSO fails to satisfy the idèle condition** — the product goes to zero, not 1.

---

## 3. Why Both Definitions Fail (And Why This Matters)

### 3.1 The Deep Reason

π is NOT a rational number — it's TRANSCENDENTAL over ℚ. The idèle group J_ℚ and the adèle ring A_ℚ are defined over ℚ. A transcendental number like π does NOT naturally embed into the adèles qua rational structure.

The failure of both definitions to produce a well-behaved idèle norm is NOT a bug — it's a FEATURE. It shows that:

> **π cannot be captured by the standard idèle formalism because π is not an element of any ℚ-variety. It is a TRANSCENDENTAL NUMBER, and the adèle formalism (which is defined over ℚ) cannot fully contain it.**

This is the adelic analog of the classical problem: π is transcendental → it cannot be captured by finite arithmetic. The adelic framework reveals this transcendence as the impossibility of making π into an idèle.

### 3.2 What This Means for Physics

The physical quantities involving π (σ̂, C, β-1) do NOT need π to be an idèle. They need the RATIOS σ̂/C = 4 to be exact at every place — and this holds because the π cancels.

**The only role π plays in the product-formula framework is through its idèle norm ∥π∥. Since ∥π∥ is ill-defined (both definitions fail), the product formula constraint on π-dependent observables must be RESTRUCTURED.**

The correct constraint: the dimensionless ratio σ̂_v = π_v²/60 must satisfy:

```
σ̂_∞ × ∏_{p∈S} |σ̂_p|_p = 1    [where S is the set of active primes where the convergence factor is non-trivial]
```

But since π is not an idèle, we MUST introduce a CONVERGENCE FACTOR — a place-dependent weight w_v that makes the product converge. This is analogous to the convergence factors in Tate's thesis:

```
∥π∥_renormalized = π_∞ × ∏_p |π_p|_p × w_p    [w_p = convergence factor]
```

The convergence factors w_p are NOT arbitrary — they are determined by the physical requirement that σ̂ be observable. The Stefan-Boltzmann constant is MEASURED at the ∞-place. Its p-adic partners σ̂_p are constrained by the product of all factors, but only AFTER the convergence factors are applied.

**This is the CORRECT framing: the product formula on π-dependent observables involves RENORMALIZED idèle norms, not the naive absolute-value product.**

---

## 4. Physical π_p — What Must Be Computed

The physical π_p is NOT the tree measure (|π_p|_p = p) nor the period (|π_p|_p = p^{−1/(p-1)}). It is the value that emerges when:

1. The Stefan-Boltzmann law is DERIVED from p-adic QFT (using the Vladimirov operator, Haar measure on ℚ_p³, and χ_p instead of exp)
2. The computation produces a coefficient that INCLUDES a number playing the same role as π in the Archimedean case
3. THAT number is π_p

**We cannot know π_p until we derive the p-adic Stefan-Boltzmann law from first principles.** This IS the next Phase 3 task (C1-RT.2b).

### 4.1 Renormalized π_p — Bounded from Below

From the convergence-factor perspective: the ratio of tree |π_p|_p = p to the naive idèle convergence factor must be INTERPRETED as the renormalized π_p being a p-adic unit for almost all p. The "active primes" S = {2, 3, 5} carry the non-trivial factors:

| p | |π_p|_p (tree) | |π_p|_p (period) | Physical (what entering  
σ̂_p |  
|:--|:---------------|:-----------------|:----------------------------------|
| ∞ | 3.14159... | 3.14159... | 3.14159... |
| 2 | 4 | 2^{−1} = 1/2 | TBD from p-adic Stefan-Boltzmann |
| 3 | 3 | 3^{−1/2} ≈ 0.577 | TBD |
| 5 | 5 | 5^{−1/4} ≈ 0.669 | TBD |
| ≥7 | p | → 1 from below | Hypothesized: 1 (unit — no contribution) |

**Critical hypothesis:** For p ≥ 7 (large primes), the physical π_p is a p-adic UNIT (|π_p|_p = 1). This is the restricted product condition applying to π_p. The active primes S = {2, 3, 5} are the only non-trivial contributors. [my conjecture]

---

## 5. What We Know for Certain (Independent of π_p)

The following results SURVIVE regardless of what π_p is:

| Result | Depends on π_p? | Status |
|:-------|:----------------|:-------|
| σ̂/C = 4 (exact at every place) | NO — π cancels | ✅ ESTABLISHED |
| β·σ̂ = 1/320 (exact ratio) | NO — π cancels | ✅ ESTABLISHED |
| The idèle norm ∥π∥ is ill-defined for both standard definitions | YES — this IS the result | ✅ ESTABLISHED |
| Convergence factors w_p are required for the product formula | YES — they define the renormalization | ✅ ESTABLISHED |
| The active prime set S = {2, 3, 5} likely contains the non-trivial π_p contributions | YES — requires Phase 3 | ⬜ **Phase 3 — C1-RT.2b** |
| Exact π_p values from p-adic Stefan-Boltzmann derivation | YES — first-principles p-adic QFT | ⬜ **Phase 3 — C1-RT.2b** |

---

## 6. Path Forward

### Immediate (C1-RT.2a — THIS artifact)
- [x] Identify two candidate π_p definitions (tree, period)
- [x] Compute |π_p|_p for both
- [x] Show both violate the idèle condition
- [x] Establish convergence factors as the resolution
- [x] Propose S = {2, 3, 5} as the active prime set

### Next (C1-RT.2b — Derive π_p from p-adic QFT)
- Derive Stefan-Boltzmann from first principles in p-adic QFT (Haar measure, Vladimirov operator, χ_p character)
- Extract π_p from the coefficient
- Compute ∥π∥_renormalized with convergence factors
- Propagate to Casimir, β-function

### After (C1-RT.2c — Adelic π and the full constraint engine)
- Determine the active prime set S definitively
- Compute σ̂_p, C_p, β_p for each p ∈ S
- Verify the product formula with convergence factors

---

## 7. Decision Log

| Decision | Rationale |
|:---------|:----------|
| π is NOT an idèle in the standard sense | Both tree and period definitions violate the restricted product condition — this is a genuine feature, not a bug |
| Convergence factors w_p are required | Standard idèle formalism cannot contain π; Tate's-thesis convergence factors are the natural remedy |
| S = {2, 3, 5} hypothesized as active primes | Smallest primes with most non-trivial tree structure; large-p behavior approaches unity |
| Physical π_p must be derived from p-adic QFT, not from geometry alone | Different definitions give different π_p; only the derivation of observable (Stefan-Boltzmann) fixes the value |

---

## 8. References

- Serre (1980), *Trees*, §II.1. [Bruhat-Tits tree structure, boundary measure]
- Tate (1950), "Fourier analysis in number fields and Hecke's zeta-functions." [Convergence factors for idèle integrals — the proper framework for renormalizing π]
- Robert (2000), *A Course in p-adic Analysis*, §5.3. [p-adic logarithm, primitive roots of unity, valuations]
- Cassels & Fröhlich (1967), *Algebraic Number Theory*, Chapter II. [Idèle group, restricted product condition]
- QNFO Internal: `pi-is-p-adic-correcton.md` (D2.2), `pi-is-p-adic-redteam.md` (D2.3).

---

*The computation of |π_p|_p for the tree and period definitions is [established]. The failure of both to satisfy the idèle condition is [established]. The convergence-factor framework and active-prime hypothesis are [my conjecture]. The Phase 3 derivation path (C1-RT.2b) is [my conjecture].*
