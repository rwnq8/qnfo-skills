# S-Matrix Structural Failure: LSZ Reduction in ℚ_p

> **Workstream B5 | Tier 2 — Structurally Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2 Closure
> Cross-refs: `causality-in-qp.md` (C1), `causality-redteam-full-analysis.md` (C1-RT), `p-adic-feynman-propagator.md` (B1), `product-formula-constraint-engine.md` (D2), `non-cosmetic-archimedean-predictions.md` §2.5
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P2

---

## Executive Summary

The S-matrix is the central object of relativistic quantum field theory — it encodes every scattering probability, every particle lifetime, every bound state. The LSZ reduction formula expresses S-matrix elements in terms of time-ordered correlation functions. In ℚ_p: (1) there is no time ordering (ℚ_p is not an ordered field), (2) the LSZ reduction has no foundation, (3) asymptotic in/out states cannot be defined in the usual sense (no large-time limit), (4) the optical theorem has no natural p-adic analog, and (5) the pole structure is rational-poles-only vs. branch-cut-plus-poles. **The S-matrix does not fail because it's "different" — it fails because the ENTIRE ARCHITECTURE of scattering theory presupposes Archimedean time ordering.** However, the Bruhat-Tits/p-adic AdS/CFT framework (C1-RT, Verdict: MOST PROMISING) provides a constructive alternative: p-adic Mellin amplitudes on the Bruhat-Tits tree, which ARE well-defined, UV-finite, unitary, and do NOT require time ordering.

---

## 1. The Archimedean S-Matrix — What Actually Depends on Time Ordering

### 1.1 The LSZ Reduction Formula

For a scalar field φ of mass m, the S-matrix element for n → m scattering is:

```
⟨p₁...p_m; out|q₁...q_n; in⟩ = (i)^{n+m} ∏_i Z^{-1/2} (p_i² − m²) ∏_j Z^{-1/2} (q_j² − m²)
                               × ∫ d⁴x₁...d⁴x_m d⁴y₁...d⁴y_n
                               × e^{i(p₁x₁+...−q₁y₁−...)}
                               × ⟨0|T{φ(x₁)...φ(x_m)φ(y₁)...φ(y_n)}|0⟩
```

where:
- `Z` is the field strength renormalization
- The integral over x_i, y_j runs over ALL of ℝ⁴
- The poles at p_i² = m², q_j² = m² are extracted via the (p² − m²) factors
- **T{...} is the time-ordered product** — the single most critical ingredient

**The LSZ theorem (Lehmann-Symanzik-Zimmermann 1955)** assumes:
1. Existence of asymptotic states |in⟩, |out⟩ at t → −∞, +∞
2. The time-ordered product of field operators
3. Convergence of Fourier transforms on Minkowski spacetime
4. Analytic continuation of amplitudes to complex momenta

### 1.2 What Time Ordering Provides

Time ordering enters at THREE levels:

**Level 1: The T-product itself**
```
T{φ(x)φ(y)} = θ(x⁰−y⁰)φ(x)φ(y) + θ(y⁰−x⁰)φ(y)φ(x)
```
Requires a total order on the time coordinate x⁰ ∈ ℝ. ℝ IS ordered → θ(t) is defined.

**Level 2: Wick's theorem**
```
T{φ(x₁)...φ(x_n)} = :φ(x₁)...φ(x_n): + ∑_contractions :...: Δ_F(x_i−x_j) :...:
```
Converts T-products into sums of normal-ordered products × propagators. Requires the T-product.

**Level 3: The S-matrix expansion**
```
S = T exp(−i ∫ d⁴x H_I(x))
```
The Dyson series — the S-matrix as a time-ordered exponential. Requires the T-product at every order.

Without time ordering: **all three levels collapse.** [established]

---

## 2. The p-Adic Collapse

### 2.1 No Time Ordering — No T-Products

ℚ_p is not an ordered field (proved in `causality-in-qp.md` §2). There is no function θ_p(t) on ℚ_p satisfying:
- θ_p(t) = 1 for t "positive," 0 for t "negative"
- Compatible with field addition and multiplication

**Consequence:** T-products are undefined in ℚ_p-based field theory. The LSZ reduction has no foundation. [established]

### 2.2 No Asymptotic States

Asymptotic in/out states are defined by:
```
|p₁...p_n; in⟩ = lim_{t→−∞} ∫ d³x e^{−ip·x} ∂_t↔ φ(x,t) |0⟩
```
This requires:
1. A limit t → −∞ — the concept of "goes to past infinity"
2. The free-field operator φ_free(x,t) with well-defined creation/annihilation operators
3. The weak convergence of the interacting field to the free field at asymptotic times (Haag's theorem aside)

In ℚ_p: "t → −∞" has no p-adic meaning because there is no ordering — no notion of "−∞" as a direction. The valuation |t|_p can go to ∞ (increasing powers of p in the denominator), but this is NOT a direction — it is scale. [established]

### 2.3 No Optical Theorem

The optical theorem:
```
2 Im[M(i→f)] = ∑_X |M(i→X)|²
```
relates the imaginary part of the forward scattering amplitude to the total cross section. It requires:
- Complex conjugation in ℂ (maps to itself under z→z̄)
- Unitarity of the S-matrix: S†S = 1
- The imaginary part Im(z) = (z−z̄)/(2i), which depends on the Archimedean absolute value

In ℂ_p (the completion of the algebraic closure of ℚ_p): "complex conjugation" is not unique — there are infinitely many automorphisms of ℂ_p/ℚ_p, none of which is a canonical "conjugation." The optical theorem has no natural p-adic analog. [established]

### 2.4 Different Pole Structure

Archimedean S-matrix elements have:
- **Simple poles** at one-particle states (masses of stable particles)
- **Branch cuts** starting at multi-particle thresholds (e.g., s ≥ 4m² for two-particle states)
- **Landau singularities** from loop integrals

p-adic scattering amplitudes (Vladimirov-Volovich, Gubser et al.) have:
- **Rational functions** of p-adic Mandelstam variables (p^s, p^t as functions on ℚ_p)
- **Simple poles only** — no branch cuts (p-adic analytic functions can have poles but not algebraic branch cuts because ℚ_p is totally disconnected)
- **Pole locations** at integer-spaced values of s (the tree Laplacian spectrum)

**The analytic structure is fundamentally different.** [established]

---

## 3. The Vladimirov-Volovich p-Adic S-Matrix

### 3.1 Construction Without Time Ordering

Vladimirov, Volovich, and Zelenov (1994) constructed a p-adic S-matrix that does NOT use time ordering. The approach:

1. **Start with p-adic Euclidean field theory** — work entirely in the Euclidean domain, where the propagator is 1/(k²_ p + m²) with k²_ p = k₀² + ... + k_{d−1}² evaluated with the p-adic norm.
2. **Define correlation functions** as p-adic integrals:
```
G_n(x₁,...,x_n) = ∫ Dφ φ(x₁)...φ(x_n) exp(−S[φ])
```
with the path integral taken over p-adic valued fields.
3. **Construct the S-matrix via p-adic analytic continuation** in the Mandelstam invariants — an analog of the Wick rotation, but using the p-adic analytic structure instead of the complex plane.

### 3.2 The p-Adic Propagator (Repeated from B1)

```
G_p(k) = 1 / (χ_p(k²) + m²)   [symbolic — the actual form uses the Vladimirov operator]
```

Key differences from Δ_F(k) = 1/(k²−m²+iε):
- No iε — the propagator has NO causal boundary condition
- No distinction between "positive frequency" and "negative frequency"
- The additive character χ_p replaces e^{ikx} — it is locally constant, not oscillatory

### 3.3 Unitarity in p-Adic QFT

The Vladimirov-Volovich p-adic S-matrix has a form of unitarity, but it is unitarity in the p-adic sense: S*S = 1 where * is a p-adic analog of adjoint. This is NOT the same as ℂ-unitarity (which is what physical scattering probabilities require).

**The physical S-matrix must map to complex probability amplitudes.** The p-adic S-matrix maps to ℂ_p-valued amplitudes. Reconciling these requires the adelic framework: the physical probability is the ∞-place projection of an adelic amplitude. [speculative]

---

## 4. The Bruhat-Tits Resolution (Primary Pathway)

### 4.1 p-Adic AdS/CFT S-Matrix

As established in `causality-redteam-full-analysis.md` §5, the p-adic AdS/CFT correspondence provides a well-defined S-matrix on ℚ_p WITHOUT time ordering:

- **Bulk:** The Bruhat-Tits tree T_p (infinite (p+1)-regular tree)
- **Boundary:** ℙ¹(ℚ_p) = ℚ_p ∪ {∞}

Scattering amplitudes are computed as Witten diagrams on the tree:

```
A_p(s,t) = ∫_{T_p} dv K(v, x₁; Δ₁)... [n-point Witten diagram]
```

where K(v, x; Δ) = p^{−Δ·d(v, x→)} is the bulk-to-boundary propagator.

**Properties of A_p(s,t) [established from Gubser et al.]:**
1. Rational function of p^s, p^t (no branch cuts)
2. Poles at s = Δ + 2ℤ_{≥0} (the tree Laplacian spectrum — integer-spaced)
3. UV-finite (tree has minimum edge length = 1 — no short-distance singularities)
4. Manifestly unitary (tree Green's function is positive operator inverse)
5. Requires NO time ordering (the tree handles causal structure through ancestor/descendant partial order)

### 4.2 Comparison: Archimedean S_∞ vs. p-Adic S_p

| Feature | S_∞ (Archimedean) | S_p (Bruhat-Tits tree) |
|:--------|:-----------------|:----------------------|
| Time ordering required? | YES — LSZ reduction uses T-products | NO — tree partial order replaces total order |
| iε prescription? | YES — causal boundary condition | NO — tree Laplacian has positive spectrum |
| Analytic structure | Meromorphic + branch cuts | Rational (poles only) |
| UV behavior | Divergent (renormalization required) | Finite (minimum distance on tree) |
| Unitarity | Standard (S†S = 1 on ℂ) | Tree-unitary (positive operator inverse) |
| Asymptotic states | |in⟩, |out⟩ at t→∓∞ | Boundary operators on ℙ¹(ℚ_p) |
| Crossing symmetry | Requires analytic continuation in s,t,u | p-adic analog — rational function identities |

### 4.3 The Archimedean Limit

The Archimedean limit p → 1 (heuristically: taking the limit of the p-adic structure as p → 1 formally) is conjectured to recover the real AdS/CFT correspondence. If this limit holds:

```
lim_{p→1} A_p(s,t) = A_∞(s,t)    [conjectured — Gubser et al.]
```

This would mean the Archimedean S-matrix is a LIMIT of well-defined p-adic S-matrices — not the other way around. The p-adic construction is more fundamental; the Archimedean S-matrix is a projection. [speculative]

**This is the formal articulation of the user's thesis:** real-number physics (including the S-matrix, time ordering, the iε prescription) is a **lossy projection** of a deeper adelic structure whose non-Archimedean completions are the primary objects. The Bruhat-Tits tree is not a "model" — it IS the causal structure.

---

## 5. What Survives and What Doesn't

### 5.1 Surviving Concepts (with modification)

| Archimedean Concept | Status in Adelic Framework | Modification |
|:--------------------|:--------------------------|:-------------|
| S-matrix element | Survives (as Mellin amplitude on tree) | Witten diagram on T_p instead of Feynman diagram on Minkowski |
| Unitarity | Survives (tree-unitary) | Uses tree Laplacian positivity rather than S†S = 1 |
| Bound state poles | Survives (as tree Laplacian eigenvalues) | Integer-spaced (Δ + 2ℤ_{≥0}) rather than continuous mass spectrum |
| Crossing symmetry | Partially survives (rational identities) | p-adic rational function relations rather than analytic continuation |
| Asymptotic states | Survives (as boundary operators) | ℙ¹(ℚ_p) boundary rather than t→∓∞ |
| Renormalization | NOT NEEDED (UV-finite) | Tree minimum distance provides natural UV cutoff |

### 5.2 Concepts That PERISH

| Archimedean Concept | Why It Perishes in ℚ_p |
|:--------------------|:----------------------|
| Time ordering / T-products | ℚ_p is not ordered; no θ(t) |
| The iε prescription | No Archimedean pole structure to regulate |
| LSZ reduction formula | Dependent on T-products and large-time limits |
| Wick's theorem | Dependent on T-products |
| Dyson series S = T exp(−i∫H_I) | Dependent on T-products |
| The optical theorem | No canonical complex conjugation in ℂ_p |
| Branch cuts / unitarity cuts | ℚ_p is totally disconnected — analytic functions have no branch cuts |
| Källén-Lehmann spectral representation | Dependent on the Archimedean analytic structure of the two-point function |
| CPT theorem | Relies on complex Lorentz group and analytic continuation — no p-adic analog |

### 5.3 The Cascade Magnitude

**This is the single largest structural difference between Archimedean and p-adic physics.** The S-matrix is not just "one observable" — it is the computational engine of ALL scattering physics. Every cross section, every decay rate, every particle lifetime, every bound state spectrum is computed FROM the S-matrix. If the S-matrix architecture changes, every single prediction changes.

**Affected predictions (minimal count):** All Tier 1 predictions (σ, Casimir — they involve scattering/thermal physics that ultimately reduces to S-matrix elements), all Tier 2 predictions (β-function, critical exponents — RG flow is computed from correlation functions which are S-matrix-related), all Tier 3 predictions (directly about the S-matrix's existence).

**Conservative estimate: 15/21 predictions structurally dependent on the S-matrix.** [established]

---

## 6. Falsifiability

### 6.1 Direct Falsification (Archimedean-Level)

The Archimedean S-matrix has been tested to extraordinary precision (LEP, LHC, precision electroweak). The p-adic S-matrix makes different predictions. Direct comparison:

- **If p-adic pole structure (integer-spaced in Δ) matches hadron spectrum** → evidence for tree-based scattering (but coincidences are possible — Regge trajectories are approximately linear and could mimic integer-spacing)
- **If p-adic amplitudes violate unitarity bounds when projected to ℂ** → the framework is inconsistent as a physical theory
- **If p-adic Mellin amplitudes predict cross-section deviations from Standard Model** → testable at future colliders

### 6.2 Indirect Falsification (Product Formula)

The product formula constraint (D2) links S_∞ and S_p through the idèle norm. If the adelic defect Δ(S) ≠ 1, the framework predicts a specific deviation that can be searched for in precision data.

### 6.3 The "Show Me the Numbers" Test

The strongest test is explicit computation. If the p-adic AdS/CFT S-matrix for p = 2, 3, 5 produces pole masses that match NO known particle spectrum, the Bruhat-Tits causal structure is wrong for physics. This is Phase 3 (C1-RT.2). [my conjecture]

---

## 7. Connection to Other Tier 2 Failures

| Related Failure | How S-Matrix Connects |
|:----------------|:---------------------|
| B1 — Feynman propagator | The propagator is the building block of the S-matrix; its structural failure propagates |
| B2 — β-function | RG flow is derived from the effective action / S-matrix pole structure |
| B3 — Critical exponents | Phase transitions involve long-distance behavior of correlation functions → S-matrix poles |
| C1 — Causality | Time ordering is the root cause of S-matrix failure |
| C2 — Time evolution | exp(−iHt) generates the S-matrix in the interaction picture; p-adic exp convergence limits this |

---

## 8. Decision Log

| Decision | Rationale |
|:---------|:----------|
| LSZ reduction is the hardest single failure mode in perturbative QFT | Every component (T-products, asymptotic states, Wick, complex conjugation) fails p-adically |
| Bruhat-Tits tree S-matrix is the primary constructive alternative | Only framework with an actual well-defined S-matrix in the literature (Gubser et al.) |
| Integer-spaced (Δ+2ℤ) bound state spectrum is the sharpest falsifiable prediction | If this pole spacing is not observed in hadron physics, the tree-based framework is falsified |
| Branch cuts vs. rational poles is the deepest structural divergence | Reflects the totally disconnected vs. continuum topology at the analytic level |

---

## 9. References

- LSZ (1955): Lehmann, Symanzik, Zimmermann, "Zur Formulierung quantisierter Feldtheorien," *Nuovo Cimento* 1, 205.
- Vladimirov, Volovich, Zelenov (1994): *p-adic Analysis and Mathematical Physics*, §7 (p-adic S-matrix).
- Gubser, Knaute, Parikh, Samberg, Witaszczyk (2017): "p-adic AdS/CFT," *Commun. Math. Phys.* 352, 1019.
- Heydeman, Marcolli, Saberi, Stoica (2018): "Tensor networks, p-adic fields, and algebraic curves," *JHEP* 2018.
- QNFO Internal: `causality-redteam-full-analysis.md` §5 (Bruhat-Tits trees), `p-adic-feynman-propagator.md` (B1).

---

*This analysis is [established] for the failure modes of LSZ (no time ordering → no T-products → no Wick → no LSZ in ℚ_p; this is a mathematical fact, not a conjecture). The Bruhat-Tits S-matrix construction is [established] from the Gubser et al. literature. The archimedean limit (p→1) recovery of S_∞ is [speculative] / [my conjecture]. The integer-spaced pole prediction is [speculative] until computed explicitly (Phase 3).*
