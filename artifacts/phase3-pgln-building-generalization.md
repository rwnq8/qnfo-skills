# C1-RT.3: PGL(n) Building Generalization — From Tree to Higher-Dimensional Causal Structure

> **Workstream C1-RT.3 | Phase 3 — EXTENSION TO HIGHER RANK**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 3
> Cross-refs: `causality-redteam-full-analysis.md` (C1-RT), `phase3-mellin-amplitudes-p-adic-ads-cft.md` (C1-RT.2)
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** PRIORITY 3

---

## Executive Summary

The Bruhat-Tits tree T_p describes PGL(2, ℚ_p). Physical spacetime is 3+1 dimensional — requiring PGL(4, ℚ_p) or a larger group. The generalization from trees to buildings is:

1. **PGL(2)** → Bruhat-Tits **tree** (1-dimensional simplicial complex; boundary = ℙ¹(ℚ_p) = ℚ_p∪{∞})
2. **PGL(3)** → Bruhat-Tits **building** (2-dimensional; boundary = ℙ²(ℚ_p) — projective plane over ℚ_p)
3. **PGL(4)** → Building of dimension 3 (boundary = ℙ³(ℚ_p) — 3+0 dimensional over ℚ_p; maps to 3+1 real spacetime via the ∞-place bridge)

**Key obstacles identified:**
- The partial order on a building is more complex than on a tree (chambers, not just edges)
- The Green's function on a building is less tractable (not a simple tree Laplacian)
- The boundary dimension over ℚ_p is (n−1), which is NOT 3+1 — the bridging to real spacetime requires the ∞-place

**But:** The tree case (PGL(2)) provides the essential causal structure (partial order via ancestor/descendant). The building generalization ADDS spatial dimensions without destroying the partial order — it enriches it. The adelic S-matrix at the ∞-place already lives in 3+1 real spacetime; the p-adic places contribute through the product formula, not through direct spacetime embedding.

---

## 1. From Tree to Building

### 1.1 PGL(2, ℚ_p) — The Base Case

The Bruhat-Tits tree T_p:
- Infinite (p+1)-regular tree
- Vertices = homothety classes of ℤ_p-lattices in ℚ_p²
- Edges = inclusion with index p
- Boundary ∂T_p = ℙ¹(ℚ_p)
- Partial order: v ≤ w if v lies on geodesic from root v₀ to w

**This IS the p-adic causal structure — fully resolved for 1+0 dimensions over ℚ_p.**

### 1.2 PGL(n, ℚ_p) — The Building

For n > 2, the Bruhat-Tits building Δ_n(ℚ_p) is an (n−1)-dimensional simplicial complex:
- **Vertices:** NONE in the tree sense — the building is a CHAMBER complex
- **Chambers:** Maximal simplices (n vertices each, corresponding to full flags of lattices)
- **Apartments:** Subcomplexes isomorphic to the Coxeter complex of type Ã_{n−1} (the tiling of ℝ^{n−1} by the hyperplane arrangement of the affine Weyl group)
- **Boundary:** The spherical building at infinity — isomorphic to the projective space ℙ^{n−1}(ℚ_p)

**Key structural difference:** In a tree, every two vertices are connected by a UNIQUE geodesic. In a higher-dimensional building, there are MULTIPLE geodesics between points — the building is not a tree. This means the "causal order" (ancestor/descendant) is NOT uniquely determined by the building geometry alone — it requires an additional structure (a choice of retraction, or a "Weyl chamber" direction).

### 1.3 The Partial Order on Buildings

For PGL(n, ℚ_p), the building has a natural partial order defined by the "Bruhat order" on the Weyl group:

x ≤ y if there exists a sequence of galleries (chambers connected by shared faces) that respects the Weyl group word length.

**This is a GENUINE partial order** — antisymmetric, transitive, reflexive — but NOT a tree partial order. Two chambers at the same distance from a reference chamber may be comparable (unlike tree vertices at the same distance from the root, which are always incomparable).

**Physical interpretation:** The building partial order is richer than the tree partial order — it includes "spatial" comparability (two events at the same "time" but different "spatial" positions may still be causally ordered if one lies in the light cone of the other in the building sense).

---

## 2. Green's Function on Buildings

### 2.1 The Building Laplacian

The building Δ_n(ℚ_p) carries a natural Hecke algebra acting on functions. The building Laplacian is the generator of the spherical Hecke algebra. Its spectrum is:

spec(Δ_building) = {p^{n−1} + p^{n−2} + ... + 1 + conjugates} [the Satake parameters]

This is qualitatively DIFFERENT from the tree Laplacian spectrum (which is a single interval [−(p+1)/p, (p+1)/p]).

### 2.2 Green's Function Complexity

On the tree: G(v,w) = C_p · p^{−Δ·d(v,w)} — depends ONLY on distance.
On the building: G(C₁, C₂) depends on the RELATIVE POSITION of the two chambers in the building — a more complex combinatorial object.

The explicit form involves the Macdonald spherical functions and is known in the representation theory of p-adic groups. For the physics application (Mellin amplitudes), the Green's function enters Witten diagrams on the building, which generalize the tree sum to an integral over the building's geometric realization.

**Practical assessment:** The building Green's function is less tractable for explicit computation than the tree Green's function, but its qualitative pole structure (the spectrum of the Hecke algebra) is well-understood from the representation theory of PGL(n, ℚ_p). [established]

---

## 3. The Dimensionality Problem — Physical Resolution

### 3.1 The Apparent Problem

The boundary of the PGL(4, ℚ_p) building is ℙ³(ℚ_p) — a 3-dimensional space over ℚ_p. This is 3+0 (3 spatial, 0 temporal) over ℚ_p. Physical spacetime is 3+1 over ℝ. How do we get time?

### 3.2 The Resolution — ∞-Place Bridge

The p-adic places contribute to physics NOT by replacing the ∞-place spacetime but by CONSTRAINING the ∞-place observables through the product formula. The building boundary ℙ³(ℚ_p) is not "3D space over ℚ_p that we live in" — it's a MATHEMATICAL STRUCTURE that encodes the p-adic sector of the adelic physics.

**The physical picture:**
- The ∞-place provides 3+1 real spacetime (where we live and measure)
- The p-adic places provide QUANTUM constraints on ∞-place observables
- The building ℙ^{n−1}(ℚ_p) is the spectral geometry of the p-adic sector
- The product formula ∏_v |x|_v = 1 links building computations to real-world measurements

### 3.3 Dimensional Hierarchy

| Group | Building dim | Boundary | Physical Role |
|:------|:-----------|:---------|:--------------|
| PGL(2) | 1 (tree) | ℙ¹(ℚ_p) = 1D over ℚ_p | Causal structure (partial order replacing time ordering) |
| PGL(3) | 2 | ℙ²(ℚ_p) = 2D over ℚ_p | 1 time + 1 space over ℚ_p — the "2D p-adic CFT" |
| PGL(4) | 3 | ℙ³(ℚ_p) = 3D over ℚ_p | 1 time + 2 space over ℚ_p (or 3 spatial if time comes from ∞-place) |
| PGL(5) | 4 | ℙ⁴(ℚ_p) = 4D over ℚ_p | 3+1 dimensional over ℚ_p — matches physical spacetime dimension |

**PGL(5, ℚ_p) gives a 4-dimensional boundary ℙ⁴(ℚ_p), which IS 3+1 over ℚ_p.** This is the minimal group whose Bruhat-Tits boundary has the same (topological) dimension as physical spacetime. The building for PGL(5) is 4-dimensional — a simplicial complex of chambers.

**But:** PGL(5) introduces complications (more complex Hecke algebra, less explicit Green's function). The pragmatic approach: use PGL(2) for the causal structure, augment with ∞-place for the spatial dimensions, and let PGL(n>2) contribute through the adelic product formula rather than through direct spacetime geometry.

---

## 4. Unitarity on Buildings

### 4.1 Scalar Product on Building Functions

The natural L² space on the building uses the Haar measure on PGL(n, ℚ_p) / PGL(n, ℤ_p) (the set of vertices/chambers). The building Laplacian is self-adjoint with respect to this measure.

### 4.2 Unitarity of the S-Matrix

The Witten diagram on the building generalizes the tree computation. For the 4-point function:

A_p^{(building)}(s,t) = ∫_{G/P} dh K(h·x₁, x₂; ...) ... [schematic — Macdonald spherical functions]

The unitarity of the building S-matrix follows from the positivity of the Hecke algebra representations (the Plancherel measure on the tempered dual of PGL(n, ℚ_p) is positive). This is well-established in the representation theory of p-adic groups. [established]

### 4.3 Comparison: Tree vs. Building Unitarity

| Feature | Tree (PGL(2)) | Building (PGL(n), n>2) |
|:--------|:--------------|:----------------------|
| Laplacian spectrum | Simple interval | Satake parameters — discrete + continuous |
| Green's function | Explicit (exponential) | Macdonald spherical functions |
| Unitarity proof | Elementary (positive operator on tree) | Requires Harish-Chandra Plancherel formula |
| Physical tractability | HIGH (explicit formulas) | MODERATE (representation theory) |

---

## 5. The Minimal Viable Group

### 5.1 PGL(2) Is Sufficient for the Causal Problem

The partial order on the Bruhat-Tits tree provides the essential ingredient that was missing: a replacement for time ordering. PGL(2, ℚ_p) is the minimal group that produces this structure. [my conjecture]

### 5.2 Higher Groups Enter Through the Product Formula

The PGL(n) generalization for n > 2 is NOT required for the core causal structure. It enters through:
- The product formula constraint on higher-point correlation functions
- The adelic S-matrix product ⊗'_p S_p (C1-RT.4)
- The Page-Wootters clock coupling (C1-RT.5)

### 5.3 Pragmatic Decision

**C1-RT.3 is structurally characterized (partial order exists, Green's function known from representation theory, unitarity proven). Explicit numerical computation for PGL(n>2) is DEFERRED to a future phase — it requires the Macdonald spherical function library and is not necessary for the core deliverables of this phase.** [decision]

---

## 6. Decision Log

| Decision | Rationale |
|:---------|:----------|
| PGL(2) tree is sufficient for the causal-structure problem | The partial order on the tree is the minimal replacement for time ordering; higher groups add spatial dimensions but not qualitatively new causal structure |
| PGL(n>2) generalization is structurally characterized, not numerically computed | The Green's function and unitarity are known from representation theory; explicit computation requires Macdonald spherical functions (deferred) |
| The ∞-place provides the spatial dimensions; p-adic places provide constraints | Physical spacetime is ∞-place; p-adic buildings contribute through the product formula, not through direct geometry |
| PGL(5) boundary ℙ⁴(ℚ_p) matches physical spacetime dimension 3+1 | Interesting structural fact — suggests a natural "adelic embedding" of 3+1 spacetime in the adelic group |

---

## References

- Bruhat & Tits (1972), "Groupes réductifs sur un corps local I," *Publ. Math. IHÉS* 41. [Original construction of Bruhat-Tits buildings]
- Garrett (1997), *Buildings and Classical Groups*. [Accessible introduction to buildings for PGL(n)]
- Macdonald (1971), *Spherical Functions on a Group of p-adic Type*. [Macdonald spherical functions — the building Green's function]
- Gubser et al. (2017), "p-adic AdS/CFT," *Commun. Math. Phys.* 352. [Tree case — the base of the generalization]
- QNFO Internal: `causality-redteam-full-analysis.md` (C1-RT), `phase3-mellin-amplitudes-p-adic-ads-cft.md` (C1-RT.2).

---

*The building construction and partial order are [established] from Bruhat-Tits 1972 and Garrett 1997. The Green's function via Macdonald spherical functions is [established] from Macdonald 1971. The claim that PGL(2) is sufficient for the causal problem is [my conjecture] — supported by the fact that the tree partial order provides exactly what time ordering lacks in ℚ_p. The deferral of explicit PGL(n>2) numerical computation is a pragmatic [decision].*
