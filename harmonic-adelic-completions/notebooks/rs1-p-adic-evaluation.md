# Notebook: RS-1 α⁻¹ p-Adic Evaluation — Cosmetic vs Non-Cosmetic

**Date:** 2026-07-23
**Context:** The RS-1 decomposition of the fine-structure constant:
α⁻¹(0) ≈ 137.036 = 137 (H_5 numerator) + Δ_adelic + Δ_RG

---

## 1. The Rational Core: p-Adic Properties of H_5 = 137/60

The harmonic number H_5 = 1 + 1/2 + 1/3 + 1/4 + 1/5 = 137/60.

As a rational number, H_5 has well-defined p-adic valuations at every prime:

| Prime p | v_p(137/60) | |137/60|_p | Notes |
|:--------|:-----------|:-------------|:------|
| 2 | −2 | 4 | 60 = 2² × 3 × 5 |
| 3 | −1 | 3 | |
| 5 | −1 | 5 | |
| 137 | +1 | 1/137 | 137 is prime, numerator |
| All other p | 0 | 1 | Trivial |

### 1.1 Product Formula Verification

For any nonzero rational r: ∏_v |r|_v = 1 (over all places including ∞).

For r = 137/60:
- |137/60|_∞ = 137/60 ≈ 2.28333...
- |137/60|_2 = 4
- |137/60|_3 = 3
- |137/60|_5 = 5
- |137/60|_137 = 1/137
- |137/60|_p = 1 ∀ p ∉ {2,3,5,137}

Product: (137/60) × 4 × 3 × 5 × (1/137) = (137/60) × 60 × (1/137) = 1 ✓

**This holds because H_5 is rational.** Every rational number satisfies this. It's a theorem about ℚ, not about physics.

## 2. The Near-Integer Coincidence

α⁻¹(0) ≈ 137.035999084 (CODATA 2018) ≈ 137.036

The RS-1 decomposition: α⁻¹ ≈ 137 + ε where ε ≈ 0.036

### 2.1 Is α⁻¹ itself rational?

**No.** α⁻¹ is an experimentally measured dimensionless coupling. The renormalization group running makes its exact value dependent on the RG scale. It is not known to be rational, and there is no evidence it is.

Key implication: α⁻¹ does NOT have well-defined p-adic valuations (except as an arbitrary real number, where p-adic valuation of a transcendental real is typically ill-defined or requires analytic continuation).

### 2.2 The Split

The decomposition α⁻¹ = 137 + ε splits into:
- **Rational part (137):** Has well-defined p-adic structure
- **Correction (ε ≈ 0.036):** Is an Archimedean-only quantity

The adelic product formula applies to 137 (trivially, as for any integer), but NOT to α⁻¹ itself.

## 3. Cosmetic vs Non-Cosmetic Test

### 3.1 Definition

A near-integer coincidence is **cosmetic** if:
- The rational core has no special p-adic properties that distinguish it from any other rational with similar Archimedean magnitude
- The correction ε has no p-adic interpretation
- The decomposition provides no falsifiable constraint linking the Archimedean and p-adic values

A near-integer coincidence is **non-cosmetic** if:
- The rational core has p-adic properties that are special (e.g., appears as a factor in the adelic product formula in a non-trivial way)
- The correction ε can be expressed as a sum of p-adically constrained terms
- The decomposition yields a falsifiable prediction that can be tested independently

### 3.2 Test: Is 137 Special p-Adically?

137 is prime. As a prime number, it appears in the product formula with valuation +1. But so does EVERY prime — this is not special.

What WOULD be special: if the p-adic factors of H_5's denominator (|137/60|_2 = 4, |137/60|_3 = 3, |137/60|_5 = 5) encoded physical quantities at those places. There is currently no evidence for this.

### 3.3 Test: Does the Adelic Product Formula Constrain ε?

Hypothetical: if α⁻¹ were exactly given by an adelic formula like α⁻¹ = Σ_p f(|p|_p) where the sum over p-adic contributions plus an Archimedean contribution yields the measured value, then ε ≈ 0.036 would be the Archimedean residue after p-adic contributions are accounted for.

But no such formula exists. The RS-1 decomposition is a phenomenological split (rational core + corrections), not an adelic constraint.

## 4. The Product Formula Applied to the Full Coupling

### 4.1 Can the product formula be applied to α⁻¹?

Only if α⁻¹ ∈ ℚ×. It is not known to be rational.

Even if it WERE rational (say, exactly 82801393/604800 ≈ 136.9... from some speculative formula), the product formula would hold trivially — as it does for every rational. The product formula is a theorem, not a constraint — it doesn't SELECT which rationals are physically realized.

### 4.2 What WOULD Be a Genuine Constraint

A non-trivial adelic constraint would be of the form:

$$\prod_v f_v(\alpha^{-1}; p) = 1$$

Where f_v are place-specific functions of the coupling (not just the absolute value), and the product over all places yields 1 as a consistency condition. The Archimedean factor f_∞ would encode the measured α⁻¹ ≈ 137.036, and the p-adic factors f_p would encode place-specific contributions, with the product tying them together.

**No such construction exists for α⁻¹.**

## 5. Specific Evaluation: The H_5 Rational Core

### 5.1 The p-adic "signal" from H_5

The rational core 137/60 has p-adic valuations at exactly 4 non-Archimedean places: p = 2, 3, 5, 137.

If these primes (2, 3, 5, 137) play a special role in the physics of α, that would be non-cosmetic evidence. Let's check:

- **p = 2:** The 2-adic norm appears in the Majorana ZBW analysis (P5 adelic QEC uses ℚ_2 specifically). But this is a different physical context (quantum computing, not QED coupling).
- **p = 3:** No known special role in α physics.
- **p = 5:** No known special role in α physics.
- **p = 137:** Trivially special because 137 ≈ α⁻¹. But this is circular — 137 is special because it's close to α⁻¹, not because of p-adic structure.

### 5.2 The Δ_adelic Term

If the RS-1 decomposition were genuinely adelic, we would expect the Bruhat-Tits contribution Δ_adelic to have a well-defined p-adic interpretation (not just be a real number fitted to make the decomposition work).

**The current literature does not provide this.** Δ_adelic is presented as a real-number correction, not a p-adically constrained quantity.

## 6. Verdict

### 6.1 Overall Classification

**The RS-1 α⁻¹ ≈ 137 near-integer coincidence is currently COSMETIC from the p-adic/adélic perspective.**

Reasons:
1. The rational core (137) satisfies the adelic product formula trivially, as every rational does
2. The correction ε ≈ 0.036 has no known p-adic interpretation
3. α⁻¹ is not known to be rational, so the product formula doesn't directly constrain it
4. The primes appearing in H_5's p-adic decomposition (2, 3, 5, 137) have no demonstrated physical connection to α beyond the trivial 137 ≈ α⁻¹
5. No falsifiable prediction emerges from the decomposition that can be tested independently of the fit itself

### 6.2 What Would Change This Assessment

| Evidence needed | Current status |
|:----------------|:---------------|
| α⁻¹ shown to be rational (or a specific algebraic number) | Not known |
| A p-adic interpretation of ε (e.g., as a p-adic regulator) | Not available |
| A product-formula constraint linking α⁻¹ values at multiple places | Not constructed |
| A falsifiable prediction: "if decomposition is non-cosmetic, then X must be observed" | Not formulated |

### 6.3 Calibration

**[my conjecture]** The RS-1 decomposition is a numerological coincidence — a rational approximation (H_5 = 137/60) that happens to produce an integer numerator close to α⁻¹. The decomposition into H_5 numerator + Δ_adelic + Δ_RG is a post-hoc phenomenological fit, not a derivation from adelic principles. The product formula ∏_v |·|_v = 1 applies to 137 trivially (as it does to any integer) and provides no constraint on α⁻¹ itself.

**Disconfirmation:** This would be disconfirmed if (a) a p-adic analogue of the QED β-function is constructed and shown to produce Δ_adelic as a genuine p-adic contribution (not a fitted real number), or (b) the primes 2, 3, 5 are shown to play a demonstrable physical role in QED coupling renormalization.
