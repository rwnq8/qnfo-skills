# Non-Cosmetic Archimedean Predictions: The p-Adic Differential Catalog

> **A systematic catalog of physical predictions whose numerical values would genuinely differ between Archimedean and p-adic completions — not just normalization, but measured observables.**
>
> Part of: *Completion Failures Under Ostrowski's Theorem* research programme
> Status: ACTIVE | Started: 2026-07-23 | Cross-refs: `adelic-constraint-engine.md`, `pi-adelic-decomposition.md`, `completion-failures-ostrowski.md`

---

## 0. Preamble: Why This Catalog Is the Programme's Linchpin

The prior documents established that π does not exist in ℚ_p, that the p-adic Gaussian integral has no π, and that there are "cosmetic" vs. "non-cosmetic" appearances of Archimedean constants in physics. But the crucial question has not been systematically answered:

> **Which physical predictions would actually come out differently in a p-adic world?**

This is not a philosophical question — it's a **falsifiability question**. If every Archimedean π turns out to be cosmetic (absorbable into coupling definitions), then the adelic programme is empty: the p-adic completions exist mathematically but make no distinguishable physical predictions. The programme lives or dies on whether it can produce **non-degenerate** predictions — predictions that differ between completions and could, in principle, be tested.

This document catalogues the Type II (non-cosmetic) predictions in five tiers of descending certainty:

| Tier | Criterion | Count |
|:---|:---|:---|
| **Tier 1: Numerically Non-Cosmetic** | Different number comes out; no free parameter to absorb it | 5 |
| **Tier 2: Structurally Non-Cosmetic** | Different mathematical structure; numerical difference plausible but harder to compute | 6 |
| **Tier 3: Existentially Non-Cosmetic** | The concept itself fails in ℚ_p; no p-adic analog exists | 4 |
| **Tier 4: Borderline/Ambiguous** | Depends on what is treated as fundamental vs. measured | 6 |

---

## 1. The Classification Methodology

### 1.1 The Cosmetic Test

Given a formula F containing π, exp, or another Archimedean-only construct:

1. **Absorption test**: Can the Archimedean constant be absorbed into a REDEFINITION of a coupling, a unit, or a coordinate choice, WITHOUT changing any measurable prediction?
   - YES → Type I (cosmetic). Example: α = e²/(4πħc). Define g² = 4πα and eliminate π.
   - NO → proceed to step 2.

2. **Emergence test**: Does the constant emerge as the EVALUATION of a mathematical operation (sum, integral, zeta value) that produces a specific number?
   - YES → Type II (emergent/non-cosmetic). Example: ζ(4) = π⁴/90 — π⁴ is the value, not a convention.
   - NO → proceed to step 3.

3. **Structure test**: Does the prediction depend on the topology, ordering, or connectedness of ℝ?
   - YES → Type II (structural non-cosmetic). Example: time ordering via θ(t) — ℚ_p is not ordered.
   - NO → Ambiguous.

### 1.2 The p-Adic Differential

For Type II predictions, define the **p-adic differential** Δ_p:

```
Δ_p = |(Prediction_∞) − (Prediction_p)| / (Prediction_∞)
```

This is the fractional difference between Archimedean and p-adic predictions. For cosmetic π, Δ_p ≡ 0. For non-cosmetic predictions, Δ_p ≠ 0.

### 1.3 Falsifiability Criterion

A prediction is **falsifiable** if there exists a measurement (real or gedanken) that distinguishes between the Archimedean and p-adic values. A prediction is **unfalsifiable** if the p-adic difference can always be absorbed into a free parameter that we already fit from data.

---

## TIER 1: NUMERICALLY NON-COSMETIC PREDICTIONS

*These produce different NUMBERS in different completions. The Archimedean answer is a specific transcendental number. The p-adic answer is a different number — not just a different normalization, but a genuinely different value of a dimensionless observable.*

---

### 1.1 The Stefan-Boltzmann Constant

#### Archimedean Form

```
u = σ T⁴
σ = π² k⁴ / (60 ħ³ c²) = 5.670374419 × 10⁻⁸ W·m⁻²·K⁻⁴
```

#### π Trace

The π² factor comes from evaluating the dimensionless integral:

```
∫₀^∞ x³/(eˣ − 1) dx = π⁴/15
```

This integral decomposes as:

```
∫₀^∞ x³ ∑_{n=1}^∞ e^{-nx} dx = 6 ∑_{n=1}^∞ 1/n⁴ = 6 ζ(4)
```

And ζ(4) = π⁴/90 by Euler. The π² in σ is (π⁴/15) × (other constants), giving π²/60 after multiplying by other factors.

#### Why It's Non-Cosmetic

- σ has DIMENSIONS (W·m⁻²·K⁻⁴). You cannot absorb π² into a unit redefinition without changing the watt, meter, or kelvin — which changes ALL other measurements in inconsistent ways.
- σ is directly MEASURED in blackbody radiation experiments. It's a physical constant, not a convention.
- The temperature scale T is fixed independently of σ (by Boltzmann constant k_B definition since 2019, or by thermodynamic temperature measurement). There is no free parameter to "absorb π."
- σ CANNOT be eliminated by redefining Boltzmann's constant k_B because k_B is FIXED in SI (k_B = 1.380649 × 10⁻²³ J/K exactly since 2019) and changing k_B would break all of statistical mechanics.

**Verdict: TYPE II — UNAMBIGUOUSLY NON-COSMETIC.**

#### p-adic Reconstruction

The p-adic analog requires:
1. **p-adic phase space integration**: The momentum space volume element d³p in ℚ_p³ has a fundamentally different measure from 4πp²dp. The p-adic sphere {x: |x|_p = pⁿ} has measure p^{2n}(1 − p^{-3}) (not 4π).
2. **p-adic Bose-Einstein distribution**: Requires exp(−ħω/kT), which converges in ℚ_p only for |ħω/kT|_p < p^{−1/(p−1)}. This is a severely restricted domain. At sufficiently low temperature, the distribution may be undefined.
3. **p-adic ζ-values**: ζ_p(s) (Kubota-Leopoldt) takes p-adic values — completely different from the real ζ(s).

The p-adic Stefan-Boltzmann "constant" would be:

```
σ_p = (something depending on p-adic measure) × ζ_p(4) × (unit conversions)
```

The key point: **ζ_p(4) is NOT π⁴/90**. It's a p-adic number with no simple relationship to π. The numerical coefficient would differ.

#### Numerical Estimate

We cannot compute σ_p exactly without a complete p-adic thermodynamic theory. But the STRUCTURE is clear: the coefficient changes. For p = 2:

- Real ζ(4) = π⁴/90 = 1.082323...
- ζ_2(4) (p-adic zeta) = ? (no closed form in terms of real numbers; a 2-adic number)

The fractional difference Δ₂ ≡ |σ − σ₂|/σ could be O(1) — i.e., the p-adic blackbody could radiate at a fundamentally different rate.

#### Falsifiability

We cannot build a p-adic blackbody in the lab. However, if the universe is fundamentally adelic, the measured σ_∞ should satisfy the product formula with σ_p. This constrains the allowed values of σ_∞.

---

### 1.2 The Casimir Force

#### Archimedean Form

```
F/A = −π² ħ c / (240 a⁴)
```

where a is the plate separation. The force per unit area between two perfectly conducting parallel plates.

#### π Trace

The Casimir energy between plates separated by distance a:

```
E(a) = (ħc/2) ∑_{n=1}^∞ ∫ d²k/(2π)² √(k² + (nπ/a)²)
```

The sum over modes diverges and is regularized using ζ-regularization:

```
∑_{n=1}^∞ n³ → ζ(−3) = 1/120
```

But the full calculation involves: ∫ d²k/(2π)² → π in normalization, and the final force comes out as π²ħc/(240a⁴). The π² emerges from:
- (2π)⁻² from momentum integration → π⁻² from the Fourier measure
- π from the mode spacing (nπ/a boundary condition)
- π from the angular integration
- Net: the surviving π² is embedded in the regularized sum

Most critically: **ζ(−3) = 1/120 is the Archimedean zeta value.** The p-adic zeta ζ_p(−3) is a p-adic number, not 1/120.

#### Why It's Non-Cosmetic

- The Casimir force has been MEASURED (Lamoreaux 1997, Mohideen 1998, and many subsequent experiments). The π²ħc/(240a⁴) formula matches measurements within experimental error.
- The a⁻⁴ distance scaling might be topological (independent of completion), but the π²/240 COEFFICIENT is specific to the Archimedean regularization.
- No free parameter exists to absorb the π² factor. ħ, c, and a are all independently determined.

**Verdict: TYPE II — UNAMBIGUOUSLY NON-COSMETIC.**

#### p-adic Reconstruction

The p-adic Casimir effect would involve:
1. p-adic momentum integration with Haar measure on ℚ_p²
2. p-adic ζ-regularization using ζ_p(s)
3. p-adic analog of perfectly conducting boundary conditions

The p-adic Casimir force:

```
(F/A)_p = −C_p ħ c / a⁴
```

where C_p ≠ π²/240. The coefficient C_p is determined by p-adic ζ-values and p-adic phase space volumes.

#### Known Literature

Vladimirov and Volovich (1988) initiated the study of p-adic quantum mechanics. Dragovich and collaborators have studied adelic quantum mechanics. However, I am not aware of a complete computation of the p-adic Casimir force in the existing literature. This is a **research opportunity**.

#### Numerical Comparison

Since ζ(s) and ζ_p(s) are fundamentally different analytic functions:
- Real ζ(−3) = 1/120 = 0.008333...
- p-adic ζ_p(−3) = (1 − p³)⁻¹ × (something) → a rational p-adic number

The Archimedean result C_∞ = π²/240 ≈ 0.0411. The p-adic C_p would be different.

---

### 1.3 Riemann Zeta at Even Integers — The Basel-Class Summations

#### Archimedean Form

```
ζ(2) = π²/6
ζ(4) = π⁴/90
ζ(6) = π⁶/945
ζ(2n) = (−1)^{n+1} B_{2n} (2π)^{2n} / (2(2n)!)
```

These are mathematical THEOREMS. The left side (ζ(2n) = ∑ 1/k^{2n}) is a sum of rational numbers. The right side contains π^{2n}.

#### Why It's Non-Cosmetic

- These are mathematical facts, not physical conventions. You cannot "redefine π away" — it would change the truth value of Euler's theorem.
- The p-adic zeta function ζ_p(s) (Kubota-Leopoldt) has NO closed-form relationship to π. The values ζ_p(2), ζ_p(4), etc., are p-adic numbers — fundamentally different from their Archimedean cousins.
- **Crucially**: the series ∑_{n=1}^∞ 1/n² converges to π²/6 in ℝ, but in ℚ_p, the TERMS |1/n²|_p can be arbitrarily large (when p divides n), and the series does NOT converge in the p-adic topology.

#### p-adic Comparison

| Property | Archimedean ζ(2) | p-adic ζ_p(2) |
|:---|:---|:---|
| Definition | ∑ 1/n² (converges in ℝ) | Interpolation of ζ at negative integers |
| Value | π²/6 ≈ 1.644934... | p-adic number — no simple real interpretation |
| Analytic structure | Meromorphic on ℂ, pole at s=1 | p-adic meromorphic on ℂ_p, pole at s=1 |
| Special values | Rational combinations of π and Bernoulli numbers | Congruences (Kummer, Iwasawa) |

#### Physics Implications

Any QFT calculation using ζ-regularization implicitly evaluates the Archimedean zeta. If the same regularization is done p-adically, different numerical coefficients emerge. This affects:
- Casimir energies (already covered in §1.2)
- Dimensional regularization in d = 4 − 2ε (Γ-function and ζ-function cancellations)
- Anomaly coefficients
- Heat kernel expansions

**Verdict: TYPE II — MATHEMATICALLY NON-COSMETIC.**

---

### 1.4 The Wien Displacement Law (Blackbody Peak)

#### Archimedean Form

```
λ_max T = b = hc/(x k_B)  where x ≈ 4.96511423174...
```

x is the solution to the transcendental equation:

```
x = 5(1 − e^{-x})
```

#### π Trace

The transcendental equation involves only exp(x). But the CONSTANT b = hc/(xk_B) = 2.897771955... × 10⁻³ m·K involves no π directly. However:

The blackbody SPECTRUM I(ν,T) ∝ ν³/(e^{hν/kT} − 1) involves exp, and the integral ∫_0^∞ x³/(eˣ−1)dx = π⁴/15 (as in Stefan-Boltzmann). The peak condition x = 5(1 − e⁻ˣ) involves the FIRST MOMENT of the distribution, while Stefan-Boltzmann involves the ZEROTH moment (total area).

#### Why It's Non-Cosmetic

- The transcendental equation x = 5(1 − e⁻ˣ) uses exp(x), which has limited p-adic convergence.
- The solution x ≈ 4.9651... is a transcendental number (not algebraic). It has no p-adic analog.
- A p-adic blackbody spectrum would use χ_p instead of exp, fundamentally changing the distribution shape and the peak location.

#### p-adic Reconstruction

The p-adic analog of the Planck spectrum would replace e^{ħω/kT} with some p-adic character expression. The peak condition would be different. The Wien constant b would have a p-adic value b_p ≠ b_∞.

**Verdict: TYPE II — NON-COSMETIC.**

---

### 1.5 Gaussian Moments and Wick's Theorem Normalization

#### Archimedean Form

Wick's theorem for a real scalar field:

```
⟨φ(x₁)...φ(x_{2n})⟩ = ∑_{pairings} ∏_{pairs} Δ_F(x_i − x_j)
```

where the propagator Δ_F(x−y) = ∫ d⁴k/(2π)⁴ e^{ik(x−y)}/(k²−m²+iε). The (2π)⁻⁴ normalization propagates into every n-point function.

#### π Trace

Every Feynman diagram with L loops contributes a factor of π^{L·d/2} from the spherical volume integration in momentum space. In dimensional regularization:

```
∫ d^d k (k²)^α/(k² + m²)^β ∝ π^{d/2} × (rational function of α,β,m²)
```

#### Why It's Non-Cosmetic

- The LOOP INTEGRAL itself contains π from the spherical volume. While the external normalization (Fourier convention) is cosmetic, the internal loop normalization is NOT — it enters the amplitude.
- Cross sections (|M|²) involve the SQUARE of the amplitude, so the π^{L·d/2} factor appears squared.
- However: if the π from loop integrals can be absorbed into the RENORMALIZED coupling, then it may become cosmetic. This is a subtle boundary case.

**Verdict: TYPE II — but check carefully. Some loop-π factors are absorbed into renormalized couplings (MS-bar scheme), but the residual finite parts may differ.**

---

## TIER 2: STRUCTURALLY NON-COSMETIC PREDICTIONS

*The mathematical object itself is different between completions. The numerical prediction depends on the structure, but direct computation of the p-adic analog may be challenging.*

---

### 2.1 Renormalization Group β-Functions

#### Archimedean Form

For φ⁴ theory in d = 4 − ε dimensions:

```
β(g) = −εg + (3/16π²) g² + O(g³)    [Archimedean]
```

The coefficient 3/(16π²) comes from the one-loop bubble diagram:

```
∫ d⁴k/(2π)⁴ 1/(k² + m²)((k+p)² + m²) → 1/(16π²) log(Λ²/m²)
```

#### p-adic Analog

Missarov (1989) and Lerner-Missarov (1989) studied p-adic φ⁴ theory using the p-adic Gaussian integral. The one-loop bubble in ℚ_p⁴ gives a DIFFERENT coefficient:

```
β_p(g) = −εg + C_p g² + O(g³)
```

where C_p ≠ 3/(16π²). The difference arises because:
- The p-adic momentum integration uses Haar measure, not Lebesgue measure
- The p-adic propagator involves additive characters, not exp
- The p-adic "spherical" volume is different

#### Why It's Non-Cosmetic

- The β-function is MEASURED (indirectly via running couplings in QED and QCD). The coefficient determines how fast the coupling runs.
- If p-adic φ⁴ has a different β-function coefficient, the running of the coupling at the p-adic place differs from the Archimedean place.
- **This means the RG flow is completion-dependent.** A theory that is asymptotically free at the ∞-place might not be asymptotically free at p-adic places.

#### Known Results

- Missarov showed p-adic φ⁴ has a non-trivial infrared fixed point that differs from the Archimedean one
- The critical exponent η (anomalous dimension) differs: η_Archimedean ≈ 0.036 (ε-expansion, O(ε²)), while η_p-adic is a different number

**Verdict: TYPE II — STRUCTURALLY NON-COSMETIC.**

---

### 2.2 Critical Exponents at Phase Transitions

#### Archimedean Form

The 3D Ising model critical exponents:

```
α ≈ 0.110,  β ≈ 0.3265,  γ ≈ 1.237,  δ ≈ 4.789,  ν ≈ 0.630,  η ≈ 0.036
```

These are computed via ε-expansion around d = 4 or via conformal bootstrap. They describe real phase transitions (liquid-gas critical point, ferromagnetic Curie point).

#### π Trace

The ε-expansion for φ⁴ theory uses loop integrals with π. The conformal bootstrap constrains operator dimensions using crossing symmetry in ℝ^d, which assumes connected space.

#### p-adic Analog

p-adic φ⁴ theory (hierarchical model) has been studied by Missarov, Bleher, Sinai, and others. The key difference:
- The p-adic Laplacian is different → different propagator
- p-adic φ⁴ on ℚ_p^d has **hierarchical** structure (ultrametric)
- The critical exponents of p-adic φ⁴ are DIFFERENT from Archimedean φ⁴

#### Why It's Non-Cosmetic

- Critical exponents are UNIVERSAL — they depend only on symmetry and dimension. If p-adic φ⁴ is a different universality class, then the exponents are different numbers.
- This means a phase transition in a "p-adic material" would have different critical behavior — different power laws for susceptibility, correlation length, specific heat.
- The critical exponents are MEASURABLE (neutron scattering, specific heat measurements).

#### Known Results

| Exponent | Archimedean (3D Ising, approx) | p-adic φ⁴ (Missarov) |
|:---|:---|:---|
| ν | 0.630 | Computable from p-adic RG recursion |
| η | 0.036 | Different — p-adic anomalous dimension |
| γ | 1.237 | Different |
| β | 0.3265 | Different |

The p-adic φ⁴ recursion relations are DIFFERENT equations from the Archimedean ones because the convolution with the p-adic propagator is structurally different.

**Verdict: TYPE II — STRUCTURALLY NON-COSMETIC. DIFFERENT UNIVERSALITY CLASS.**

---

### 2.3 Anomalous Dimensions and Operator Product Expansions

#### Archimedean Form

In conformal field theory, the scaling dimension Δ of an operator φ is:

```
Δ_φ = Δ_φ^{(0)} + γ_φ(g)
```

where γ_φ(g) is the anomalous dimension computed from loop diagrams. In φ⁴ at one loop:

```
γ_φ(g) = (1/12) (g/(16π²))² + O(g³)   [Archimedean]
```

#### π Trace

The 16π² comes from the loop integral normalization. In p-adic CFT (or p-adic QFT), the anomalous dimension receives p-adic corrections:

```
γ_φ^{(p)}(g) = (1/12) C_p² g² + O(g³)   [p-adic]
```

where C_p is the p-adic loop coefficient.

#### Why It's Non-Cosmetic

- Anomalous dimensions determine scaling laws at critical points
- If p-adic anomalous dimensions differ, the critical behavior differs
- Connected to §2.2 (critical exponents) but more general — applies also away from critical points

**Verdict: TYPE II — STRUCTURALLY NON-COSMETIC.**

---

### 2.4 The Feynman Propagator and Causality

#### Archimedean Form

```
Δ_F(x−y) = ∫ d⁴k/(2π)⁴ e^{−ik·(x−y)} / (k² − m² + iε)
```

The iε prescription selects the causal (Feynman) boundary condition:
- Positive frequencies propagate forward in time
- Negative frequencies propagate backward in time

The time-ordering step function:

```
θ(t) = { 1, t > 0; 0, t < 0; 1/2, t = 0 }
```

#### Why It's Non-Cosmetic (Structurally)

ℚ_p is NOT an ordered field. There is no total order compatible with field operations. This means:
- "t > 0" has NO MEANING in ℚ_p
- θ(t) has NO p-adic analog
- The Feynman propagator's causal structure is Archimedean-only

#### p-adic Status

p-adic propagators have been constructed (Vladimirov-Volovich) using additive characters instead of exp, and without the iε prescription. The resulting propagator does not distinguish between forward and backward propagation.

The p-adic propagator describes **acausal** propagation. This is not a minor modification — it's a fundamental structural difference.

#### Physics Implication

In a p-adic world, there is no "arrow of time." Events are ultrametrically ordered (tree structure) rather than linearly ordered. S-matrix time ordering fails. The entire apparatus of QFT perturbation theory — which relies on time-ordered products — collapses.

**Verdict: TYPE III BORDERLINE** — the concept of causality fails in ℚ_p, but it's not clear this produces a "different numerical prediction" so much as a different conceptual framework.

---

### 2.5 The S-Matrix (Scattering Amplitudes)

#### Archimedean Form

The LSZ reduction formula:

```
⟨out|S|in⟩ = poles of ⟨T{φ(x₁)...φ(x_n)}⟩
```

The S-matrix is the central object of QFT — it encodes all scattering probabilities.

#### Why It's Non-Cosmetic

The p-adic S-matrix would involve:
1. **p-adic Fourier transform** (additive characters) instead of e^{ikx} — different asymptotic states
2. **p-adic propagator** (no iε, no causal boundary condition)
3. **No time ordering** — the LSZ reduction uses T-products, which don't exist p-adically
4. **p-adic unitarity** — the optical theorem requires complex conjugation, which maps ℂ to itself — but the p-adic analog would need values in ℂ_p (complex p-adic numbers)
5. **Different pole structure** — the analytic structure of p-adic correlation functions is completely different

#### p-adic Status

Vladimirov-Volovich-Zelenov (1994) constructed p-adic quantum mechanics and p-adic perturbation theory. The p-adic S-matrix has been studied by various authors. Key findings:
- p-adic scattering amplitudes are rational functions of p-adic momenta
- The pole structure (particle masses) can differ
- Unitarity in the p-adic sense is different from Archimedean unitarity

**Verdict: TYPE II — STRUCTURALLY NON-COSMETIC.**

---

### 2.6 The Uncertainty Principle

#### Archimedean Form

```
Δx Δp ≥ ħ/2
```

The 1/2 comes from the specific normalization of the Fourier transform. In the convention:

```
ψ̂(p) = (1/√(2πħ)) ∫ dx e^{−ipx/ħ} ψ(x)
ψ(x) = (1/√(2πħ)) ∫ dp e^{+ipx/ħ} ψ̂(p)
```

The Parseval identity gives ∫|ψ|²dx = ∫|ψ̂|²dp. The uncertainty product minimization occurs for Gaussians: ψ(x) ∝ e^{−x²/(4σ²)} where Δx = σ, Δp = ħ/(2σ), product = ħ/2.

#### p-adic Analog

In p-adic quantum mechanics (Vladimirov-Volovich), the Fourier transform uses the additive character:

```
ψ̂(k) = ∫_{ℚ_p} χ_p(−kx) ψ(x) dx
```

with Haar measure normalized by ∫_{ℤ_p} dx = 1. There is NO π in the normalization. The p-adic Parseval identity has a different constant. The p-adic Gaussian is χ_p(ax²), which has different localization properties.

The p-adic uncertainty principle would take the form:

```
Δ_p x · Δ_p k ≥ C_p ħ
```

where C_p ≠ 1/2. The constant C_p depends on the p-adic Fourier normalization and the p-adic Gaussian's localization.

#### Why It's Non-Cosmetic

- The uncertainty bound is a MEASURED constraint — it affects squeezing limits, quantum metrology, and quantum information bounds.
- If C_p ≠ 1/2, then p-adic quantum mechanics has a different fundamental noise floor.
- However: the uncertainty principle is usually derived from the commutation relation [x̂,p̂] = iħ, which is algebraic and may be completion-independent. The constant 1/2 comes from a SPECIFIC choice of Fourier normalization. If the Fourier normalization is cosmetic, C_p = 1/2 might be universal. This is debatable.

**Verdict: BORDERLINE** — depends on whether the 1/2 in ΔxΔp ≥ ħ/2 is a consequence of algebraic structure (universal) or analytic normalization (completion-dependent).

---

## TIER 3: EXISTENTIALLY NON-COSMETIC PREDICTIONS

*The concept itself dissolves in ℚ_p. These are not predictions with different numbers — they are predictions that can't even be FORMULATED p-adically.*

---

### 3.1 Time Ordering and Causality

Already covered in §2.4. Essential point:

> **ℚ_p is not an ordered field. There is no p-adic analog of "before" and "after."**

Consequences:
- Feynman propagator (iε prescription) — no causal boundary condition
- S-matrix time ordering — T-products undefined
- Retarded/advanced Green's functions — no distinction
- Keldysh/Schwinger-Keldysh formalism — entire closed-time-path framework fails
- Quantum measurement (wavefunction collapse is a causal event) — undefined

This is arguably the HARDEST PROBLEM in the entire programme.

---

### 3.2 The Exponential Function and Time Evolution

#### Archimedean Form

```
U(t) = e^{−iHt/ħ}
```

Time evolution is unitary, continuous, and defined for all t ∈ ℝ.

#### p-adic Status

The p-adic exponential exp_p(x) converges only for:

```
|x|_p < p^{−1/(p−1)}
```

For p = 2, this means |x|_2 < 1/2 — an extremely restricted domain. For large t, the time evolution operator e^{−iHt/ħ} is undefined in ℚ_p.

p-adic time evolution would be:
- **Local**, not global — defined only for short times
- **Discontinuous** in the Archimedean sense (continuous in p-adic topology, but the topology is totally disconnected)
- **Non-unitary** in the usual sense — p-adic "unitarity" is different

**Verdict: TYPE III — EXISTENTIALLY NON-COSMETIC. Time evolution itself is Archimedean.**

---

### 3.3 Continuous Symmetries and Noether's Theorem

#### Archimedean Form

Noether's theorem: every continuous symmetry of the action generates a conserved current:

```
∂_μ j^μ = 0
```

The proof requires differentiation (limit of difference quotient) and continuous Lie group actions.

#### p-adic Status

ℚ_p is totally disconnected — there are no continuous paths. Lie groups over ℚ_p exist (p-adic Lie groups), but their infinitesimal generators (Lie algebras) are defined algebraically, not via limits. p-adic differentiation exists but the derivative is a very different object.

The p-adic analog of Noether's theorem has been studied (p-adic variational calculus by Vladimirov-Volovich), but the conserved currents are structurally different. The connection between symmetries and conservation laws may be weaker or different.

**Verdict: TYPE III — EXISTENTIALLY NON-COSMETIC. Continuous symmetry is Archimedean.**

---

### 3.4 WKB Quantization and Bohr-Sommerfeld

#### Archimedean Form

```
∮ p dx = 2πħ (n + γ_Maslov)
```

The quantization condition requires:
1. A closed orbit in phase space — a continuous closed curve
2. Integration around the orbit
3. The Maslov index γ counting caustics

#### p-adic Status

In ℚ_p, there are no continuous paths — only totally disconnected "jumps." A "closed orbit" in p-adic phase space has no natural parametrization. The integral ∮ p dx is undefined in the continuous sense.

The p-adic WKB method (if it exists) would use:
- p-adic integration over disconnected sets
- A fundamentally different quantization condition
- The "phase" 2πn would be replaced by something p-adic

**Verdict: TYPE III — EXISTENTIALLY NON-COSMETIC. WKB/geometric quantization is Archimedean.**

---

## TIER 4: BORDERLINE/AMBIGUOUS PREDICTIONS

*These predictions contain π or exp, but the Archimedean constant might be cosmetic — or the classification depends on what we treat as fundamental.*

---

### 4.1 The Fine Structure Constant α

#### Archimedean Form

```
α = e²/(4πε₀ħc) ≈ 1/137.035999084
```

#### Cosmetic or Non-Cosmetic?

**Argument for cosmetic**: α is MEASURED. It's a dimensionless number. The π in its definition (4π) is purely a convention for defining the coupling strength. If we define g² = e²/(ħc) (no π), then α = g²/(4π), and g² is the "bare" coupling. All physical predictions can be rewritten in terms of α (the measured number) without ever needing to separate the 4π.

**Argument for non-cosmetic**: α itself, AS AN ADELIC OBJECT, would have different values at different places. If α_∞ = 1/137.036, then by the product formula, α_p must be different numbers. The "cosmetic" argument only works if α is taken as a monolithic measured constant — but in the adelic framework, α is a VECTOR with one component per place. The fact that α_∞ happens to be ~1/137 is an ∞-place phenomenon that would be BALANCED by different α_p at other places.

#### Resolution

**α as a measured constant is cosmetic** (Type I) — we measure one number and build theory around it. But α as an adelic object is non-cosmetic (Type II) — different places have different couplings.

The key question: is the RUNNING of α (the β-function) completion-dependent? If yes (as Missarov's p-adic φ⁴ work suggests), then even if α(M_Z) is the same at all places, the UV value α(M_Pl) differs.

**Verdict: AMBIGUOUS — Type I for α as measured constant, Type II for α as adelic vector.**

---

### 4.2 The Anomalous Magnetic Moment (g−2)

#### Archimedean Form

```
a_e = (g_e − 2)/2 = α/(2π) + C₂(α/π)² + C₃(α/π)³ + C₄(α/π)⁴ + ...
```

where a_e(theory) = 1159652181.78(77) × 10⁻¹² (as of 2023).

#### Cosmetic or Non-Cosmetic?

The Schwinger term α/(2π) contains π. But α is measured, and α/(2π) is just α × (1/(2π)). If α is cosmetic (§4.1), then α/(2π) = g²/(8π²) — which still contains π² in the denominator.

However: the coefficient 1/2 in the Schwinger term is NOT cosmetic — it's the specific number that comes out of the one-loop vertex correction. In the p-adic theory, the one-loop vertex correction would involve p-adic loop integrals with DIFFERENT normalization, giving a different coefficient.

If we compute (g−2)_p using p-adic QED, we would get:

```
a_e^{(p)} = C_p^{(1)} α_p + C_p^{(2)} α_p² + ...
```

where C_p^{(1)} ≠ 1/(2π). The coefficients genuinely differ because the loop integrals differ.

**Verdict: TYPE II for the COEFFICIENTS (C₂, C₃, ...) — these come from loop integrals with π. The Schwinger term 'α/(2π)' is a specific number (≈ 0.0011614) that would differ p-adically.**

---

### 4.3 The Lamb Shift

#### Archimedean Form

The Lamb shift (2S_{1/2} − 2P_{1/2} in hydrogen):

```
ΔE = (α/3π) (ħ/mc)² (4πħ²/m) [log(mc²/ΔE) + ...] ≈ 1057 MHz
```

#### π Trace

The α/(3π) comes from the electron self-energy diagram (one-loop vertex correction). The 4π inside comes from additional factors. Multiple π factors from multiple loop integrals.

#### Cosmetic or Non-Cosmetic?

The same analysis as g−2 (§4.2): the loop integral coefficients contain π from the Archimedean evaluation. In p-adic QED, the same diagrams would produce different coefficients.

**Verdict: TYPE II — the loop coefficients differ, but the measured value (1057 MHz) already incorporates the Archimedean coefficients. A "p-adic hydrogen atom" would have a different Lamb shift.**

---

### 4.4 The Cosmological Constant Hierarchy

#### Archimedean Form

```
Λ / M_Pl⁴ ≈ 10⁻¹²²
```

#### π Trace

The zero-point energy calculation:

```
ρ_vac = (1/2) ∫ d³k/(2π)³ √(k² + m²) ∼ Λ_cutoff⁴/(16π²)
```

The 1/(16π²) comes from the solid angle 4π and Fourier normalization π factors.

#### Cosmetic or Non-Cosmetic?

**If the zero-point energy is the origin of Λ**: The 1/(16π²) is non-cosmetic — it's a loop integral result. In p-adic theory, the zero-point energy has a different coefficient.

**BUT**: The cosmological constant problem is that the CALCULATED zero-point energy is 10¹²² times larger than the OBSERVED Λ. This means either:
1. The calculation is wrong (supersymmetry cancellation, or something deeper)
2. There's a fine-tuning that cancels the zero-point piece to 122 decimal places

If the resolution is adelic — the zero-point energies at ALL places sum to zero by the product formula — then the observed 10⁻¹²² is the ∞-place residual after near-perfect cancellation. In this case, the tiny number IS a non-cosmetic adelic prediction.

**Verdict: SPECULATIVE — potentially the most exciting Type II prediction of the entire programme, but requires a working theory of adelic gravity.**

---

### 4.5 Black Hole Entropy and Temperature

#### Archimedean Form

Schwarzschild black hole:
```
S_BH = A/(4G) = 4π M² / M_Pl²    (in Planck units)
T_H = 1/(8πM)                    (in Planck units)
```

#### π Trace

- S_BH: The 4π comes from the area of the horizon sphere: A = 4πr_s² = 16πG²M²
- T_H: The 8π comes from the surface gravity κ = 1/(4GM), and T = κ/(2π)

#### Cosmetic or Non-Cosmetic?

The area-entropy law S = A/4 might be topological (completion-independent). But:
- In p-adic geometry, a "sphere" is a totally disconnected clopen set
- Its "area" (Haar measure of the boundary) scales differently
- The 1/4 in S = A/4 might be universal (from the Euclidean path integral), or it might depend on the completion

If p-adic general relativity exists, the Bekenstein-Hawking formula might become:
```
S_BH^{(p)} = C_p · M² / M_Pl²     where C_p ≠ 4π
```

**Verdict: AMBIGUOUS — depends on the p-adic formulation of gravity. The area-entropy proportionality might be universal, but the coefficient may not be.**

---

### 4.6 The Factor 2π in Quantum Hall Conductance

#### Archimedean Form

```
σ_H = ν e²/h = ν/(2π)    (in units where e = ħ = 1)
```

The von Klitzing constant R_K = h/e² = 25812.80745... Ω.

#### π Trace

The 2π comes from the relationship ħ = h/(2π). In natural units with e = ħ = 1, the conductance quantum is e²/h = 1/(2π).

#### Cosmetic or Non-Cosmetic?

If we work in units where h = 1 (not ħ = 1), the 2π disappears: R_K = 1/e². The π is purely a choice of which constant (h or ħ) we set to 1. This is COSMETIC.

However, the CHERN NUMBER (topological invariant) giving the quantized Hall conductance is an integer. The conversion from Chern number to conductivity involves e²/h. If the Chern number is defined p-adically, the conversion factor would involve p-adic constants.

**Verdict: MOSTLY COSMETIC — the 2π is a unit convention. The quantization (integer filling factors) is topological and universal.**

---

## 5. CROSS-CUTTING ANALYSIS

### 5.1 The Three Root Mechanisms of Non-Cosmetic π

| Mechanism | π's Role | Examples | Universality |
|:---|:---|:---|:---|
| **ζ(s) evaluation** | π^{2n} from ζ(2n) = rational × π^{2n} | SB, Casimir, Basel sums | π is the value of ζ at even integers — mathematical fact, not convention |
| **Loop integral normalization** | π^{d/2} from spherical volume | β-functions, g−2 coefficients, Lamb shift | Every loop in QFT contributes π factors — structurally unavoidable |
| **Geometric integration** | π from surface area of sphere | Solid angle 4π, Coulomb law normalization, BH entropy area | Sphere area is topological in ℝ^n but different in ℚ_p^n |

### 5.2 The Three Root Mechanisms of Existential Failure

| Mechanism | Why It Fails in ℚ_p | Examples |
|:---|:---|:---|
| **Ordering** | ℚ_p is not an ordered field | Causality, θ(t), time evolution, S-matrix |
| **Connectedness** | ℚ_p is totally disconnected | Continuous paths, WKB orbits, Berry phase, Lie group actions |
| **Exponential domain** | p-adic exp converges only on restricted domain | Global time evolution, Boltzmann factor, Planck spectrum shape |

### 5.3 The Stefan-Boltzmann–Casimir–Zeta Trifecta

The strongest non-cosmetic predictions all share the same mathematical origin: **ζ(s) evaluation at specific values**. 

```
Stefan-Boltzmann:  ζ(4)  = π⁴/90  →  σ = π²k⁴/(60ħ³c²)
Casimir:           ζ(−3) = 1/120  →  F = π²ħc/(240a⁴)   [note: π² still appears after regularization]
Planck spectrum:   ζ(4)  = π⁴/90  →  total energy density
Wien:              root of x = 5(1−e⁻ˣ) involving exp
```

In each case, the Archimedean ζ-function produces a specific number. The p-adic ζ-function ζ_p(s) produces a different number. There is no free parameter to align them. **These are the programme's strongest falsifiable predictions.**

### 5.4 The β-Function/Critical Exponent Trifecta

The second strongest category involves RG flow:

```
φ⁴ β-function coefficient
φ⁴ critical exponents (ν, η, γ, β)
φ⁴ anomalous dimensions (γ_φ, γ_m²)
```

All involve loop integrals with spherical volume elements → π factors. Missarov's work demonstrates that p-adic φ⁴ has different β-function coefficients. This means the running of couplings and the critical behavior are completion-dependent.

**If we could build a material whose low-energy physics is governed by p-adic rather than Archimedean φ⁴, it would show different critical exponents at its phase transition.**

---

## 6. THE FALSIFIABILITY MATRIX

### 6.1 Directly Falsifiable (via Measurement)

| Prediction | Archimedean Value | p-adic Status | Can We Test It? |
|:---|:---|:---|:---|
| Stefan-Boltzmann σ | π²k⁴/(60ħ³c²) | Different | ❌ Cannot build p-adic blackbody |
| Casimir force coefficient | π²/240 | Different | ❌ Cannot build p-adic Casimir plates |
| β-function coefficients | 3/(16π²), etc. | Different (Missarov) | ❌ Cannot build p-adic QFT lab |
| Critical exponents | 20+ digits from bootstrap | Different | ❌ Cannot build p-adic material |
| g−2 coefficients | C₂=1/2, C₃, C₄... | Different | ❌ Cannot measure p-adic g−2 |

**All Tier 1–3 predictions are UNFALSIFIABLE by direct experiment** because we cannot construct a p-adic laboratory. This is not a defect of the programme — it's a feature of the question. The programme is about what WOULD differ, not what we can currently measure.

### 6.2 Indirectly Constraining (via Product Formula)

The true falsification path is through the **adelic product formula**:

```
∏_v |Prediction_v|_v = 1
```

If this constraint forces relationships between ∞-place and p-adic values, and if the ∞-place values are known, we can PREDICT (some function of) the p-adic values. The product formula becomes a selection rule for which ∞-place configurations are physically allowed.

**Examples of productive constraints:**

1. **α⁻¹ ≈ 137**: If α is an adelic quantity, the product formula constrains α_p, and in turn constrains α_∞. The proximity to 137 might be explained (or ruled out).

2. **Mass hierarchies**: If m_e/M_Pl ≈ 4.2 × 10⁻²³ is the ∞-place component of an adele, the product formula requires balancing values at p-adic places. This could explain or constrain the hierarchy.

3. **Cosmological constant**: If Λ/M_Pl⁴ ≈ 10⁻¹²² is constrained by adelic cancellation, the product formula makes a prediction about p-adic vacuum energies.

### 6.3 The Best Falsification Path: ZBW as p-Adic Observable

The existing QNFO adelic physics programme (ZBW-Majorana papers P1–P7) provides the most concrete falsification path: if Zitterbewegung shows p-adic spectral signatures (ultrametric clustering, Bruhat-Tits structure), that would be direct evidence that p-adic completions are physically relevant. The non-cosmetic predictions in this catalog would then become empirically meaningful.

---

## 7. SUMMARY TABLE: ALL NON-COSMETIC PREDICTIONS

| # | Prediction | Tier | π Type | p-Adic Differential Δ_p | Falsifiability |
|:--|:---|:---|:---|:---|:---|
| 1 | Stefan-Boltzmann constant σ | 1 — Numeric | ζ(4) emergence | O(1) — different coefficient | ⬜ Indirect (product formula) |
| 2 | Casimir force coefficient π²/240 | 1 — Numeric | ζ(−3) regularization | O(1) — different coefficient | ⬜ Indirect |
| 3 | Basel summations ζ(2n) | 1 — Numeric | Mathematical truth | 100% — completely different numbers | ✅ Mathematical |
| 4 | Wien displacement constant | 1 — Numeric | exp transcendental root | O(1) — different peak | ⬜ Indirect |
| 5 | Loop integral volumes π^{d/2} | 1–2 | Spherical volume | Varies with loop number L | ⬜ Indirect |
| 6 | β-function coefficients | 2 — Structural | Loop π | Known to differ (Missarov) | ⬜ Indirect |
| 7 | Critical exponents (ν,η,γ,β) | 2 — Structural | Loop π + RG | Different universality class | ⬜ Indirect |
| 8 | Anomalous dimensions γ_φ | 2 — Structural | Loop π | Different recursion | ⬜ Indirect |
| 9 | Feynman propagator causality | 2 — Structural | Ordering + iε | Structurally absent | ✅ Conceptual |
| 10 | S-matrix / LSZ reduction | 2 — Structural | All components | Different S-matrix | ⬜ Indirect |
| 11 | Uncertainty principle constant | 2 — Structural | Fourier normalization | C_p ≠ 1/2 (debated) | ⚠️ Borderline |
| 12 | Time ordering / causality | 3 — Existential | ℚ_p not ordered | Concept fails | ✅ Conceptual |
| 13 | exp-based time evolution | 3 — Existential | p-adic exp domain | Local only, not global | ✅ Conceptual |
| 14 | Continuous symmetries / Noether | 3 — Existential | Totally disconnected | Different structure | ✅ Conceptual |
| 15 | WKB / Bohr-Sommerfeld | 3 — Existential | No closed orbits | Quantization fails | ✅ Conceptual |
| 16 | Fine structure α (as adelic) | 4 — Borderline | Depends on interpretation | Different α_p | ⬜ Product formula constraint |
| 17 | Anomalous moment (g−2) coefficients | 4 — Borderline | Loop integrals | Different C_n | ⬜ Indirect |
| 18 | Lamb shift coefficients | 4 — Borderline | Loop integrals | Different | ⬜ Indirect |
| 19 | CC hierarchy 10⁻¹²² | 4 — Speculative | Adelic cancellation | Possibly explanatory | ⚠️ Highly speculative |
| 20 | BH entropy 4π coefficient | 4 — Borderline | Horizon geometry | C_p ≠ 4π (if p-adic GR exists) | ⚠️ Speculative |
| 21 | Quantum Hall 2π factor | 4 — Mostly Cosmetic | Unit convention | Absorbable into ħ vs h | ✅ Cosmetic |

---

## 8. THE PROGRAMME'S CORE PREDICTION

> **If physics is fundamentally defined over ℚ (or a finite extension), and if the observed ∞-place values are projections of adelic objects, then the Stefan-Boltzmann constant, Casimir force coefficient, and β-function coefficients at the ∞-place are constrained by the product formula ∏_v |·|_v = 1 across all completions.**

This means:

1. **σ is not arbitrary** — it must satisfy the adelic constraint with its p-adic counterparts
2. **The Casimir coefficient π²/240 is not arbitrary** — it's the ∞-place projection of an adelic zeta value
3. **The running of couplings (β-functions) at the ∞-place is locked to the p-adic β-functions**
4. **The cosmological constant hierarchy may be the ∞-place shadow of adelic near-cancellation**

The next step is to make these constraints **quantitative**: given the product formula and the structure of the p-adic zeta function, can we compute bounds on σ, the Casimir coefficient, or α?

---

## 9. OPEN PROBLEMS AND NEXT STEPS

### 9.1 Immediate Computational Targets

1. **σ_p for p = 2, 3**: Attempt explicit computation of the p-adic Stefan-Boltzmann coefficient using p-adic phase space integration + p-adic Bose-Einstein distribution (even if approximate or formal).

2. **Casimir C_p**: Construct the p-adic Casimir energy using ζ_p-regularization. Compare C_p to C_∞ = π²/240.

3. **Missarov β-function coefficients**: Extract numerical values for p-adic φ⁴ β-function coefficients from the literature and compare to 3/(16π²) ≈ 0.01899.

4. **Product formula constraint on α**: If α⁻¹_∞ ≈ 137.036 and α_p ≈ 1 for most p, compute what the product formula predicts for the "missing" p-adic contributions.

### 9.2 Conceptual Hard Problems

1. **Causality in ℚ_p**: Is there a p-adic notion of time ordering? Possible approaches: ultrametric time (crystalline time), p-adic worldline parametrization, or abandoning causality as an ∞-place emergent phenomenon.

2. **p-adic Noether**: Can conserved currents be defined without continuous symmetry? Possibly via algebraic (Hopf algebra) approaches or p-adic differential operators.

3. **p-adic gravity**: Does p-adic general relativity exist? The Einstein-Hilbert action involves integration with √−g, which assumes smooth manifolds. p-adic manifolds (rigid analytic spaces) are very different.

### 9.3 Publication Targets

- The Stefan-Boltzmann–Casimir–Zeta trifecta is the strongest material for a paper
- The β-function/critical exponent comparison is the second strongest
- The causality problem is the deepest conceptual challenge and deserves its own paper

---

## References

### Internal Documents
- `completion-failures-ostrowski.md` — Programme specification, Categories A-D
- `pi-adelic-decomposition.md` — π deep-dive, solid angle, Type I vs II
- `adelic-constraint-engine.md` — Catalog expansion A-G, p-adic Gaussian integral, α engine

### Key Literature
- Vladimirov, Volovich, Zelenov (1994): *p-adic Analysis and Mathematical Physics*
- Missarov (1989): p-adic φ⁴ theory and RG
- Lerner-Missarov (1989): p-adic φ⁴ fixed points
- Kubota-Leopoldt (1964): p-adic L-functions and ζ_p(s)
- Koblitz (1984): *p-adic Numbers, p-adic Analysis, and Zeta-Functions*
- Dragovich et al.: Adelic quantum mechanics

### QNFO Adelic Programme
- ZBW-Majorana Papers P1–P7 (Zenodo DOIs, 2026)
- `zbw-majorana-tqc-p7-grand-synthesis` — Adelic physics grand synthesis
- `fine-structure-constant-cross-ratio` — α as cross-ratio, adelic extension §7.7

---

*Document status: ACTIVE | Next: p-adic Feynman propagator construction, Casimir p-adic analog, α engine implementation, causality problem*
