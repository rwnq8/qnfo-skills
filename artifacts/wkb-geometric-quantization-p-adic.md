# WKB and Geometric Quantization in ℚ_p: Absence of Closed Orbits

> **Workstream C4 | Tier 3 — Existentially Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `causality-in-qp.md` (C1), `time-evolution-p-adic-failure.md` (C2), `noether-continuous-symmetries-p-adic.md` (C3), `non-cosmetic-archimedean-predictions.md` §3.4
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P1

---

## Executive Summary

The WKB approximation and Bohr-Sommerfeld quantization:

```
∮ p dq = (n + γ)h    [n ∈ ℤ, γ = Maslov index]
```

require: (1) a closed orbit in phase space, (2) integration of a 1-form along a closed curve, (3) the stationary phase approximation e^{iS/ħ} with small ħ. In ℚ_p: (1) ℚ_p is totally disconnected — there are NO closed curves (no continuous paths connecting distinct points), (2) p-adic integration uses the Haar measure on open subsets, not 1-forms along curves, (3) the p-adic exponential exp_p has restricted convergence — e^{iS/ħ} is undefined for generic phases. **WKB quantization does not just fail — the very concept of a "closed orbit" has no p-adic analog.** This forces a fundamentally different approach to semiclassical quantization: spectral geometry on the Bruhat-Tits tree and Vladimirov operator spectrum, not Bohr-Sommerfeld conditions.

---

## 1. The Archimedean Structure

### 1.1 Bohr-Sommerfeld Quantization

```
∮ p dq = 2πħ(n + 1/2)    [n = 0, 1, 2, ...]
```

For a particle in a potential V(x) with turning points x₁, x₂:

```
∫_{x₁}^{x₂} √(2m(E−V(x))) dx = πħ(n + 1/2)
```

This determines the discrete energy spectrum E_n.

### 1.2 WKB Wavefunction

```
ψ(x) ∼ [p(x)]^{−1/2} exp(±i/ħ ∫ p(x') dx')
```

The WKB approximation requires: (1) slowly varying potential (λ ≪ L), (2) existence of the exponential e^{iS/ħ}, (3) matching conditions at turning points via Airy functions.

### 1.3 What All These Require

1. **Continuous paths:** ∮ p dq integrates along a closed curve in phase space → requires connectedness of the underlying space
2. **The exponential function:** exp(±iS/ħ) → requires global definition of exp
3. **Smooth potentials:** V(x) must be differentiable → requires limit of difference quotients
4. **Classical limit:** ħ → 0 → requires Archimedean "arbitrarily small" parameter

---

## 2. p-Adic Collapse

### 2.1 No Closed Orbits

ℚ_p is totally disconnected. There are NO continuous paths connecting distinct points. The concept of a "closed orbit" — an integral ∮ F(x) dx along a continuous loop — has NO p-adic analog. [established]

**What replaces it?** Integration in ℚ_p is over open subsets (clopen balls) using the Haar measure:

```
∫_{B_r(a)} f(x) dμ(x)    [integral over p-adic ball, NOT along a curve]
```

There is no "curve" to integrate along. The 1-form dq has no p-adic analog as an object to integrate along paths.

### 2.2 Exponential Failure (Compound with C2)

The p-adic exponential exp_p converges only for |x|_p < p^{−1/(p−1)}. The phase S/ħ is typically large (p-adically), so exp_p(iS/ħ) diverges for generic S, ħ.

Even if S/ħ = 0 (classical action zero): exp_p(0) = 1. But for any non-zero S/ħ with |S/ħ|_p ≥ p^{−1/(p−1)}, exp_p(iS/ħ) DIVERGES. [established from C2]

### 2.3 No Small-ħ Limit

The WKB expansion in ħ → 0 relies on the Archimedean concept of "arbitrarily small." In ℚ_p, the p-adic norm of ħ (|ħ|_p) depends on the units chosen — it's not a dimensionless small parameter in any invariant sense. The "semiclassical limit" is not universally defined p-adically. [established]

---

## 3. What Replaces WKB — Three Approaches

### 3.1 Vladimirov Operator Quantization

The Vladimirov fractional derivative D^α replaces the kinetic term p̂²/2m:

```
Ĥ = −(ħ²/2m) D^α + V(x̂)
```

The spectrum of D^α is:

```
D^α ψ_k(x) = |k|_p^α ψ_k(x)    [plane waves in ℚ_p]
```

where ψ_k(x) = χ_p(kx) are p-adic plane waves (additive characters). The energy spectrum is:

```
E_k = (ħ²/2m) |k|_p^α + V_p(k)
```

For a harmonic oscillator potential V(x) = mω²x²/2 (defined p-adically via the quadratic form), the spectrum can be computed analytically. [established from Vladimirov-Volovich]

### 3.2 Bruhat-Tits Spectral Geometry

On the Bruhat-Tits tree T_p, the Laplacian Δ_tree has a well-defined spectrum:

```
Δ_tree φ_λ = λ φ_λ    [λ ∈ [−(p+1)/p, (p+1)/p]]
```

This is the p-adic analog of the Schrödinger operator on ℝ. The "quantization condition" is:

```
λ_n = spectral parameter of Δ_tree    [determined by tree geometry]
```

This gives a DISCRETE spectrum (not continuous + WKB-discretized) directly from the tree Laplacian. No semiclassical approximation needed — the tree is fundamentally discrete. [my conjecture]

### 3.3 p-Adic Path Integral (Alternative)

Feynman's path integral:

```
K(x_f, t_f; x_i, t_i) = ∫ D[x(t)] exp(iS[x]/ħ)
```

In ℚ_p: the "paths" are maps from a p-adic time parameter to ℚ_p^n. These are NOT continuous curves (ℚ_p is totally disconnected). The "path integral" becomes a sum over combinatorial paths on the Bruhat-Tits tree:

```
K_tree(v_f, v_i) = Σ_{paths} exp_p(iS[path]/ħ)    [sum over tree paths]
```

This converges on the tree because: (1) the number of paths of length L is finite ((p+1)·p^{L−1}), (2) the action S[path] is bounded, (3) exp_p converges on the bounded domain. The tree path integral is more like a transfer matrix than a functional integral. [my conjecture]

---

## 4. The Spectral Shift — What Changes Numerically

### 4.1 Energy Levels

Archimedean WKB (harmonic oscillator):

```
E_n = ħω(n + 1/2)    [n = 0, 1, 2, ...]
```

p-adic Vladimirov spectrum (harmonic oscillator on ℚ_p):

```
E_p(k) = ħ²|k|_p^α/(2m) + (mω²/2)|x|_p²    [k, x ∈ ℚ_p]
```

The spectrum is qualitatively DIFFERENT — it depends on the p-adic norms of quantum numbers, not on integers n. States with the same integer n but different p-adic valuations have different energies.

### 4.2 Degeneracies

Archimedean: degenerate only by symmetry (e.g., rotational SO(3) for 3D).
p-adic: naturally degenerate — all states with the same p-adic norm cluster together. Ultrametric degeneracy structure reflects the tree topology.

### 4.3 The Maslov Index

The Maslov index γ (typically 1/2 for a simple turning point, different for other singularities) has NO p-adic analog because it's defined by the topology of Lagrangian submanifolds — which are real manifolds. The p-adic replacement would be a tree-based topological invariant. [speculative]

---

## 5. Connection to the Full Adelic Framework

### 5.1 Unified via the Bruhat-Tits Tree

| C-Task | Failure Mode | Bruhat-Tits Resolution |
|:-------|:-------------|:----------------------|
| C1 — Causality | No time ordering (ℚ_p not ordered) | Tree partial order (ancestor/descendant) |
| C2 — Time evolution | exp_p converges only locally | Tree Laplacian spectrum replaces exp_p |
| C3 — Noether | No infinitesimal transformations | Tree automorphisms (PGL(2,ℚ_p)) as symmetry |
| C4 — WKB | No closed orbits, no ∮ p dq | Tree spectral geometry — eigenvalues, not quantization conditions |

All four Tier 3 existential failures are resolved by the SAME geometric object: the Bruhat-Tits tree. [my conjecture]

### 5.2 The Adelic Semiclassical Limit

The "classical limit" ħ → 0 has different meanings at different places:

```
∞-place:    ħ → 0 (Archimedean continuous limit) → WKB, classical trajectories
p-adic:     ħ_p ≡ 1 (p-adic ħ is a unit, |ħ|_p = 1 for appropriate normalization) → tree discretization
```

There is NO unified "small ħ" limit across all places. The "semiclassical" regime is completion-dependent. [speculative]

---

## 6. Falsifiability

- **If the Vladimirov spectrum matches NO known quantum system** → p-adic quantization is physically irrelevant
- **If tree spectral geometry (λ_n from Δ_tree) predicts energy levels matching hadron resonances** → evidence for Bruhat-Tits quantization (see also B5 S-matrix pole structure)
- **WKB is Archimedean-only** — this is [established] because the construction requires connectedness, continuous paths, and global exp

---

## 7. Decision Log

| Decision | Rationale |
|:---------|:----------|
| WKB/geometric quantization fails existentially in ℚ_p | Closed orbits don't exist; exp_p restricted; no ħ → 0 limit |
| Bruhat-Tits spectral geometry replaces Bohr-Sommerfeld | Tree Laplacian spectrum is the natural quantization condition |
| All four Tier 3 failures (C1-C4) are unified by the Bruhat-Tits tree | Each failure is resolved or reframed by tree geometry |
| p-adic path integral on the tree is a viable constructive approach | Combinatorial sum over tree paths converges; exp_p domain is bounded |

---

## 8. References

- Vladimirov, Volovich, Zelenov (1994), *p-adic Analysis and Mathematical Physics*, §6–7. [Vladimirov operator spectrum, p-adic quantum mechanics]
- Serre (1980), *Trees*, §II. [Bruhat-Tits tree, Laplacian, spectral theory]
- Gubser et al. (2017), "p-adic AdS/CFT." [Witten diagrams on tree — the computational analog of path integral]
- QNFO Internal: `causality-redteam-full-analysis.md` (C1-RT), `time-evolution-p-adic-failure.md` (C2), `noether-continuous-symmetries-p-adic.md` (C3).

---

*The failure of closed orbits and ∮ p dq in ℚ_p is [established] (totally disconnected → no continuous curves). The Bruhat-Tits replacement of WKB is [my conjecture]. The p-adic path integral on the tree is [speculative] but grounded in the Witten-diagram computation of Gubser et al. The unification of C1–C4 via the Bruhat-Tits tree is [my conjecture].*
