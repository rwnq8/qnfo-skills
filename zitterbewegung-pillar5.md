# Pillar 5: CMB and Ultrametric Structure

**Zitterbewegung Cosmology Research Program** | **Author:** Rowan Brad Quni-Gudzinas  
**Date:** 2026-07-12 | **Status:** Draft v0.1

---

## 5.1 The CMB as an Ultrametric Probe

The Cosmic Microwave Background (CMB) is the oldest light in the universe — a snapshot of the universe at $z \approx 1100$, approximately 380,000 years after the Big Bang. Its temperature anisotropies $\Delta T(\hat{n})$ encode the primordial density fluctuations that seeded all cosmic structure [established].

Pillar 2 established that Zitterbewegung cycles correspond to ultrametric tree-depth steps. This pillar develops the observational consequence: the CMB power spectrum should exhibit signatures of the ultrametric (specifically, $p$-adic) structure underlying cosmic expansion [my conjecture].

## 5.2 The CMB Power Spectrum

### 5.2.1 Spherical Harmonic Decomposition

The temperature fluctuations are decomposed in spherical harmonics:

$$\frac{\Delta T(\hat{n})}{T_0} = \sum_{\ell=0}^\infty \sum_{m=-\ell}^\ell a_{\ell m} Y_{\ell m}(\hat{n})$$

The **power spectrum** is the variance of the coefficients:

$$C_\ell = \frac{1}{2\ell + 1} \sum_{m=-\ell}^\ell |a_{\ell m}|^2$$

Under the assumption of statistical isotropy and Gaussianity, the $C_\ell$ completely characterize the CMB [established].

### 5.2.2 Standard Acoustic Peaks

In the standard $\Lambda$CDM model, the $C_\ell$ exhibit acoustic peaks at $\ell \approx 220, 540, 810, \ldots$ (the fundamental and harmonics of baryon acoustic oscillations) [established]. These peaks are well-measured and provide precision constraints on cosmological parameters.

## 5.3 The p-adic Modulation Hypothesis

### 5.3.1 Log-Periodic Oscillations

If the Zitterbewegung tree-depth correspondence (Pillar 2) is correct, the CMB power spectrum should exhibit **log-periodic oscillations** in $\ell$:

$$C_\ell \approx C_\ell^{\text{standard}} \times \left[1 + A \cos\left(2\pi \frac{\log(\ell/\ell_0)}{\log(p)} + \phi\right)\right]$$

where $p$ is a prime number, $A$ is the modulation amplitude, $\ell_0$ is a reference multipole, and $\phi$ is a phase offset [my conjecture].

### 5.3.2 Physical Origin

Log-periodic oscillations arise naturally from discrete scale invariance — a symmetry under scale transformations by factors of $p$. In the ultrametric tree-depth framework, each depth transition corresponds to a factor-of-$p$ change in scale. The cumulative effect of many such transitions produces oscillations in $\log(\ell)$ with period $\log(p)$ [speculative].

### 5.3.3 Prime Signature Identification

The prime responsible for the modulation can be identified by scanning over candidate primes $\{2, 3, 5, 7, 11, \ldots\}$ and measuring the goodness-of-fit of each log-periodic template. The prime with the highest Bayesian evidence (or lowest $\chi^2$) is the candidate "Zitterbewegung prime" [speculative].

**Prediction:** $p = 2$ is the most likely candidate, given that:
1. The Kepler Program (Phase 7) found $p = 2$ coherence in biological quantum systems
2. The 2-adic valuation has the richest tree structure (binary tree at each depth)
3. Binomial coefficient structures in the Mahler expansion (Ultrametric Foundation Ch4) are inherently 2-adic

## 5.4 p-adic Non-Gaussianity

### 5.4.1 The Primordial Bispectrum

Non-Gaussianity in the CMB is characterized by the **bispectrum** — the three-point correlation function of the primordial curvature perturbation $\zeta(k)$:

$$\langle \zeta(k_1) \zeta(k_2) \zeta(k_3) \rangle = (2\pi)^3 \delta^{(3)}(k_1 + k_2 + k_3) B_\zeta(k_1, k_2, k_3)$$

In the ultrametric framework, the bispectrum acquires a $p$-adic modulation when the three wavevectors satisfy $v_p(k_1) = v_p(k_2) = v_p(k_3)$ — i.e., when they lie at the same depth in the ultrametric tree [my conjecture].

### 5.4.2 The Equilateral Configuration

For the equilateral configuration $k_1 \approx k_2 \approx k_3$, the $p$-adic non-Gaussianity is maximal because all three modes occupy the same tree depth. The predicted amplitude is:

$$f_{\text{NL}}^{\text{equil, } p} \approx \frac{1}{p-1}$$

For $p = 2$, this gives $f_{\text{NL}}^{\text{equil}} \approx 1$, which is consistent with current Planck constraints $f_{\text{NL}}^{\text{equil}} = -26 \pm 47$ (68% CL) [speculative].

### 5.4.3 The Squeezed Configuration

In the squeezed limit $k_1 \ll k_2 \approx k_3$, the $p$-adic non-Gaussianity vanishes because the modes occupy different tree depths. This is a distinctive signature: non-Gaussianity present in equilateral but absent in squeezed configurations [speculative].

This prediction is falsifiable by upcoming CMB experiments (Simons Observatory, CMB-S4) and large-scale structure surveys (Euclid, LSST).

## 5.5 The Sachs-Wolfe Effect and Tree-Depth

### 5.5.1 Gravitational Potential Fluctuations

The Sachs-Wolfe effect relates CMB temperature fluctuations to gravitational potential fluctuations at the last scattering surface:

$$\frac{\Delta T}{T}(\hat{n}) \approx -\frac{1}{3}\Phi(\eta_{\text{dec}}, \hat{n} \cdot \eta_{\text{dec}})$$

In the Zitterbewegung framework, the gravitational potential $\Phi$ is itself an aggregate of Zitterbewegung oscillations (Pillar 3), so its fluctuations inherit the ultrametric tree structure [speculative].

### 5.5.2 Integrated Sachs-Wolfe (ISW) Effect

The late-time ISW effect — the change in CMB photon energy as they traverse evolving gravitational potentials — is particularly sensitive to the dark energy equation of state. Since Pillar 4 predicts $w = -1$ from Zitterbewegung zero-point energy, the ISW effect provides an indirect test of the Zitterbewegung dark energy mechanism [speculative].

## 5.6 CMB Polarization and Ultrametric Parity

### 5.6.1 E-mode and B-mode Polarization

CMB polarization is decomposed into E-modes (curl-free, scalar) and B-modes (divergence-free, tensor). Primordial B-modes are the "smoking gun" of inflationary gravitational waves [established].

### 5.6.2 The TB and EB Cross-Spectra

Parity-violating correlations (TB and EB cross-spectra) are expected to vanish in standard $\Lambda$CDM. In the ultrametric framework, a non-zero $p$-adic phase in the Zitterbewegung oscillation can produce parity-violating correlations at the level of:

$$C_\ell^{TB} \approx A_p \cdot C_\ell^{TT} \cdot \sin(\omega_Z t_{\text{dec}})$$

where $t_{\text{dec}}$ is the time of decoupling. This is a distinctive, falsifiable prediction [speculative].

## 5.7 Comparison with Existing Anomalies

### 5.7.1 The CMB Cold Spot

The CMB Cold Spot — a region of unusually low temperature spanning approximately $10^\circ$ — has been interpreted as a statistical anomaly. In the ultrametric framework, it could be a large-scale manifestation of a deep tree-depth transition: a region where Zitterbewegung coherence was lost at a particularly early time [speculative].

### 5.7.2 Hemispherical Power Asymmetry

The observed hemispherical power asymmetry (more power in one hemisphere than the other at large scales) could arise from a global $p$-adic phase gradient imprinted during inflation. The preferred direction would correspond to the gradient of the $p$-adic valuation field [speculative].

### 5.7.3 The Parity Asymmetry

The observed odd-parity preference in the CMB (more power in odd $\ell$ than even $\ell$ at low multipoles) is a natural consequence of the ultrametric tree structure: odd $\ell$ correspond to antisymmetric modes that sample opposite sides of the tree, while even $\ell$ correspond to symmetric modes that sample the same side [speculative].

## 5.8 The CMB Test Protocol

The following is a pre-registered analysis protocol for testing the ultrametric CMB predictions:

1. **Log-periodic scan:** Fit $C_\ell$ data with template $C_\ell = C_\ell^{\Lambda\text{CDM}} \times [1 + A \cos(2\pi \log_p(\ell/\ell_0) + \phi)]$ for $p \in \{2, 3, 5, 7, 11, 13\}$
2. **Bayesian model comparison:** Compare $\Lambda\text{CDM} + \text{modulation}$ against $\Lambda\text{CDM}$ using the Bayesian evidence ratio
3. **Bispectrum search:** Template $f_{\text{NL}}$ measurements against equilateral $p$-adic prediction
4. **Polarization parity:** TB/EB cross-spectrum search for parity-violating signal
5. **Multiple-testing correction:** Bonferroni correction for scanning over 6 primes

**Status:** Protocol pre-registered in the Kepler Program literature brief. Analysis pending access to Planck 2018 likelihood code and/or Simons Observatory early data [not yet falsifiable].

## References

1. Planck Collaboration (2020). Planck 2018 results. I. Overview and the cosmological legacy of Planck. *A&A*, 641, A1.
2. Hu, W. & Dodelson, S. (2002). Cosmic microwave background anisotropies. *Annual Review of Astronomy and Astrophysics*, 40, 171–216.
3. Maldacena, J. (2003). Non-Gaussian features of primordial fluctuations in single field inflationary models. *JHEP*, 05, 013.
4. Komatsu, E. et al. (2011). Seven-year Wilkinson Microwave Anisotropy Probe (WMAP) observations: Cosmological interpretation. *ApJS*, 192, 18.
5. Ade, P. A. R. et al. (2016). Planck 2015 results. XVI. Isotropy and statistics of the CMB. *A&A*, 594, A16.
6. Akrami, Y. et al. (2020). Planck 2018 results. VII. Isotropy and statistics of the CMB. *A&A*, 641, A7.

---

*Pillar 5 of the Zitterbewegung Cosmology Research Program. Next: Pillar 6 — Matter-Antimatter Asymmetry.*
