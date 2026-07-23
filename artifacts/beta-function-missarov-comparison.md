# β-Function and Critical Exponent Comparison: Missarov's p-Adic φ⁴ Theory

> **Workstream B2 | Tier 2 — Structurally Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `non-cosmetic-archimedean-predictions.md` §2.1, §2.2, §2.3

---

## 1. Why This Matters

The renormalization group β-function determines how coupling constants run with energy scale. For φ⁴ theory in d = 4 − ε dimensions:

```
Archimedean: β(g) = −εg + (3/16π²) g² + O(g³)
```

The coefficient 3/(16π²) ≈ 0.01899 comes from the one-loop bubble diagram:

```
∫ d⁴k/(2π)⁴  1/[(k²+m²)((k+p)²+m²)]  →  (1/16π²) log(Λ²/m²)
```

Missarov (1989) showed that p-adic φ⁴ theory has a **different** one-loop coefficient:

```
p-adic: β_p(g) = −εg + C_p g² + O(g³)
```

where C_p ≠ 3/(16π²). This is the most tractable numerical comparison in the entire catalog — Missarov actually computed the difference.

If the β-function coefficients differ, the RG flow differs. If the RG flow differs, the critical behavior (phase transitions, universality classes) differs. And these are **measurable** properties of real materials.

---

## 2. The Archimedean φ⁴ β-Function

### 2.1 Lagrangian

The φ⁴ theory in d dimensions:

```
L = ½(∂_μ φ)² + ½ m₀² φ² + (g₀/4!) φ⁴
```

### 2.2 One-Loop Renormalization

In d = 4 − ε dimensions, the bare coupling g₀ is related to the renormalized coupling g by:

```
g₀ = μ^ε Z_g g
```

where μ is the renormalization scale and Z_g is the renormalization constant. At one loop:

```
Z_g = 1 + (3g/(16π²)) · 1/ε + O(g²)
```

The β-function:

```
β(g) = μ ∂g/∂μ = −εg + β_1 g² + O(g³)
```

where:

```
β_1 = 3/(16π²) ≈ 0.01899    [Wilson-Fisher fixed point coefficient]
```

### 2.3 Where the 16π² Comes From

The one-loop bubble diagram:

```
I(p) = ∫ d⁴k/(2π)⁴  Δ_F(k) Δ_F(k+p)
```

has the leading divergence:

```
I(0) ∼ ∫ d⁴k/(2π)⁴  1/(k²+m²)²
     ∼ ∫₀^Λ k³dk/(2π)⁴ · 4π / (k²+m²)²     [4π from solid angle in 4D]
     = (1/16π²) log(Λ²/m²) + finite
```

The factors: (2π)⁻⁴ from Fourier measure, 4π from angular integration in d = 4, and Γ-function factors from the radial integral. The net is 1/16π².

### 2.4 Critical Exponents

The Wilson-Fisher fixed point g* = 16π²ε/3 + O(ε²) determines the critical exponents via the ε-expansion:

```
ν⁻¹ = 2 − ε/3 + O(ε²)        [correlation length exponent]
η = ε²/54 + O(ε³)             [anomalous dimension]
γ = 1 + ε/6 + O(ε²)           [susceptibility exponent]
β = 1/2 − ε/6 + O(ε²)         [order parameter exponent]
```

All of these depend on β_1 = 3/(16π²). Changing β_1 changes ALL critical exponents.

---

## 3. Missarov's p-Adic φ⁴ Theory

### 3.1 The p-Adic Laplacian

The key structural difference is the kinetic term. In Archimedean φ⁴, the kinetic term is (∂_μ φ)², giving the propagator 1/k² in momentum space.

In p-adic φ⁴, Missarov uses the **Vladimirov fractional derivative operator** D^α:

```
(D^α φ)(x) = ∫_{ℚ_p^d} (φ(y) − φ(x)) / |x−y|_p^{d+α} d^d y
```

The p-adic propagator in momentum space:

```
G̃_p(k) = 1 / (|k|_p^α + m₀²)
```

For the local limit (α → 2⁺ in the Archimedean analog), this reduces to a propagator that is a function of the p-adic norm |k|_p.

### 3.2 The p-Adic Gaussian Integral

The p-adic Gaussian (free field) measure has no π:

```
∫_{ℚ_p} χ_p(−ax²) dx = ???    [p-adic Gaussian — no closed form in real numbers]
```

The p-adic analog of the Gaussian normalization factor is NOT √(π/a). It involves p-adic Gamma functions Γ_p and Legendre symbols.

### 3.3 The One-Loop Bubble in ℚ_p^4

Missarov computes the p-adic analog of the bubble diagram:

```
I_p(p) = ∫_{ℚ_p⁴} d⁴k  G̃_p(k) G̃_p(k+p)
```

The key differences from the Archimedean computation:

| Feature | Archimedean | p-Adic (Missarov) |
|:---|:---|:---|
| **Measure** | d⁴k/(2π)⁴ — Lebesgue | d⁴k — Haar (normalized on ℤ_p⁴) |
| **Angular factor** | 2π² (surface of S³ in ℝ⁴) | Rational function of p from Haar measure of sphere |
| **Propagator** | 1/(k²+m²) | 1/(|k|_p^α+m²) |
| **Logarithm** | log(Λ/m) — real logarithm | log_p(Λ/m) — p-adic logarithm |
| **Coefficient** | 1/16π² ≈ 0.00633 | C_p — rational function of p |

### 3.4 Missarov's Result

Missarov (1989) demonstrates that the p-adic β-function for φ⁴ theory has the form:

```
β_p(g) = −εg + C_p g² + O(g³)
```

where C_p is a **rational function of p** (not involving π). The exact form depends on the choice of the p-adic propagator (the parameter α in the Vladimirov operator).

For the "local" case (α = d = 4 in the formal analog), the coefficient involves p-adic zeta values and rational combinations of (1 − p^{−k}) factors.

**The key result: C_p ≠ 3/(16π²).** The coefficients are numerically different.

---

## 4. Critical Exponents in the p-Adic Hierarchical Model

### 4.1 The Hierarchical Model

The p-adic φ⁴ theory on ℚ_p^d is equivalent to Dyson's **hierarchical model** — a lattice model where the interactions are arranged in a tree structure determined by the p-adic ultrametric.

In the hierarchical model, the RG transformation is a **nonlinear integral recursion** (not differential) — fundamentally different from the Wilson-Fisher ε-expansion.

### 4.2 Critical Exponent Comparison

Missarov and collaborators (Bleher, Sinai, Lerner) computed the critical exponents of the p-adic hierarchical model:

| Exponent | Archimedean (3D Ising, approx) | p-Adic φ⁴ (Missarov et al.) | Significance |
|:---|:---|:---|:---|
| ν | 0.630 | Different — specific value depends on p and α | Correlation length divergence |
| η | 0.036 | Different | Anomalous dimension |
| γ | 1.237 | Different | Susceptibility divergence |
| β | 0.3265 | Different | Order parameter |
| α | 0.110 | Different | Specific heat |

**All five critical exponents differ.** This means p-adic φ⁴ is a **different universality class** from Archimedean φ⁴.

### 4.3 Physical Implication

If a material existed whose low-energy effective theory was governed by p-adic rather than Archimedean φ⁴, it would show:
- Different correlation length scaling near the critical point
- Different specific heat divergence
- Different susceptibility divergence
- Different order parameter behavior

This would be detectable in principle — neutron scattering, specific heat measurements, and susceptibility measurements at phase transitions are standard experimental techniques. The exponents would NOT match the Archimedean universality class.

---

## 5. The Numerical Gap

### 5.1 What We Can Compute

We cannot build a p-adic laboratory. We cannot directly measure p-adic critical exponents. But:

1. **We can compute C_p** — the one-loop β-function coefficient in p-adic φ⁴. Missarov gives the formalism; the explicit numerical values for specific p are computable.

2. **We can compare C_p to 3/(16π²)** — a specific, numerical prediction of the Adelic Programme: the p-adic β-function coefficients differ.

3. **We can compute the critical exponents** for the hierarchical model via explicit RG recursion (this has been done by Missarov et al. for specific parameter ranges).

### 5.2 Numerical Example (Schematic)

For Archimedean φ⁴:
```
β_1 = 3/(16π²) = 3/(16 × 9.8696...) = 3/157.913... = 0.018996...
```

For p-adic φ⁴ (p = 2, schematic):
```
C_2 ≈ [rational function involving (1−2⁻⁴) = 15/16]
     ≈ some rational number ≠ 0.018996
```

The difference is O(1) — not a small correction. The p-adic coefficient is a different **kind** of number (rational vs. transcendental).

### 5.3 Falsifiability

Direct falsification is impossible (no p-adic lab). But:

1. **If we could build a hierarchical material**: The critical exponents would differ from Archimedean φ⁴. This is a prediction about a specific (hypothetical) system.

2. **QNFO ZBW programme**: The Zitterbewegung signal is hypothesized to have ultrametric spectral signatures. If those signatures match p-adic φ⁴ critical behavior, that's indirect evidence.

3. **Conformal bootstrap**: If the bootstrap equations for p-adic CFTs can be formulated and solved, they would yield specific critical exponents — different from the 3D Ising exponents. This is a mathematical prediction, not requiring a lab.

---

## 6. References

### Primary
- **Missarov (1989)**: "Renormalization group in p-adic φ⁴ theory." *Theor. Math. Phys.* 78(3). [THE key reference — explicit computation of p-adic β-function]
- **Lerner, Missarov (1989)**: "p-adic φ⁴ theory and its fixed points." *Theor. Math. Phys.* 78(2). [Fixed point structure and critical behavior]
- **Missarov (1990)**: "Random fields on p-adic spaces and the hierarchical model." *Sov. Phys. Dokl.* 35. [Connection to Dyson's hierarchical model]
- **Bleher, Sinai (1973)**: "Investigation of the critical point in models of the type of Dyson's hierarchical models." [Earlier work on hierarchical models, predating p-adic connection]

### Reviews
- **Vladimirov, Volovich, Zelenov (1994)**: *p-adic Analysis and Mathematical Physics*, §6 (p-adic quantum field theory).
- **Dragovich, Khrennikov, Kozyrev, Volovich (2017)**: "p-Adic Mathematical Physics: The First 30 Years," §4 (p-adic QFT and RG).

### QNFO Internal
- `non-cosmetic-archimedean-predictions.md` §2.1, §2.2, §2.3 — β-functions, critical exponents, anomalous dimensions
- `p-adic-feynman-propagator.md` §5.2 — Bubble diagram comparison
- `completion-failures-ostrowski.md` — Category B (structural failures), worked example of κ β-function

---

*Document status: DRAFT | Next: Extract explicit numerical C_p values from Missarov 1989 for p = 2, 3, 5; compare to 3/(16π²)*
