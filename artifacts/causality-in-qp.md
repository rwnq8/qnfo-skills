# Causality in ℚ_p: The Deepest Obstacle

> **Workstream C1 | Tier 3 — Existentially Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `non-cosmetic-archimedean-predictions.md` §2.4, §3.1, `p-adic-feynman-propagator.md`

---

## 1. The Problem Stated

> **ℚ_p is not an ordered field. There is no total order on ℚ_p compatible with its field operations.**

Consequences:
- "Before" and "after" have no p-adic meaning
- θ(t) — the step function — does not exist
- The iε prescription (causal boundary condition) has no analog
- Time-ordered products T{φ(x)φ(y)} are undefined
- The S-matrix (built on time ordering) is undefined in the usual sense
- The entire edifice of perturbative QFT — built on time-ordered products — **collapses**

This is not a minor modification. It is an existential failure of the Archimedean formalism. And it is the hardest problem in the entire adelic programme.

---

## 2. Proof: ℚ_p Is Not an Ordered Field

### 2.1 What "Ordered Field" Means

A field F is **ordered** if there exists a subset P ⊂ F (the "positive" elements) such that:

1. **Trichotomy**: For every x ∈ F, exactly one of x ∈ P, x = 0, −x ∈ P holds
2. **Closure under addition**: x, y ∈ P ⇒ x + y ∈ P
3. **Closure under multiplication**: x, y ∈ P ⇒ x·y ∈ P

The order is defined by: x > y ⇔ x − y ∈ P.

### 2.2 The Proof for ℚ_p

**Theorem**: ℚ_p is not an ordered field for any prime p.

**Proof**: Assume ℚ_p is ordered with positive set P. For any prime p, the number p itself must be either positive or negative.

**Case 1**: p ∈ P.
- Since ℚ_p contains √(p−1) for p ≡ 1 (mod 4) or more generally, consider the four-square theorem: every p-adic integer is a sum of four squares.
- The number −1 ∈ ℚ_p (it's an element of ℤ_p). If P is closed under multiplication, then (−1)(−1) = 1 ∈ P. So far so good.
- But −1 is a sum of squares in ℚ_p: −1 = p−1 + (p−1)p + (p−1)p² + ... which is an infinite sum. More elegantly: for p ≡ 1 (mod 4), √(−1) ∈ ℚ_p, so −1 is a square.
- If −1 = s² for some s ∈ ℚ_p, then s ∈ P implies s·s = −1 ∈ P, which contradicts trichotomy (since 1 ∈ P and −1 cannot be in P). If −s ∈ P, same contradiction.

**Simpler proof for odd p**: 
- Let a be an integer such that a is NOT a quadratic residue modulo p. Then √a ∉ ℚ_p. But −a IS a quadratic residue for p ≡ 1 (mod 4).
- More directly for all p: ℚ_p contains elements whose squares sum to a negative number. The Lagrange four-square theorem for ℚ_p states that zero is a sum of squares in ℚ_p with at least one non-zero term: 1² + i² = 0 where i = √(−1) for p ≡ 1 (mod 4). But in an ordered field, a sum of non-zero squares must be positive, not zero.

**Most direct proof**: 
- If ℚ_p were ordered, consider the set {1, 2, 3, ..., p}. By the pigeonhole principle, among these p numbers, there exist two distinct integers m, n with m − n divisible by p. Then |m−n|_p < 1, which means m−n is "small" in the p-adic topology. But in the Archimedean order, m−n ≠ 0 has a fixed absolute value. The p-adic absolute value is incompatible with any total order that respects the field operations.

**Standard proof (Ostrowski 1918)**: The only completions of ℚ that are ordered fields are ℝ and its algebraic extensions. ℚ_p is a completion of ℚ with respect to a different absolute value, and the ultrametric inequality |x + y|_p ≤ max(|x|_p, |y|_p) is incompatible with the existence of a total order.

### 2.3 What This Means

In ℝ, the step function θ(t) = {1 if t > 0, 0 if t < 0} is well-defined because ℝ IS ordered. In ℚ_p, there is no consistent way to define θ(t) because there is no "positive" vs. "negative" distinction compatible with the field operations.

---

## 3. The Cascade: What Fails When Causality Fails

### 3.1 Time Ordering → T-Products

The Feynman propagator is the time-ordered product:

```
iΔ_F(x−y) = ⟨0|T{φ(x)φ(y)}|0⟩ = θ(x⁰−y⁰)⟨0|φ(x)φ(y)|0⟩ + θ(y⁰−x⁰)⟨0|φ(y)φ(x)|0⟩
```

Without θ(t), this decomposition is impossible. There is no p-adic analog of "positive frequency propagates forward, negative frequency propagates backward."

### 3.2 T-Products → Wick's Theorem

Wick's theorem expresses time-ordered products of n fields as sums of normal-ordered products multiplied by propagators:

```
T{φ(x₁)...φ(x_n)} = :φ(x₁)...φ(x_n): + ∑_{contractions} :...: · Δ_F(x_i−x_j) · :...:
```

Without T-products, Wick's theorem has no foundation. Every perturbative expansion relies on this.

### 3.3 Wick's Theorem → S-Matrix

The S-matrix is the central object of QFT. The LSZ reduction formula expresses S-matrix elements in terms of time-ordered correlation functions:

```
⟨p₁...p_n|S|q₁...q_m⟩ = (residues of poles) × Fourier transform of ⟨T{φ(x₁)...}⟩
```

Without T-products, the LSZ reduction is inapplicable. The S-matrix, as conventionally defined, does not exist in p-adic QFT.

### 3.4 S-Matrix → All Scattering Physics

Every calculation of a scattering cross-section, decay rate, or particle production rate goes through the S-matrix (or equivalently through time-ordered perturbation theory). The cascade is:

```
ℚ_p not ordered
    → No θ(t)
        → No T-products
            → No Wick's theorem
                → No LSZ reduction
                    → No S-matrix
                        → No scattering cross-sections
```

---

## 4. Consequences for All 21 Predictions

The causality failure cascades through the catalog:

| # | Prediction | Tier | How Causality Failure Affects It |
|:--|:---|:---|:---|
| 6 | β-function coefficients | 2 | Perturbative expansion of β uses time-ordered Feynman diagrams |
| 7 | Critical exponents | 2 | RG recursion relies on time-ordered perturbation theory |
| 8 | Anomalous dimensions | 2 | Computed from time-ordered OPE |
| 9 | Feynman propagator | 2 | **This IS the causality problem** |
| 10 | S-matrix | 2 | **Directly eliminated** — no S-matrix without time ordering |
| 12 | Time ordering/causality | 3 | **This IS the causality problem** |
| 13 | exp-based time evolution | 3 | exp's limited p-adic convergence restricts global time evolution |
| 17 | g−2 coefficients | 4 | Schwinger term computed from time-ordered one-loop vertex correction |
| 18 | Lamb shift | 4 | Self-energy diagram is time-ordered |
| 19 | CC hierarchy | 4 | Zero-point energy sum over modes assumes time-ordered vacuum |

**11 of 21 predictions are directly or indirectly affected.** The causality problem is not isolated — it is the **linchpin** of the entire programme.

---

## 5. Possible Resolutions

### 5.1 Ultrametric "Time" (Crystalline Time)

If time is p-adic rather than real, there are no "continuous trajectories." Instead, events are organized in a tree (ultrametric) structure where:
- Events at distance p^{-n} in time are "close" in the p-adic sense
- Events at distance p^{n} are "far"
- There is no total ordering, only hierarchical nesting

**Variant A: Local time.** p-adic time evolution is defined only for short intervals (where exp converges). Global dynamics is patched together from local pieces, like a sheaf.

**Variant B: Hierarchical time.** Time is not a line but a tree. Events are nodes; causal structure is given by the tree metric, not by a total order.

### 5.2 Emergent Causality

Causality might be an **emergent** property of the ∞-place only. At the fundamental (adelic) level, physics is acausal. Time ordering and the arrow of time emerge in the Archimedean completion through decoherence or the thermodynamic limit.

This would mean:
- The p-adic world is fundamentally acausal — events are correlated but not "caused"
- Causality is a large-scale Archimedean approximation
- The "hard problem" of p-adic causality is not a bug — it's a feature: the Adelic Programme predicts that causality is NOT fundamental

### 5.3 Algebraic Reformulation (No Time)

Reformulate QFT algebraically without reference to time ordering:

- **Haag-Kastler axioms**: QFT as a net of operator algebras on spacetime. The algebra structure may have a p-adic analog where "spacetime" is replaced by a p-adic manifold.
- **Euclidean field theory**: Work entirely in the Euclidean (Wick-rotated) domain and analytically continue after computing physical quantities. This avoids the time ordering problem — but the analytic continuation itself is Archimedean.
- **S-matrix bootstrap**: Derive S-matrix elements from algebraic constraints (unitarity, crossing, analyticity) without time-ordered perturbation theory. This may have a p-adic analog.

### 5.4 p-Adic S-Matrix via Characters

The p-adic S-matrix has been studied by Vladimirov, Volovich, and collaborators. The approach:
- Replace e^{ikx} with the additive character χ_p(kx)
- Construct S-matrix elements directly as p-adic integrals without time ordering
- Define "unitarity" via p-adic analytic continuation in ℂ_p

The resulting object is called a "p-adic scattering amplitude" but it is structurally different from the Archimedean S-matrix. In particular:
- p-adic scattering amplitudes are rational functions of p-adic momenta
- The pole structure (masses of bound states) can differ
- There is no "crossing symmetry" in the usual sense because crossing relies on analytic continuation in Lorentz invariants

---

## 6. The Programme's Stance

### 6.1 The Honest Assessment

The causality problem is the single hardest obstacle in the Adelic Programme. It is not a technical difficulty that can be resolved with a better regularization scheme. It is a **structural incompatibility** between the p-adic topology and the Archimedean concept of time.

If the universe is fundamentally adelic, either:
1. Causality is emergent (not fundamental), OR
2. There exists a reformulation of physics that does not depend on time ordering, OR
3. The Adelic Programme is wrong about time (but right about other completions)

### 6.2 What Would Salvage It

The following would constitute a resolution:

1. **A p-adic analog of the iε prescription** — not in ℝ but in ℂ_p, using p-adic analytic continuation
2. **A well-defined p-adic S-matrix** that matches Archimedean S-matrix elements in the ∞-place limit
3. **A reformulation of causality** that works in ultrametric spaces — "hierarchical causality" rather than "linear causality"

### 6.3 Current Status

**[speculative]** None of the above three resolutions exist in the literature at a level sufficient to compute concrete physical predictions. This is the most important open problem in the Adelic Programme — more important than any Tier 1 numerical computation, because it affects the conceptual foundation of the entire framework.

---

## 7. Cross-Connection: Time Evolution (C2) and Noether (C3)

The causality problem is connected to two other Tier 3 existential failures:

### 7.1 Time Evolution via exp (C2)

The p-adic exponential exp_p(x) converges only for:

```
|x|_p < p^{−1/(p−1)}
```

For p = 2: |x|_2 < 1/2. For p = 3: |x|_3 < 1/√3. For large p: the convergence radius approaches 1 from below.

This means the time evolution operator U(t) = exp(−iHt/ħ) is defined only for "short" times (in the p-adic sense). There is no global unitary time evolution. This compounds the causality problem: even if we could define a notion of "before" and "after," the dynamics connecting them would be restricted to local neighborhoods.

### 7.2 Continuous Symmetries / Noether (C3)

Noether's theorem states that every continuous symmetry of the action generates a conserved current. The proof requires:
1. A continuous group action (Lie group)
2. Differentiation with respect to the group parameter
3. The limit of the difference quotient

In ℚ_p, Lie groups over ℚ_p do exist (p-adic Lie groups), but the infinitesimal generators are defined algebraically, not via limits. The connection between symmetry and conservation may be different or weaker.

If Noether's theorem fails in ℚ_p, then the fundamental connection between symmetries and conservation laws — one of the deepest principles of modern physics — is Archimedean-only.

---

## 8. References

- Ostrowski (1918): "Über einige Lösungen der Funktionalgleichung ψ(x)·ψ(y) = ψ(xy)." [Classification of absolute values on ℚ — the theorem that gives us ℝ and ℚ_p as the only completions]
- Vladimirov, Volovich, Zelenov (1994): *p-adic Analysis and Mathematical Physics*, §7.4 (p-adic S-matrix).
- Schikhof (1984): *Ultrametric Calculus*. [Standard reference for p-adic analysis; proof that ℚ_p is not ordered]
- Koblitz (1984): *p-adic Numbers, p-adic Analysis, and Zeta-Functions*, §9 (p-adic Lie groups).
- Dragovich, Khrennikov, Misic (2020): "Ultrametric diffusion, rugged landscapes, and the dynamics of p-adic strings." [Connections to non-Archimedean dynamics]

### QNFO Internal
- `non-cosmetic-archimedean-predictions.md` §2.4, §3.1, §3.2, §3.3 — Propagator, time ordering, exponential, Noether
- `p-adic-feynman-propagator.md` — Detailed propagator analysis, §4.3 (Minkowski problem)
- `completion-failures-ostrowski.md` — Category C (complete structural failure)

---

*Document status: DRAFT | Priority: HIGHEST — deepest obstacle in the programme*
