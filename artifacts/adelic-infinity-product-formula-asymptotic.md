# Adelic Infinity and the Product Formula: Asymptotics, Hilbert's Hotel, and Completion-Dependent Notions of the Infinite

> **Workstream D2.1 | Cross-Cutting — Philosophical/Mathematical Bridge**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `product-formula-constraint-engine.md` (D2), `non-cosmetic-archimedean-predictions.md`
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** ARCHITECTURAL

---

## Executive Summary

Three questions are addressed:

1. **Is the product formula ∏_v |x|_v = 1 effectively an asymptote because there are infinitely many completions?** — NO. For rational x, the product is EXACT and FINITE (only finitely many non-trivial factors). For physical quantities involving π, the extension to non-principal idèles makes the product genuinely infinite, but the convergence is guaranteed by the restricted product condition ("almost all" factors are p-adic units, |·|_p = 1). The product formula is an exact constraint, not an asymptote — the "infinity" of completions is tamed by the restricted product topology.

2. **Does this abstract infinity support or oppose Hilbert's-Hotel-style infinity in physics?** — It SUPPORTS a restricted, structured infinity. Unlike Hilbert's Hotel (where ℵ₀ leads to paradoxes when applied to physical quantities), the adelic framework imposes the restricted product condition: "almost all" p-adic components are integral. This is a FINITENESS condition imposed on infinity — exactly the structure that prevents the divergences plaguing Archimedean QFT.

3. **Similarities and differences between adelic infinity and Archimedean/Cartesian infinity?** — Both are completions of ℚ, but they differ in connectedness (ℝ is a continuum; ℚ_p is totally disconnected), ordering (ℝ is ordered; ℚ_p is not), the behavior of "more" (|n| grows with n in ℝ; |n|_p shrinks in ℚ_p), and the regulation of UV divergences (ℝ-based QFT is UV-divergent; p-adic QFT on trees is UV-finite). The Archimedean infinity is the UNIQUE unrestricted, ordered, connected completion — and this uniqueness (Ostrowski's theorem) explains why time, causality, and the continuum are Archimedean-only phenomena.

---

## 1. The Product Formula — Finite Product, Infinite Places

### 1.1 The Rational Case: Exact, Finite

For any non-zero x ∈ ℚ:

```
|x|_∞ × ∏_p |x|_p = 1
```

Write x = a/b with a,b coprime. Then:

```
|x|_∞ = |a/b| (ordinary absolute value)
|x|_p = p^{ord_p(b) − ord_p(a)}
```

For any prime p that does NOT divide a or b: ord_p(a) = ord_p(b) = 0, so |x|_p = p⁰ = 1.

**There are only finitely many primes dividing a or b.** Therefore, |x|_p = 1 for ALL BUT FINITELY MANY p. The infinite product REDUCES to a finite product:

```
|x|_∞ × ∏_{p|a or p|b} p^{ord_p(b) − ord_p(a)} = |a/b| × ∏_{p|a} p^{-ord_p(a)} × ∏_{p|b} p^{ord_p(b)} = 1
```

The "infinity" of completions is a RED HERRING for rational numbers — it's always a finite product. There is no asymptote, no limit, no convergence question. [established]

### 1.2 The Transcendental Case: The Real Problem

For physical quantities involving π (like σ̂_∞ = π²/60), the situation changes radically. π is transcendental — it is NOT a rational number. The product formula as stated for principal adeles (elements of ℚ embedded diagonally) does not directly apply.

**The proper mathematical framework:** The idèle group J_ℚ. An idèle a = (a_v) is a tuple with a_v ∈ ℚ_v^× for each place v, satisfying:

```
|a_v|_v = 1  for all but finitely many v    [RESTRICTED PRODUCT CONDITION]
```

The **idèle norm** is ∥a∥ = ∏_v |a_v|_v. This product is WELL-DEFINED because almost all factors are 1 — it is effectively a finite product.

For a principal idèle (x ∈ ℚ^× embedded diagonally): ∥x∥ = 1 (the product formula).
For a non-principal idèle: ∥a∥ may be any positive rational number.

**The physical claim [speculative]:** Dimensionless physical constants like σ̂ = π²/60 are the ∞-place components of NON-PRINCIPAL idèles. Their p-adic components σ̂_p are p-adic numbers (elements of ℚ_p^×, typically rational numbers in ℚ_p). The idèle norm:

```
∥σ̂∥ = σ̂_∞ × ∏_p |σ̂_p|_p
```

is well-defined (almost all σ̂_p are p-adic units, so their factors are 1) and is NOT necessarily 1 — it characterizes the idèle class of σ̂.

### 1.3 Why It's NOT an Asymptote

The product ∏_p |σ̂_p|_p is NOT a limit or an asymptote. It is an EXACT product — convergent in the real numbers because:

1. Almost all factors are exactly 1 (by the restricted product condition)
2. The finitely many non-trivial factors multiply to a well-defined real number
3. There is no "remainder term," no "approximation error"

The appearance of an "infinite product" is misleading. It's a finite product dressed in the notation of an infinite one. **This is the central mathematical fact that makes adelic physics possible as an exact framework.** [established]

---

## 2. The Restricted Product — Taming Infinity

### 2.1 What "Restricted Product" Means

The adele ring A_ℚ is the RESTRICTED product:

```
A_ℚ = ℝ × ∏'_p ℚ_p
```

where ∏'_p means: an element a = (a_∞, a_2, a_3, ...) belongs to A_ℚ if and only if a_p ∈ ℤ_p (the p-adic integers) for ALL BUT FINITELY MANY p.

**This is a FINITENESS condition imposed on an infinite product.** It says: you cannot have "interesting" behavior at infinitely many places simultaneously. At almost all primes, the component must be an integer — bounded, regular, non-singular. [established]

### 2.2 Physical Interpretation

The restricted product condition has a direct physical meaning:

```
"For almost all primes p, the physical observable is a p-adic unit — 
 it carries no p-adic charge, no singular behavior, no special structure."
```

The primes that DO carry non-trivial structure are the "active primes" — a FINITE set. For the completion-failures framework, the active primes are small: p = 2, 3, 5, and possibly a few more. At all larger primes, the physics is "trivial" (the p-adic component is a unit, |σ̂_p|_p = 1).

**This is the exact opposite of Hilbert's Hotel.** In Hilbert's Hotel:
- Every room has a guest (infinitely many non-trivial entities)
- Moving guests creates paradoxes (ℵ₀ + 1 = ℵ₀)
- There is no "almost all" condition — every room matters

In the adelic restricted product:
- Almost all places are trivial (|·|_p = 1)
- Only finitely many places carry structure
- The infinite tail is "frozen" — it contributes nothing

**The restricted product is a FINITENESS PRINCIPLE imposed on infinity. It prevents the paradoxes that arise when infinity is treated as "unrestricted addition."** [established]

### 2.3 The Adelic UV Completion

This has a direct connection to UV divergences in QFT:

| Framework | UV Behavior | Why |
|:----------|:-----------|:----|
| Archimedean (ℝ) QFT | UV-divergent — loop integrals diverge as k → ∞ | ℝ has arbitrarily small distances; the continuum allows infinite resolution |
| p-adic QFT on Bruhat-Tits tree | UV-FINITE — tree has minimum edge length | The tree is discrete; the Laplacian has a gap; no short-distance singularities |
| Adelic (all places) | UV-finite at p-adic places; ∞-place acquires p-adic cutoff | Product formula links ∞-place to p-adic places; the restricted product provides natural UV regularization |

**The Archimedean UV divergences are a consequence of unrestricted infinity — the continuum allows modes at arbitrarily high momentum.** The p-adic places, being totally disconnected and having minimum distance (the tree edge), do NOT have this problem. The adelic framework, by combining both, may provide a natural UV completion: the ∞-place gets regularized by its coupling to the p-adic places through the product formula. [speculative]

---

## 3. Three Notions of Infinity

### 3.1 Archimedean/Cartesian Infinity — The Continuum

**Geometry:** ℝ — connected, ordered, smooth. The "real line" extends infinitely in both directions.

**Key properties:**
1. **Uncountable** (cardinality 2^ℵ₀) — the continuum
2. **Connected** — any two points can be joined by a continuous path
3. **Ordered** — a total order compatible with field operations
4. **Archimedean** — for any x > 0, there exists n ∈ ℕ with nx > 1 ("the small accumulates to the large")
5. **No minimum distance** — points can be arbitrarily close (ε → 0)

**Physical manifestation:** Spacetime as a smooth manifold. Limits (t → ∞, ε → 0). The iε prescription. Renormalization (counterterms cancel UV divergences). The concept of "arbitrarily large" and "arbitrarily small."

### 3.2 Hilbert's Hotel Infinity — Countable Addition

**Set-theoretic:** ℕ = {0, 1, 2, ...} with cardinality ℵ₀.

**Key properties:**
1. **Countable** — can be enumerated
2. **Discrete** — no notion of "closeness" beyond identity
3. **Well-ordered** — every non-empty subset has a least element
4. **Paradoxical under addition:** ℵ₀ + 1 = ℵ₀, ℵ₀ + ℵ₀ = ℵ₀ — addition does not increase cardinality
5. **No intrinsic metric** — all distinctions are qualitative (set membership), not quantitative (distance)

**Physical manifestation:** Quantum states in Fock space (countable basis). Energy levels of the harmonic oscillator (discrete spectrum). The "particle number" operator. Lattice models (countably infinite sites).

**Hilbert's Hotel paradox:** If every room is full and you add one guest, you can still accommodate them by shifting everyone. This shows that "∞ + 1 = ∞" is not a physical conservation law — it's a set-theoretic property that does NOT translate to physical quantities (energy, particle number, volume) where addition has operational meaning.

### 3.3 Adelic Infinity — Restricted Product

**Arithmetic:** A_ℚ = ℝ × ∏'_p ℚ_p with the restricted product topology.

**Key properties:**
1. **Product of completions** — each place is a local field (ℝ or ℚ_p)
2. **Restricted:** almost all components are integral (in ℤ_p)
3. **Not connected, not ordered overall** — but contains the ordered ℝ as a factor
4. **Locally compact** — supports harmonic analysis (adelic Fourier transform, Tate's thesis)
5. **Product formula binds the places** — ∏ |x|_v = 1 for principal adeles

**Physical manifestation:** The adelic framework for physics. Each completion ℚ_v supports its own "physics" (Archimedean QFT at the ∞-place, p-adic QFT at finite places). The product formula constrains observables across places. The restricted product ensures UV finiteness.

### 3.4 Comparison Table

| Property | Archimedean (ℝ) | Hilbert's Hotel (ℕ) | Adelic (A_ℚ) |
|:---------|:---------------|:-------------------|:-------------|
| Cardinality | 2^ℵ₀ (uncountable) | ℵ₀ (countable) | 2^ℵ₀ (uncountable) |
| Connected? | YES | NO (discrete) | NO (product of disconnected + connected) |
| Ordered? | YES (total order) | YES (well-order) | NO (only the ℝ factor is ordered) |
| Has metric? | YES (|x−y|) | YES (discrete metric) | YES (product metric from each place) |
| Minimum distance? | NO (ε → 0) | YES (distance 1) | MIXED (NO at ∞-place; YES at finite places — tree edges) |
| "More = bigger"? | YES (|n| grows with n) | NO (cardinality doesn't distinguish finite from infinite addition) | MIXED (YES at ∞-place; NO at p-adic — |pⁿ|_p = p^{−n} shrinks as n grows) |
| UV behavior | Divergent | N/A (no continuum to diverge in) | REGULATED (p-adic places are UV-finite; ∞-place coupled to them) |
| Product formula | N/A (only one place) | N/A (not a field) | ∏_v |x|_v = 1 — EXACT constraint across all places |

---

## 4. "More Is Bigger" — The Archimedean Exception

### 4.1 The Intuition That Fails Everywhere Else

In ℝ: if n > m as integers, then |n| > |m|. The usual absolute value GROWS with the size of the number. This seems obvious — until you realize it's a SPECIAL PROPERTY of the Archimedean absolute value.

In ℚ_p: |p|_p = 1/p (smaller than 1), |p²|_p = 1/p² (even smaller), |p^n|_p → 0 as n → ∞. Numbers with HIGHER powers of p become p-adically SMALLER.

**The Archimedean intuition — "more is bigger" — is the EXCEPTION, not the rule.** Among all completions of ℚ:
- 1 completion (ℝ) satisfies "more is bigger"
- Infinitely many completions (ℚ_p for each p) satisfy "more (powers of p) is smaller"

### 4.2 Physical Consequences

This inversion has physical consequences:

| Phenomenon | Archimedean Interpretation | p-Adic Interpretation |
|:-----------|:--------------------------|:---------------------|
| High momentum (k → ∞) | Short distances (UV) → divergences | Large |k|_p = p^{large} → SMALL in p-adic norm → finite contribution |
| Large times (t → ∞) | Asymptotic states defined | t with large |t|_p is p-adically SMALL — no "large time" limit |
| Many particles (N → ∞) | Thermodynamic limit | N with large p-adic norm is small — not a meaningful "large N" |
| High loop order (L → ∞) | Perturbation theory breaks down | p-adic diagrams at high order may converge faster (p-adic rational functions) |

**The Archimedean divergences are consequences of the "more is bigger" intuition being taken as universal, when it is actually completion-specific.** [speculative]

---

## 5. Does Adelic Infinity Support or Oppose Physical Infinity?

### 5.1 The Case FOR: Adelic Infinity as Structured Finiteness

The restricted product condition makes adelic infinity PHYSICALLY VIABLE in a way that Hilbert's Hotel infinity is not:

1. **Only finitely many places are "active"** — energy, complexity, information are concentrated at a finite set of primes
2. **The product formula is an exact constraint, not an asymptotic limit** — no need to take limits or truncate
3. **UV finiteness at p-adic places** — the tree structure provides natural short-distance regularization
4. **The ∞-place is unique** — Ostrowski's theorem selects ℝ as the only ordered, connected completion. There is exactly ONE place where "time" and "causality" and "continuum" make sense.

**The adelic framework SUPPORTS physical infinity by rendering it STRUCTURED rather than paradoxical.**

### 5.2 The Case AGAINST: Infinity as Artifact of Completion

The alternative view: "infinity" itself is an artifact of the Archimedean completion. In the p-adic completions:
- There is no "infinitely large" (the p-adic absolute value is bounded on ℤ_p)
- There is no "infinitely small" (the tree has minimum edge length)
- The "point at infinity" in ℙ¹(ℚ_p) = ℚ_p ∪ {∞} is a single point — not a continuum of directions

**If physics is fundamentally adelic, then "infinity" — both the infinitely large and the infinitesimally small — may be Archimedean-only concepts with no adelic analog.** This does not mean infinity is "wrong" — it means infinity is a FEATURE of one particular completion that does not generalize to the full adelic structure. [PHILOSOPHY] [my conjecture]

### 5.3 Resolution: Infinity Is Completion-Dependent

The three notions of infinity are not competitors — they are different STRUCTURES, each appropriate to its own completion:

| Completion | Appropriate Infinity | Physical Role |
|:-----------|:-------------------|:--------------|
| ℝ (∞-place) | The continuum — uncountable, ordered, connected | Spacetime, causality, smooth manifolds, limits |
| ℚ_p (p-adic places) | The Bruhat-Tits tree — infinite (p+1)-regular, partial order, discrete | UV regularization, hierarchical structure, algebraic scattering |
| A_ℚ (adelic) | Restricted product of all completions — binds them via product formula | The full theory: ∞-place provides spacetime; p-adic places provide UV completion; product formula constrains observables |

**The adelic framework does not abolish infinity — it DISTRIBUTES it across completions, with each completion contributing its own notion of "the infinite" appropriate to its topology.** [speculative]

---

## 6. The Hardest Question: Truncation vs. Completion

### 6.1 If the Product Is Exact, Why Does It Feel Like an Asymptote?

The product formula ∏_v |x|_v = 1 is exact for rational x. For physical quantities involving transcendental numbers, the extension to non-principal idèles is a CONJECTURE — not yet proven to be the correct mathematical framework.

The asymptotic question arises because:
1. We don't know which primes are "active" for a given physical observable
2. We don't know the idèle class of physical constants (what is ∥σ̂∥?)
3. We cannot compute σ̂_p for individual primes without a full p-adic QFT
4. The product over ALL primes seems to require knowing σ̂_p for every p

**But this is not an asymptotic problem — it's an epistemological one.** The product formula IS exact (as a mathematical identity for principal adeles, or as the definition of the idèle norm for non-principal ones). Our INABILITY to compute individual factors does not make the product an asymptote — it makes the computation incomplete.

**Analogy:** The Riemann zeta function ζ(s) = ∑_{n=1}^∞ n^{−s} is an exact definition, not an asymptotic series. The fact that we cannot compute ζ(3) in closed form does not make ζ(3) an "asymptote." Similarly, the product formula is an exact constraint — our incomplete knowledge of the factors is a computational limitation, not a structural one. [established]

### 6.2 The "Only Active Primes Matter" Principle

The restricted product condition guarantees that |σ̂_p|_p = 1 for all but finitely many p. Therefore:

```
∥σ̂∥ = σ̂_∞ × ∏_{p ∈ S} |σ̂_p|_p
```

where S is the FINITE set of "active" primes. The product is genuinely finite — not as an approximation, but as an exact consequence of the restricted product topology.

**The challenge is to identify S.** For the completion-failures framework, the candidates are:
- p = 2: smallest prime, most non-trivial topology (Bruhat-Tits tree is 3-regular)
- p = 3: appears in physical construction via the propagator pole structure
- p = 5: appears in Stefan-Boltzmann through zeta regularization
- p = ∞: the Archimedean place — the only ordered completion

**For any p ∉ {2, 3, 5}: |σ̂_p|_p = 1 unless there is a specific physical reason for that prime to be active.** This is a falsifiable claim — if Phase 3 computation reveals non-trivial structure at p = 7, 11, etc., the "small primes only" hypothesis is wrong. [speculative]

---

## 7. Connection to the Bruhat-Tits Framework

### 7.1 The Tree at Each Prime

Each prime p has its own Bruhat-Tits tree T_p — an infinite (p+1)-regular tree. The tree's boundary is ℙ¹(ℚ_p). Physics on ℚ_p is formulated as physics on T_p.

**The product formula over all primes corresponds to the product over all trees:**

```
∥σ̂∥ = σ̂_∞ × ∏_p |σ̂_p|_p = 1    [if principal]
```

Each |σ̂_p|_p is computed from the Witten diagram on T_p. The ∞-place factor σ̂_∞ is computed from the Archimedean QFT.

**The restricted product condition says: for all but finitely many p, the Witten diagram on T_p contributes trivially (|σ̂_p|_p = 1).** This means the scattering amplitude on T_p for large p is the "free" amplitude (no interaction).

### 7.2 Why Large Primes Are Trivial

For large p, the Bruhat-Tits tree T_p is highly branched (p+1 neighbors per vertex). The Green's function on a highly branched tree approaches the free-field propagator — interactions are suppressed by the large branching factor. The p-adic coupling g_p → 0 as p → ∞.

**This is the adelic analog of asymptotic freedom:** at large p (which corresponds to small p-adic distance — "UV" in the p-adic sense), the theory becomes free. The non-trivial physics is concentrated at the smallest primes (p = 2, 3, 5), where the tree is least branched and interactions are strongest.

This is the INVERSE of Archimedean asymptotic freedom (where the theory becomes free at high MOMENTUM, i.e., short real distances). In the p-adic case, the theory becomes free at large PRIME, which corresponds to a different notion of "scale." [my conjecture]

---

## 8. Synthesis: The Five Infinities of Physics

Physics as currently formulated uses (at least) five distinct notions of "infinity," only some of which are compatible:

| Infinity | Domain | Status in Adelic Framework |
|:---------|:-------|:--------------------------|
| **Continuum infinity** (ℝ) | Spacetime, limits, smoothness | RETAINED at ∞-place only — the UNIQUE ordered completion |
| **Countable infinity** (ℕ) | Fock space, energy levels, lattice sites | RETAINED — discrete spectrum survives |
| **UV infinity** (k → ∞) | Loop integral divergences | REGULARIZED — p-adic places provide tree cutoff; no UV divergences on T_p |
| **Adelic infinity** (∏'_v ℚ_v) | Product formula, idèle class, restricted product | THE FRAMEWORK — binds all completions with finiteness condition |
| **Transfinite infinity** (set theory, cardinalities) | Hilbert's Hotel, continuum hypothesis | PHYSICALLY IRRELEVANT — cardinal arithmetic does not constrain measurable quantities |

The adelic framework replaces "infinity as an unbounded quantity" with "infinity as a restricted product of finitely many active structures." This is not a weakening of the mathematical framework — it is a STRENGTHENING, because it eliminates the UV divergences that plague Archimedean-only physics. [speculative]

---

## 9. Falsifiability

### 9.1 The "Active Primes Only" Hypothesis

**Claim:** Only finitely many primes (candidates: p = 2, 3, 5) contribute non-trivial factors to physical observables.

**Falsification:** If Phase 3 computation reveals that |σ̂_p|_p ≠ 1 for primes p > 5 (e.g., p = 7, 11, 13), the "small primes only" hypothesis is wrong. The active set S is larger than {2, 3, 5}.

**If confirmed:** The product formula reduces to a genuinely finite constraint involving 3–5 primes, making the theory computationally tractable and directly falsifiable.

### 9.2 The "Product Formula Is Exact" Hypothesis

**Claim:** The idèle norm ∥O∥ of every dimensionless physical observable is a well-defined rational number (not transcendental), characterizing the observable's idèle class.

**Falsification:** If the computed ∥σ̂∥ is irrational (e.g., involving π or other transcendentals that don't cancel), the framework as currently formulated is inconsistent — the product formula requires rational norms.

**If confirmed:** Each physical constant carries an "adelic charge" — a rational number ∥O∥ that constrains its values across completions. This is a NEW KIND OF CONSERVATION LAW. [my conjecture]

### 9.3 The "Large-p Triviality" Hypothesis

**Claim:** For primes p → ∞, the p-adic coupling g_p → 0 and all p-adic observables approach their free-field values (|O_p|_p = 1).

**Falsification:** If Missarov-type β-function coefficients or Bruhat-Tits Mellin amplitudes do NOT approach trivial values for large p, the restricted product condition is violated — infinitely many primes would be active, and the product formula would diverge.

**If confirmed:** The adelic framework has a natural UV completion: large-p physics is free, and only small-p physics is interacting. This is an adelic analog of asymptotic freedom.

---

## 10. Decision Log

| Decision | Rationale |
|:---------|:----------|
| The product formula is EXACT, not asymptotic — the "infinity" of completions is tamed by the restricted product | For rational x, the product is literally finite (only finitely many non-trivial factors). For non-principal idèles, convergence is guaranteed by the restricted product topology. |
| Adelic infinity SUPPORTS physical application (unlike Hilbert's Hotel infinity) | The restricted product condition imposes a finiteness principle — "almost all places are trivial" — that prevents paradoxes and UV divergences |
| Archimedean infinity is the UNIQUE unrestricted completion — explaining why time, causality, and the continuum are ∞-place-only phenomena | Ostrowski's theorem: ℝ is the only connected, ordered completion of ℚ |
| The "more is bigger" intuition is Archimedean-only | In ℚ_p, higher powers of p make numbers p-adically SMALLER — the intuition inverts |
| Large primes are physically trivial (small-p dominance) | As p → ∞, the Bruhat-Tits tree becomes highly branched, suppressing interactions → g_p → 0 |
| Five distinct notions of infinity operate in physics, only some compatible with the adelic framework | Continuum + countable + UV + adelic + transfinite — the adelic framework unifies the first four while rendering transfinite infinity physically irrelevant |

---

## 11. References

- Cassels & Fröhlich (1967), *Algebraic Number Theory*, Chapter II (adèles, idèles, restricted product, product formula).
- Tate (1950), "Fourier analysis in number fields and Hecke's zeta-functions" (Tate's thesis). [Adelic Fourier analysis; the restricted product as the natural domain for harmonic analysis]
- Neukirch (1999), *Algebraic Number Theory*, §III.1 (Ostrowski's theorem and product formula).
- Serre (1980), *Trees*, §II.1 (Bruhat-Tits tree, PGL(2, ℚ_p), boundary at infinity).
- Gubser et al. (2017), "p-adic AdS/CFT," *Commun. Math. Phys.* 352, 1019. [Witten diagrams on Bruhat-Tits tree]
- Missarov (1989), "p-adic φ⁴ theory," *Theor. Math. Phys.* 79, 580. [Large-p behavior of p-adic coupling — asymptotically free as p → ∞]
- QNFO Internal: `product-formula-constraint-engine.md` (D2), `causality-redteam-full-analysis.md` (C1-RT).

---

*The mathematical content (restricted product, product formula for principal adeles, idèle norm) is [established] from standard algebraic number theory. The extension to physical constants as non-principal idèles is [speculative]. The "active primes only" hypothesis (S = {2, 3, 5}) is [my conjecture]. The large-p triviality claim (g_p → 0 as p → ∞) is [speculative] but grounded in Missarov's analysis of the hierarchical model. The unification of five notions of infinity under the adelic framework is [PHILOSOPHY] — it is a structural claim about the architecture of physical theories, not a mathematical theorem.*
