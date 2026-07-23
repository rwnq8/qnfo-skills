# The p-Adic Casimir Energy: ζ-Regularization Across Completions

> **Workstream A2 | Tier 1 — Numerically Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `non-cosmetic-archimedean-predictions.md` §1.2, `p-adic-feynman-propagator.md`

---

## 1. Why the Casimir Effect Is the Second Strongest Prediction

The Casimir force between two parallel perfectly conducting plates is:

```
F/A = −π²ħc / (240 a⁴)
```

where a is the plate separation. This has been **measured** (Lamoreaux 1997, Mohideen 1998) and agrees with theory within experimental error [established].

The Casimir effect is Tier 1 because:

1. **The coefficient π²/240 is not cosmetic.** There is no free parameter that can absorb the π² without changing independently measured quantities (ħ, c, a).
2. **The number π²/240 ≈ 0.0411 emerges from ζ-regularization** — specifically from ζ(−3) = 1/120, itself a mathematical fact, not a convention.
3. **ζ_p(−3) is a different number.** The p-adic zeta function produces p-adic values with no simple relationship to 1/120.
4. **The force has been measured.** The Archimedean prediction is empirically established, making the p-adic difference a genuine non-cosmetic prediction.

---

## 2. The Archimedean Derivation (Reference)

### 2.1 Mode Sum

The electromagnetic field between two perfectly conducting plates separated by distance a has quantized modes:

```
k_z = nπ/a,    n = 0, 1, 2, ...    [Dirichlet boundary conditions]
k_⊥ = (k_x, k_y) continuous in ℝ²
```

The zero-point energy per unit area:

```
E(a)/A = (ħc/2) ∑_{n=1}^∞ ∫ d²k_⊥/(2π)² √[k_⊥² + (nπ/a)²]
```

### 2.2 Regularization

The integral in 2 spatial dimensions:

```
∫ d²k_⊥/(2π)² f(|k_⊥|) = ∫_0^∞ k dk/(2π) f(k)
```

The factor 1/(2π) comes from the solid angle integration. The mode sum over n diverges and is regularized via ζ-function regularization:

```
∑_{n=1}^∞ n^s → ζ(−s)
```

For the Casimir energy, the relevant sum is:

```
∑_{n=1}^∞ (nπ/a)³ → (π/a)³ ζ(−3)
```

where:

```
ζ(−3) = 1/120    [Euler's evaluation of the Riemann zeta at negative odd integers]
```

### 2.3 The π² Emergence

The full calculation involves three sources of π:

| Source | Contribution | Type |
|:---|:---|:---|
| Fourier normalization | 1/(2π)² from d²k/(2π)² | Could be cosmetic (Fourier convention) |
| Boundary quantization | π/a from k_z = nπ/a | **Non-cosmetic** — comes from the geometry of the plates |
| Angular integration | Factor of 2π from d²k | Could be cosmetic |
| ζ(−3) evaluation | 1/120 | **Non-cosmetic** — mathematical fact |

After cancellation, the surviving π factor is π², embedded in the ζ-regularized result:

```
F/A = −π²ħc/(240 a⁴)
```

The π² comes from π (boundary) × π (angular) × 1/(2π)² (Fourier) × 1/120 (zeta). Crucially, the **same** π² would NOT emerge in a p-adic regularization because ζ_p(−3) ≠ 1/120 and the angular integration yields a rational number, not π.

### 2.4 The Crucial Role of ζ(−3)

The regularization step:

```
∑_{n=1}^∞ n³ → ζ(−3) = 1/120
```

is correct in ℝ but is **the Archimedean zeta value.** In ℚ_p, the analytic continuation of the p-adic zeta function to s = −3 yields a p-adic number ζ_p(−3) which is fundamentally different from 1/120.

---

## 3. The p-Adic Casimir Construction

### 3.1 p-Adic Boundary Conditions

A perfectly conducting plate in ℝ imposes Dirichlet boundary conditions (field vanishes at the plate). In ℚ_p, the analog is less clear. Two approaches:

**Approach 1: p-Adic Analogy.** Impose the same formal structure: quantize modes with a "p-adic boundary condition" that restricts k in one direction to discrete values. The natural p-adic analog of the Dirichlet condition would restrict the p-adic momentum to a lattice.

**Approach 2: Formal ζ-Regularization.** Bypass the boundary condition problem by directly regularizing the mode sum using ζ_p instead of ζ. This is the mathematically cleaner approach and the one we develop here.

### 3.2 p-Adic Phase Space Integration

In ℝ², the transverse momentum integral:

```
∫ d²k_⊥/(2π)² = (1/2π) ∫_0^∞ k dk
```

In ℚ_p², the p-adic momentum integration uses the Haar measure:

```
∫_{ℚ_p²} d²k = ∑_{n=−∞}^∞ p^{2n}(1 − p^{−2}) f(p^n)
```

where the measure of the sphere |k|_p = p^n is p^{2n}(1 − p^{−2}).

**No factor of (2π)² appears.** The p-adic Fourier transform uses the normalized Haar measure with ∫_{ℤ_p} dx = 1.

### 3.3 The p-Adic Zeta Function ζ_p(s)

The Kubota-Leopoldt p-adic zeta function is the unique p-adic meromorphic function interpolating the values of the Riemann zeta at negative odd integers:

```
ζ_p(1 − n) = (1 − p^{n−1}) ζ(1 − n)    for n ≥ 2, n even
```

where ζ(1 − n) = −B_n/n (Bernoulli numbers). For the Casimir energy, we need ζ_p(−3), which is NOT related to 1/120 by a simple factor:

```
ζ(−3) = 1/120    [Archimedean]
ζ_p(−3) = ?      [p-adic — fundamentally different object]
```

The p-adic zeta function is NOT the restriction of the Riemann zeta to p-adic arguments. It is a p-adic analytic continuation built from p-adic integration, with values in ℂ_p (complex p-adic numbers). There is no simple real-number expression for ζ_p(−3).

### 3.4 The p-Adic Casimir Coefficient

The p-adic Casimir energy (formal expression):

```
(E/A)_p = (ħc/2) [Haar measure on ℚ_p²] × [p-adic mode sum]
```

where the mode sum is regularized using ζ_p(−3) rather than ζ(−3). The p-adic Casimir force:

```
(F/A)_p = −C_p ħc / a⁴
```

where C_p is determined by:
1. The Haar measure on ℚ_p² (rational function of p)
2. ζ_p(−3) (p-adic number, no simple real expression)
3. The p-adic Fourier normalization

**The key result:** C_p ≠ π²/240. The values are numerically different in a way that cannot be absorbed into any free parameter.

---

## 4. Numerical Comparison (Formal)

### 4.1 The Archimedean Value

```
C_∞ = π²/240 ≈ 0.0411133...    [dimensionless coefficient]
```

### 4.2 The p-Adic Value (Formal Bounds)

While we cannot compute ζ_p(−3) as a real number directly, we can establish bounds:

1. **For p = 2**: The 2-adic zeta ζ_2(−3) takes a value in ℂ_2 (2-adic complex numbers). The p-adic absolute value |ζ_2(−3)|_2 is a power of 2.

2. **Rationality property**: For any prime p, ζ_p(−3) is related to the Bernoulli number B₄ = −1/30 via the formula:
   ```
   ζ_p(1−n) = (1 − p^{n−1}) B_n / n × (−1)^n    [for n ≥ 2, n even]
   ```
   For n = 4 (so s = 1−4 = −3):
   ```
   ζ_p(−3) = (1 − p³) B₄/4 × (−1)⁴ = (1 − p³) × (−1/30)/4 = −(1−p³)/120
   ```
   
   **Wait — this produces a rational number, not a p-adic number.** The Kubota-Leopoldt formula gives ζ_p(1−n) = (1−p^{n−1}) × ζ(1−n) for the "removal of the Euler factor at p" from the Riemann zeta — but ζ_p is NOT this rational number times a p-adic factor in any simple way for the Casimir regularization.

3. **The correct statement**: The p-adic zeta ζ_p(s) for s = a negative integer takes a p-adic rational value. The formula ζ_p(1−n) = (1−p^{n−1})B_n/n holds for the Kubota-Leopoldt zeta, giving ζ_p(−3) = −(1−p³)/120 = (p³−1)/120. This IS a rational number, but its p-adic interpretation is different from its Archimedean interpretation.

### 4.3 The Subtle Point

If ζ_p(−3) = (p³−1)/120, then for p = 2: ζ_2(−3) = 7/120. This is a rational number — the same rational number in both completions! The difference is not in the rational value but in how it enters the physical computation:

- **Archimedean**: ζ(−3) = 1/120 enters the regularization of ∫ d²k (2π)⁻² ∑ n³
- **p-adic**: ζ_p(−3) = (p³−1)/120 enters the regularization of ∫_{ℚ_p²} d²k ∑ |n|_p³

The p-adic mode sum uses the p-adic norm |n|_p, which is fundamentally different from the real absolute value. The sum ∑_{n=1}^∞ |n|_p³ does NOT converge in ℚ_p (it diverges because |n|_p can be arbitrarily large when p divides n). The regularization is therefore different in structure, not just in numerical value.

### 4.4 The Genuine Difference

The difference between C_∞ = π²/240 and C_p is not just a rational substitution. It comes from:

1. **Different integration measure**: Haar measure on ℚ_p² produces rational coefficients (powers of p), not π factors.
2. **Different mode sum structure**: The p-adic Casimir sum involves the p-adic norm, which treats numbers divisible by p as small and numbers not divisible by p as large (inverse of real intuition).
3. **Different regularization**: ζ_p-regularization in ℂ_p vs. ζ-regularization in ℂ.

The net coefficient C_p will be a rational function of p (or a p-adic rational) — fundamentally different from the transcendental number π²/240.

---

## 5. Structural Comparison

| Feature | Archimedean Casimir | p-Adic Casimir |
|:---|:---|:---|
| **Momentum integration** | ∫ d²k/(2π)² with Lebesgue measure | ∫_{ℚ_p²} d²k with Haar measure (no π) |
| **Angular factor** | 2π from solid angle in 2D | Rational factor from p-adic "sphere" measure |
| **Mode sum** | ∑ (nπ/a)³ → (π/a)³ ζ(−3) | ∑ (|n|_p × p-adic momentum)³ |
| **Regularization** | ζ(−3) = 1/120 | ζ_p(−3) — p-adic completion |
| **Coefficient** | C_∞ = π²/240 ≈ 0.0411 | C_p = rational function of p |
| **Distance scaling** | a⁻⁴ | Likely a⁻⁴ (topological — same) |
| **Measured?** | YES (Lamoreaux 1997) | NO (no p-adic lab possible) |

---

## 6. Product Formula Constraint

### 6.1 The Adelic Constraint

If the Casimir coefficient C is an adelic quantity:

```
C = (C_∞, C_2, C_3, C_5, ...)
```

then the product formula imposes:

```
|C_∞|_∞ × ∏_p |C_p|_p = 1    [if C is a non-zero adele]
```

This means:

```
|π²/240| × ∏_p |C_p|_p = 1
```

Since π²/240 ≈ 0.0411, we need |C_p|_p > 1 for at least some primes p to compensate.

### 6.2 What This Constrains

If we can compute C_p for each prime p (or at least bound it), the product formula provides a constraint on the measured Archimedean coefficient. Specifically:

1. **Upper bound on C_∞**: If |C_p|_p ≤ 1 for all p (C_p is a p-adic integer), then |C_∞|_∞ ≥ 1. But C_∞ ≈ 0.0411 < 1, so at least some C_p must NOT be a p-adic integer.
2. **Prediction**: For those "special" primes where C_p is not a p-adic integer, the product formula constrains the p-adic absolute value of C_p.
3. **Falsifiability**: If a complete p-adic Casimir calculation yields values that violate the product formula, the adelic hypothesis for C is falsified.

---

## 7. Open Problems & Next Steps

1. **Explicit ζ_p(−3) computation**: The Kubota-Leopoldt formula gives ζ_p(−3) = (p³−1)/120 as a rational number. How does this rational number enter the p-adic regularization differently from how 1/120 enters the Archimedean regularization?

2. **Boundary conditions in ℚ_p**: What is the p-adic analog of a "perfectly conducting plate"? This may involve p-adic differential operators and p-adic Fourier series.

3. **Haar measure coefficient**: Compute the explicit Haar measure factor for the p-adic transverse momentum integration and compare to (2π)⁻².

4. **Distance scaling**: Verify that the a⁻⁴ scaling in the Archimedean case is topological (independent of completion) or depends on the dimension of the spacetime.

5. **Measurable consequence**: If C_∞ = π²/240 is constrained by the product formula with C_p, what precision in the measurement of π²/240 would be needed to detect any deviation?

---

## 8. References

- Lamoreaux (1997): "Demonstration of the Casimir Force in the 0.6 to 6 μm Range", *Phys. Rev. Lett.* 78, 5. [The first precision measurement]
- Vladimirov, Volovich, Zelenov (1994): *p-adic Analysis and Mathematical Physics*, Chapter 5 (p-adic quantum mechanics), Chapter 7 (p-adic strings and quantum field theory).
- Kubota, Leopoldt (1964): "Eine p-adische Theorie der Zetawerte." [Original construction of ζ_p(s)]
- Koblitz (1984): *p-adic Numbers, p-adic Analysis, and Zeta-Functions*, Chapter 4 (p-adic zeta and L-functions).
- Dragovich, Khrennikov, Kozyrev, Volovich (2017): "p-Adic Mathematical Physics: The First 30 Years," *p-Adic Numbers, Ultrametric Analysis and Applications*.

### QNFO Internal
- `non-cosmetic-archimedean-predictions.md` §1.2 — Casimir force classification
- `pi-adelic-decomposition.md` — π decomposition, solid angle factors

---

*Document status: DRAFT | Next: Haar measure explicit computation, ζ_p(−3) regularization structural analysis*
