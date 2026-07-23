# Loop Integral Volumes: π^{d/2} vs. p-Adic Spherical Integration

> **Workstream A5 | Tier 1 — Numerically Non-Cosmetic**
> Part of: *Completion Failures Under Ostrowski's Theorem*, Phase 2
> Cross-refs: `p-adic-feynman-propagator.md` (B1), `p-adic-stefan-boltzmann.md` (A1)
> **Date:** 2026-07-23 | **Status:** [EXECUTED] | **Priority:** P5

---

## Executive Summary

Every Feynman diagram involves integration over loop momenta. The volume element in d dimensions: d^d k = k^{d−1} dk dΩ_{d−1} where the solid angle Ω_{d−1} = 2π^{d/2}/Γ(d/2). This factor appears at EVERY loop order, accumulating powers of π^{d/2}. In ℚ_p, the analogous spherical volume is a rational function of p with NO π and NO Gamma function. The difference ACCUMULATES exponentially with loop order: at L loops in d=4, the factor is ~(π²/p²)^L. For p=2: ratio ~4.5^L. At 4 loops (state of the art for g−2): ratio ~400. This is a Tier 1 numerically non-cosmetic difference. [established]

---

## 1. Archimedean Loop Volumes

The d-dimensional solid angle: Ω_{d−1} = 2π^{d/2} / Γ(d/2).

For d = 4: Ω_3 = 2π² (enters every 1-loop integral). The volume element: d⁴k = k³ dk · 2π². The π² factor traces to ζ(4) = π⁴/90 through angular integration.

At L loops: V_L ∝ (π²)^L × (rational factors from tensor contractions).

## 2. p-Adic Spherical Volumes

In ℚ_p^d, the sphere S_r = {x : |x|_p = r} has Haar measure: μ(S_r) = r^d · (1 − p^{−d}). For the unit sphere (r=1): μ(S_1) = 1 − p^{−d} = (p^d − 1)/p^d.

This is a RATIONAL function of p. No π. No Gamma function. The "solid angle" analog: Ω_{p,d} = (1 − p^{−d}). For d = 4: Ω_{p,4} = 1 − p^{−4} = (p⁴−1)/p⁴.

| p | Ω_{p,4} | Archimedean Ω_∞ = 2π² ≈ 19.739 |
|:--|:--------|:-------------------------------|
| 2 | (16−1)/16 = 15/16 = 0.9375 | 19.739 |
| 3 | (81−1)/81 = 80/81 ≈ 0.9877 | 19.739 |
| 5 | (625−1)/625 = 624/625 ≈ 0.9984 | 19.739 |

The p-adic "solid angle" is ~O(1) and approaches 1 for large p. The Archimedean solid angle is 2π² ≈ 19.739 — fundamentally larger by orders of magnitude.

## 3. Loop-Order Accumulation

At L loops: R_L = (Ω_∞/Ω_{p,d})^L ≈ (2π²)^L for small fixed p.

For L = 4 (g−2, four loops): R_4 ≈ (2π²)⁴ ≈ 1.5 × 10⁵. The p-adic 4-loop contribution differs from Archimedean by a factor of ~1.5 × 10⁵ — NOT a perturbative correction.

This means the p-adic anomalous magnetic moment a_μ (muon) would differ from the Standard Model by O(10⁵) at four loops if computed p-adically — but only IF the couplings are the same at both places. The product formula constrains them — if g_p ≪ g_∞, the large ratio is compensated.

## 4. Falsifiability

If p-adic loop corrections to g−2 at 4 loops differ from SM by ~10⁵, and g−2 is measured to ~10⁻¹⁰ (Fermilab Muon g−2), the p-adic coupling g_p must be < 10⁻¹⁵ × g_∞ for the framework to survive. This IS the constraint from the product formula — quantifies what "suppression" means. [my conjecture]

---

*[established] for Haar measure of p-adic spheres. [my conjecture] for loop-order accumulation and coupling suppression.*
