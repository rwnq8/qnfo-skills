# The p-Adic Feynman Propagator: Structural Analysis

> **Workstream B1 | Tier 2 — Structurally Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `non-cosmetic-archimedean-predictions.md` §2.4, `completion-failures-ostrowski.md`

---

## 1. Why the Propagator Matters

The Feynman propagator is the single most important object in perturbative QFT. It is:

- The Green's function of the free field equation: (□ + m²)Δ_F(x−y) = −iδ⁴(x−y)
- The building block of every Feynman diagram (internal lines)
- The carrier of causality: the iε prescription selects retarded propagation forward in time
- The object whose p-adic analog determines whether p-adic QFT can be perturbative at all

If the p-adic propagator is structurally different — with no iε, no time ordering, no causal boundary condition — then **every Feynman diagram computation changes**. This is not a cosmetic difference; it's a structural one that cascades through all of perturbative QFT.

---

## 2. The Archimedean Feynman Propagator (Reference)

### 2.1 Position-Space Form

For a scalar field of mass m in d = 4 Minkowski spacetime:

```
Δ_F(x−y) = ∫ d⁴k/(2π)⁴  e^{−ik·(x−y)} / (k² − m² + iε)
```

where:
- `k² = (k⁰)² − k²` (Minkowski metric signature +−−−)
- `iε` is the Feynman prescription: ε → 0⁺
- The integration is over ℝ⁴ with Lebesgue measure d⁴k

### 2.2 The iε Prescription (Crucial)

The iε term does three things simultaneously:

1. **Selects the causal boundary condition**: positive frequencies propagate forward in time, negative frequencies backward
2. **Regularizes the poles**: moves them off the real axis to k⁰ = ±√(k² + m²) ∓ iε
3. **Enforces the time-ordered product**:

```
⟨0|T{φ(x)φ(y)}|0⟩ = iΔ_F(x−y)
```

where T is the time-ordering operator:

```
T{φ(x)φ(y)} = θ(x⁰ − y⁰)φ(x)φ(y) + θ(y⁰ − x⁰)φ(y)φ(x)
```

with the step function θ(t) = 1 for t > 0, 0 for t < 0.

### 2.3 Wick Rotation Connection

The iε prescription is equivalent to the Euclidean continuation k⁰ → ik⁴_E, which yields the Euclidean propagator:

```
Δ_E(x−y) = ∫ d⁴k_E/(2π)⁴  e^{ik_E·(x−y)_E} / (k²_E + m²)
```

The poles are at k⁰_E = ±i√(k² + m²) — purely imaginary, never on the integration contour.

---

## 3. The p-Adic Framework

### 3.1 The Additive Character (Replaces e^{ikx})

The p-adic Fourier transform uses the **additive character** χ_p(ξ) instead of exp(2πiξ):

```
χ_p(ξ) = exp(2πi · {ξ}_p)
```

where `{ξ}_p` is the fractional part of ξ ∈ ℚ_p:

```
{ξ}_p = ∑_{i=n}^{-1} a_i p^i    (n < 0 if |ξ|_p > 1)
```

**Key properties:**

| Property | Archimedean (e^{ikx}) | p-adic (χ_p(kx)) |
|:---|:---|:---|
| Domain | ℝ (all real numbers) | ℚ_p (all p-adic numbers) |
| Periodicity/additivity | e^{i(k₁+k₂)x} = e^{ik₁x} e^{ik₂x} | χ_p(ξ₁+ξ₂) = χ_p(ξ₁)χ_p(ξ₂) |
| Orthogonality | ∫ e^{ikx} dx = 2πδ(k) | ∫_{ℤ_p} χ_p(kx) dx = 1_{|k|_p ≤ 1} |
| Analyticity | Entire function on ℂ | Locally constant, NO analytic continuation |

**Critical difference:** χ_p is NOT the restriction of exp to ℚ_p. The restriction of the real exponential to ℚ_p is unbounded and not a character. χ_p is a fundamentally different function — it is **locally constant** (constant on balls of radius p^{-1}), while e^{ikx} is nowhere locally constant.

### 3.2 The p-Adic Fourier Transform

For a function f: ℚ_p^d → ℂ:

```
F[f](k) = ∫_{ℚ_p^d} χ_p(−k·x) f(x) d^d x
```

where:
- `k·x = k₁x₁ + ... + k_d x_d` (p-adic dot product)
- `d^d x` is the **Haar measure** on ℚ_p^d, normalized by ∫_{ℤ_p^d} d^d x = 1

**No factor of (2π)^{-d/2} appears.** The normalization is purely algebraic — the Haar measure is normalized on the unit ball ℤ_p^d, not by any continuous integral formula.

### 3.3 p-Adic Integration Over Spheres

In ℝ^d, the volume element in spherical coordinates is:

```
d^d k = k^{d−1} dk dΩ_{d−1}    →    dΩ_{d−1} = 2π^{d/2}/Γ(d/2)
```

In ℚ_p^d, the "sphere" of radius p^n:

```
S_n = {x ∈ ℚ_p^d : |x|_p = p^n}
```

has Haar measure:

```
μ(S_n) = p^{n d} (1 − p^{−d})
```

This is a RATIONAL number — no π, no Gamma function. The p-adic sphere is a **totally disconnected clopen set**, not a smooth manifold.

---

## 4. The p-Adic Propagator

### 4.1 Vladimirov-Volovich Construction

Vladimirov, Volovich, and Zelenov (1994) constructed the p-adic propagator as the Green's function of the p-adic Klein-Gordon operator:

```
(D + m²) G_p(x) = δ(x)
```

where D is the p-adic Laplace operator (Vladimirov operator):

```
(Dφ)(x) = ∫_{ℚ_p^d} (φ(y) − φ(x)) / |x−y|_p^{d+α} d^d y    [fractional derivative of order α]
```

The p-adic propagator in momentum space:

```
G̃_p(k) = 1 / (|k|_p^α + m²)
```

**No iε. No causal boundary condition. No time ordering.** The denominator is p-adically valued and there is no concept of "above" vs. "below" the real axis — because ℚ_p is not ordered and there is no notion of "small imaginary part."

### 4.2 Explicit Form in Position Space

The p-adic propagator G_p(x−y) has the following properties:

1. **Radial**: depends only on |x−y|_p (ultrametric structure)
2. **No oscillatory behavior**: χ_p(kx) is locally constant, not oscillatory
3. **Decay**: For large |x−y|_p, decays as a power law (not exponential)
4. **No light-cone**: There is no p-adic analog of the light-cone singularity structure (x² = 0)

### 4.3 The Euclidean vs. Minkowski Problem

There is a deeper issue. The standard Feynman propagator uses Minkowski spacetime ℝ^{3,1} with indefinite metric signature. The Wick rotation maps this to Euclidean ℝ⁴. The p-adic propagator G̃_p(k) = 1/(|k|_p^α + m²) is inherently **Euclidean** — the denominator adds |k|_p^α (a norm) and m² (a positive number), with no possibility of a sign difference.

**In ℚ_p, there is no natural Minkowski analog.** The p-adic norm |·|_p is always non-negative, and the decomposition into "time-like" and "space-like" components (k⁰² − k²) has no p-adic meaning because:
- k⁰² − k² involves subtraction, which is ill-behaved p-adically (ultrametric: |a−b|_p ≤ max(|a|_p, |b|_p))
- The concept of a "light-cone" requires an ordered distinction between time and space

### 4.4 What Is Missing

| Feature | Archimedean Propagator | p-Adic Propagator |
|:---|:---|:---|
| **Oscillatory kernel** | e^{ikx} — oscillates everywhere | χ_p(kx) — locally constant, piecewise |
| **iε prescription** | Selects causal boundary condition | **Absent** — no complex deformation possible |
| **Time ordering** | θ(x⁰−y⁰) via contour integral | **Absent** — θ(t) undefined in ℚ_p |
| **Light-cone singularities** | Branch cut structure at k² = m² | No Lorentz group p-adically |
| **Retarded/advanced split** | Δ_R vs. Δ_A via contour choice | **No distinction** — propagator is acausal |
| **Wick rotation** | Maps Minkowski → Euclidean | Propagator is already "Euclidean" |
| **Fourier normalization** | (2π)^{-4} from ∫ e^{ikx}dx = (2π)⁴δ(k) | Normalized by ∫_{ℤ_p} dx = 1 (no π) |

---

## 5. Structural Consequences

### 5.1 Every Feynman Diagram Changes

The propagator is the building block of every Feynman diagram. If G_p ≠ Δ_F, then:

- **One-loop diagrams**: Self-energy, vacuum polarization, vertex corrections — all change
- **Multi-loop diagrams**: Different integration measure × different propagator = different amplitudes at every loop order
- **Cutting rules**: The optical theorem (Im M = ∑|M|²) relies on the iε prescription's analytic structure — fails p-adically
- **Unitarity**: The S-matrix is non-unitary in the usual sense; p-adic "unitarity" is different

### 5.2 The β-Function Connection

The one-loop β-function coefficient comes from the bubble diagram:

```
∫ d⁴k/(2π)⁴  Δ_F(k) Δ_F(k+p)  →  1/(16π²) log(Λ²/m²) + finite
```

In p-adic QFT, the same diagram gives:

```
∫_{ℚ_p⁴} d⁴k  G̃_p(k) G̃_p(k+p)  →  C_p log_p(Λ/m)
```

where C_p is a rational function of p (not involving π) and log_p is the p-adic logarithm. The coefficient differs. This is Missarov's (1989) core result for φ⁴ theory.

### 5.3 The S-Matrix and LSZ Reduction

The LSZ reduction formula extracts S-matrix elements from correlation functions:

```
⟨out|S|in⟩ = lim_{p_i²→m²} ∏_i (p_i²−m²) ⟨T{φ(p₁)...φ(p_n)}⟩
```

This requires:
1. **On-shell limit**: p_i² → m² — poles of the propagator
2. **Time ordering**: T-product of field operators

The p-adic propagator has different pole structure (rational poles in |k|_p, not continuous poles in k²), and T-products do not exist. The LSZ reduction must be reformulated — if it can be at all.

---

## 6. Implications for the Catalog

### 6.1 Direct Affected Predictions

| Prediction | Tier | How Propagator Difference Affects It |
|:---|:---|:---|
| **β-function coefficients** (#6) | Tier 2 | One-loop bubble diagram coefficient changes directly |
| **Critical exponents** (#7) | Tier 2 | RG recursion from propagator convolution differs |
| **Anomalous dimensions** (#8) | Tier 2 | OPE depends on propagator short-distance behavior |
| **S-matrix** (#10) | Tier 2 | Every S-matrix element changes; LSZ may not exist |
| **g−2 coefficients** (#17) | Tier 4 | Schwinger term from one-loop vertex correction changes |
| **Lamb shift** (#18) | Tier 4 | Self-energy diagram coefficient changes |
| **Loop integral volumes** (#5) | Tier 1–2 | Every loop diagram normalization changes |

**Total: 7 of 21 predictions directly affected by the propagator difference.**

### 6.2 The Cascade Structure

The propagator difference is not isolated — it **cascades**:

```
Propagator difference
    → Different one-loop amplitudes
        → Different β-functions (Missarov)
            → Different RG flow
                → Different critical behavior at all scales
    → Different multi-loop amplitudes
        → Different g−2, Lamb shift, etc.
    → No T-product → No LSZ → No S-matrix (in the usual sense)
```

---

## 7. Open Problems

1. **Is there a p-adic analog of the iε prescription?** Possible via p-adic analytic continuation into ℂ_p (complex p-adic numbers), but this is a totally different completion — ℂ_p is algebraically closed and not locally compact.

2. **Can p-adic QFT be formulated with a meaningful time direction?** Ultrametric time (crystalline time) or a p-adic "light-cone" based on quadratic forms over ℚ_p might exist but has not been developed.

3. **Does p-adic unitarity have a physical interpretation?** The p-adic optical theorem (if it exists) would relate p-adic amplitudes to p-adic probabilities — but what does a p-adic probability mean?

4. **Can we compute explicit numerical differences for specific diagrams?** The bubble diagram (for β-function) and the vertex correction (for g−2) are the most tractable computational targets.

---

## 8. References

- Vladimirov, Volovich, Zelenov (1994): *p-adic Analysis and Mathematical Physics*, World Scientific. **The standard reference.** Chapters 5-7 cover p-adic quantum mechanics and the p-adic propagator.
- Missarov (1989): "Renormalization group in p-adic φ⁴ theory." Explicit computation of p-adic β-function coefficients.
- Lerner, Missarov (1989): "p-adic φ⁴ theory and its fixed points."
- Dragovich, Khrennikov, Kozyrev, Volovich (2017): "p-Adic Mathematical Physics: The First 30 Years." Review article covering the state of the art.
- Koblitz (1984): *p-adic Numbers, p-adic Analysis, and Zeta-Functions*. Foundational text for p-adic analysis.

### QNFO Internal
- `non-cosmetic-archimedean-predictions.md` §2.1, §2.4, §2.5 — β-functions, propagator causality, S-matrix
- `completion-failures-ostrowski.md` — Programme specification, Category B (propagator)
- `pi-adelic-decomposition.md` — Fourier normalization, π in Archimedean Fourier transform

---

*Document status: DRAFT | Next: Compare explicit bubble diagram computation (Archimedean vs. p-adic) for β-function coefficient*
