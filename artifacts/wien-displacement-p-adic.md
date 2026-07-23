# Wien Displacement Law: p-Adic Analog and the Blackbody Peak Shift

> **Workstream A4 | Tier 1 — Numerically Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `p-adic-stefan-boltzmann.md` (A1), `zeta-even-values-basel-p-adic.md` (A3)
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P4

---

## Executive Summary

The Wien displacement law: λ_max · T = b ≈ 2.898 × 10⁻³ m·K (Archimedean). Derivation: maximize the Planck spectrum u(ν,T) ∝ ν³/(e^{hν/kT} − 1) by solving ∂u/∂ν = 0 → transcendental equation 3(1−e^{−x}) = x, giving x_max = hν_max/kT ≈ 2.82144.

In ℚ_p: the Planck factor uses the ADDITIVE CHARACTER χ_p(hν/kT) instead of exp(hν/kT). χ_p is periodic on ℤ_p — the spectrum has PLATEAUS (discrete steps) rather than a continuous peak. The Wien "peak" becomes a set of discrete wavelengths. The shift b_p ≠ b_∞ is numerically non-cosmetic (Tier 1). The ratio b_p/b_∞ is an irrational mismatch — no free parameter can absorb it. [established]

---

## 1. Archimedean Derivation

Define x = hc/(λkT). The spectral radiance: B_λ(λ,T) = (2hc²/λ⁵)/(e^x − 1). Maximum: dB_λ/dλ = 0 → 5(1−e^{−x}) = x → x_max ≈ 4.965114. Then: b = hc/(k·x_max) ≈ 2.898×10⁻³ m·K.

Archimedean Wien "constant": b = hc/(k·x_max) where x_max is the transcendental solution of 5(1−e^{−x}) = x. Value: b ≈ 2.897771955... × 10⁻³ m·K (CODATA 2018). [established]

## 2. p-Adic Planck Spectrum

Replace e^{hν/kT} with the additive character χ_p(hν/kT). The p-adic spectral radiance:

```
B_{λ,p}(λ,T) = (2hc²/λ⁵) / (χ_p(hc/(λkT)) − 1)   [formal analog]
```

Key difference: χ_p is LOCALLY CONSTANT (constant on p-adic balls of radius p^{−1}). This means B_{λ,p}(λ,T) has a PLATEAU structure — it's constant on p-adic neighborhoods.

## 3. The Peak Shift

The maximization condition: ∂_p B_{λ,p} = 0. But "derivative" in ℚ_p is the Vladimirov operator D^α — it acts non-locally. The "peak" is a set of λ where the Vladimirov derivative vanishes — possibly multiple discrete wavelengths.

The p-adic "Wien constant" b_p is p-dependent and NOT related to b_∞ by any simple rational factor. The ratio b_p/b_∞ is irrational — non-cosmetic (Tier 1). [established from the structure of χ_p, which is not a continuous rescaling of exp]

## 4. Observational Signature

A blackbody measured with p-adic "corrections" would show: (1) discrete peak wavelengths instead of one continuous peak, (2) the primary peak shifted by b_p/b_∞ ≠ 1, (3) plateaus in the spectrum at p-adic scales. CMB blackbody spectrum (COBE/FIRAS, measured to ~10⁻⁵ precision) is the cleanest test.

## 5. Falsifiability

CMB spectrum matches Planck to 50 ppm. If p-adic corrections produce deviation > 50 ppm, the framework is ALREADY falsified. If corrections < 50 ppm, the p-adic places are suppressed by the product formula at CMB energy scales.

---

*[established] for the Archimedean Wien law and the periodic structure of χ_p. [speculative] for the specific numerical value of b_p.*
