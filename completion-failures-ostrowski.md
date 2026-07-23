# Completion Failures Under Ostrowski's Theorem

> **A Systematic Research Programme into the Adelic Incompleteness of Mathematical Physics**
>
> Status: ACTIVE | Started: 2026-07-22 | Last updated: 2026-07-23
> Handoff anchor: `handoff/adelic-completion-failures-research`

---

## 1. The Programme Thesis

### 1.1 Ostrowski's Theorem (1916)

The only non-trivial absolute values on ℚ, up to equivalence, are:

- The **Archimedean** absolute value |·|_∞ (the usual real absolute value)
- The **p-adic** absolute values |·|_p for each prime p = 2, 3, 5, 7, ...

Correspondingly, the only non-trivial completions of ℚ are ℝ and ℚ_p.

### 1.2 The Metacritique

> **Any mathematical object defined over ℚ has completions at EVERY Ostrowski place. Physics that uses only the ∞-place (Archimedean/real) is using ONE projection of a multivariate adelic structure. This is a systematic error, not an occasional oversight.**

The programme catalogs, classifies, and quantifies failures where analysis in physics assumes only the Archimedean completion, ignoring other equally valid completions under Ostrowski's theorem. It then constructs the adelic completion where possible and determines whether the physical prediction depends on the choice of completion.

### 1.3 Why This Matters

1. **Completeness of analysis**: If a formula works in ℝ but not in ℚ_p, the formula is not well-defined over ℚ — it depends on the choice of completion. This means the physics is hiding implicit assumptions.
2. **The adelic constraint**: The product formula ∏_v |q|_v = 1 (for q ∈ ℚ^×) connects all completions. Measurements at the ∞-place constrain the p-adic places and vice versa. Ignoring this loses information.
3. **New physics**: p-adic completions may yield physically different predictions. If an experiment can distinguish between completions, the theory is falsifiable in a novel way.
4. **Methodological hygiene**: Any analytic expression over ℚ should specify which completion it lives in, or be shown to be completion-independent.

---

## 2. Catalog of Completion Failures

### 2.1 Category A: Functions That Don't Survive p-adic Completion

These are functions defined on ℝ that have no global analog in ℚ_p, or exist only on restricted domains.

| Object | Archimedean | p-adic Status | Physics Failure |
|:---|:---|:---|:---|
| **e^x** (exp) | Defined globally on ℝ | Exists only on restricted domain (|x|_p < p^{-1/(p-1)}) | Time evolution U(t) = e^{-iHt/ħ} — p-adic exp is local, not global |
| **ln x** | Defined on ℝ^+ | p-adic log defined on 1 + pℤ_p | Entropy S = k ln W — p-adic log has different branch structure |
| **sin/cos** | Defined globally | Defined via power series; p-adic convergence on restricted domain | Harmonic oscillator, wavefunctions — angle is Archimedean concept |
| **Γ(z)** | Meromorphic on ℂ | Morita's p-adic Γ exists but is different | Path integrals, zeta regularization — Γ-function appears everywhere |
| **π** | Real constant ≈ 3.14159... | Does not exist in ℚ_p (not a rational number, no p-adic limit) | Fine structure α = e²/(4πħc), Stefan-Boltzmann σ = π²k⁴/(60ħ³c²), Coulomb V = e²/(4πr) |
| **e** | Real constant ≈ 2.71828... | Does not exist in ℚ_p | Exponential decay, Boltzmann factor |
| **γ** (Euler-Mascheroni) | Real constant ≈ 0.5772... | Unknown p-adic status | Dimensional regularization, renormalization |

### 2.2 Category B: Geometric Objects Without p-adic Meaning

| Object | Physics Use | Archimedean Only? | Reason |
|:---|:---|:---|:---|
| **S¹** (circle) | Phase, U(1) gauge group, angular momentum | YES | π appears in circumference; p-adic analog would be a totally different structure |
| **S^n** (n-sphere) | Solid angle, angular integration | YES | Vol(S^{n-1}) = 2π^{n/2}/Γ(n/2) — π appears |
| **SO(3)** | Rotations, angular momentum algebra | YES | p-adic orthogonal groups exist but are totally disconnected |
| **Angle/phase** | Interference, coherent states, Berry phase | YES | Angle is fundamentally an Archimedean/real concept |
| **Solid angle 4π** | Coulomb's law, coupling constants | YES | 4π steradians — no p-adic meaning |
| **Continuous paths** | Feynman path integral | YES | ℚ_p is totally disconnected — "paths" are different |

### 2.3 Category C: Analytic Operations That Fail p-adically

| Operation | Physics Use | p-adic Status | Failure Mode |
|:---|:---|:---|:---|
| **Derivative as limit** | Equations of motion, β-functions | p-adic derivative exists but topology differs | The limit definition uses Archimedean convergence |
| **Chain rule** | β-function derivation, coordinate transforms | Holds but the underlying objects (π, e) may not exist | Derivatives of quantities involving π fail |
| **Integration / measure** | Action, path integral, probabilities | Haar measure exists but is different | Gaussian integral ∫ e^{-x²} dx = √π — assumes ℝ measure |
| **Intermediate Value Theorem** | Existence proofs, fixed points | Fails in ℚ_p (totally disconnected) | Proofs that assume connectedness |
| **Fourier transform** | QFT, signal processing | p-adic Fourier transform exists but is different | Dual group of ℚ_p is ℚ_p, not ℝ |
| **Analytic continuation** | Complex analysis, S-matrix | Different theory (rigid analytic geometry) | Resummation, dispersion relations may differ |

### 2.4 Category D: Physical Constants as Single-Place Projections

| Constant | Symbol | Defined Using | p-adic Question |
|:---|:---|:---|:---|
| **Fine structure constant** | α ≈ 1/137 | e²/(4πħc) | What is α_p? Is α adelic? |
| **Planck's constant** | ħ | Measured in ℝ | Is ħ the ∞-place projection? What are ħ_p? |
| **Speed of light** | c | Measured in ℝ | c is a rationalized definition now — but historically? |
| **Boltzmann constant** | k | Measured in ℝ | Same question |
| **Gravitational constant** | G | Measured in ℝ | G may be emergent, not fundamental |

---

## 3. Worked Example: The Kappa β-Function

The Kappa framework's β(α) = 8πCα² derivation is audited step-by-step for completion assumptions. This serves as the canonical case study for the programme.

### 3.1 The Derivation Steps and Their Completion Status

| Step | Expression | Completion Assumption | p-adic Status |
|:---|:---|:---|:---|
| (1) | g₀ is the bare coupling | Defined over ℝ | g₀ is a real number; no p-adic extension specified |
| (2) | κ = g₀/g | Ratio, defined over ℝ | g is measured; g₀ is unobservable |
| (3) | g(μ) is the running coupling | μ is a real scale | Scale μ ∈ ℝ^+ |
| (4) | α = g²/(4π) | **4π is Archimedean** | ❌ FAILS — π doesn't exist in ℚ_p |
| (5) | κ(μ) = g₀/g(μ) | Composition | ok |
| (6) | α₀ = g₀²/(4π) | Same as (4) | ❌ FAILS |
| (7) | dg/d(ln μ) = β(g) | Continuous derivative | ⚠️ Assumes ℝ calculus |
| (8) | κ⁴ = 16π²α²/g₀⁴ | **π² appears** | ❌ FAILS — double Archimedean |
| (9) | β(α) = 8π·C·α² | **8π is the N_∞ normalization** | ❌ FAILS |

### 3.2 Key Finding

The Kappa result is **Archimedean-only** in three explicit ways:
1. π appears in the coupling definition (step 4)
2. π² appears in the group-theoretic coefficient (step 8)
3. 8π is the ∞-place normalization factor (step 9)

The result is NOT falsified — it is CORRECT for the ∞-place. But it is a **single-place projection** of what should be an adelic quantity. The programme asks: what is the full adelic β-function?

### 3.3 The SIIT Interpretation

The SIIT ontology interprets g₀ as an observer-imposed boundary condition, not a physical parameter. Under this view:
- g₀ is chosen at one Ostrowski place (∞)
- But g₀ is defined over ℚ (it's a rational coupling in the UV fixed-point theory)
- Therefore g₀ has completions at ALL places
- The cancellation g₀/g₀ = 1 in the reduction uses the ∞-place value only
- What happens if g₀,p ≠ 1 at finite primes?

The product formula ∏_v |g₀|_v = 1 then imposes:
> g_{0,∞} · ∏_p g_{0,p} = 1

This converts the "free parameter" g₀ into a derived quantity — the Archimedean bare coupling is the reciprocal of the product of all p-adic bare couplings.

---

## 4. Systematic Methodology

### 4.1 The Completion Audit Protocol

For any mathematical quantity Q appearing in a physics formula:

1. **Origin check**: Is Q defined over ℚ, ℝ, or ℂ?
2. **Ostrowski expansion**: If over ℚ, Q has completions Q_∞ and Q_p for all p
3. **Formula audit**: Which completion does the formula implicitly assume?
4. **p-adic reconstruction**: Can the formula be rewritten for ℚ_p?
5. **Physical comparison**: Does the physical prediction differ between completions?
6. **Verdict**: 
   - **Completion-independent**: Formula works in all completions → adelic
   - **Completion-dependent**: Formula works only in one completion → incomplete
   - **Completion-impossible**: Formula cannot be defined in other completions → Archimedean-only

### 4.2 The Adelic Lift

When a quantity fails at individual p-adic places, attempt the **adelic lift**:
- Embed Q in the adele ring A_ℚ
- The adelic version Q_A = (Q_∞, Q_2, Q_3, Q_5, ...)
- Physical predictions become vectors: (pred_∞, pred_2, pred_3, ...)
- Global constraints from the product formula

### 4.3 Falsification Design

For each completion-dependent formula, design an experiment that could distinguish between completions:
- p-adic predictions give specific rational constraints
- These may differ from Archimedean predictions at some precision
- If measured value matches Archimedean but not p-adic → ∞-place is physically preferred
- If measured value is adelic → all places contribute

---

## 5. Mathematical Foundations

### 5.1 The Adelic Product Formula

For any non-zero rational number q ∈ ℚ^×:

> |q|_∞ · ∏_p |q|_p = 1

This is the fundamental constraint linking all completions. Any quantity defined over ℚ must satisfy this.

### 5.2 p-adic Analysis — Key Differences

| Property | ℝ | ℚ_p |
|:---|:---|:---|
| Topology | Connected | Totally disconnected |
| Compactness | Not compact | ℤ_p is compact |
| Metric | Archimedean | Ultrametric (strong triangle inequality) |
| exp(x) radius | ∞ | p^{-1/(p-1)} |
| log(x) domain | (0, ∞) | 1 + pℤ_p |
| π | Exists (transcendental) | Does not exist |
| e | Exists (transcendental) | Does not exist as a real number |

### 5.3 p-adic Special Functions

When standard functions fail, use p-adic analogs:

- **p-adic exponential**: exp_p(x) = ∑ xⁿ/n!, converges for |x|_p < p^{-1/(p-1)}
- **p-adic logarithm**: log_p(1+x) = ∑ (-1)^{n+1} xⁿ/n, converges for |x|_p < 1
- **Morita's p-adic Gamma**: Γ_p(n) = (-1)^n ∏_{1≤k<n, p∤k} k
- **p-adic zeta**: ζ_p(s) via Kubota-Leopoldt
- **p-adic Fourier transform**: Different dual group structure

---

## 6. The Adelic Constraint Engine

### 6.1 Core Idea

Convert the product formula into an algebraic engine: for any rational quantity q appearing in physics,

> q_∞ = 1 / (∏_p q_p)

This means the Archimedean value is **determined** by the p-adic values. If the p-adic completions are constrained by theory (e.g., rational couplings at finite primes from discrete symmetries), the Archimedean value is a prediction, not an input.

### 6.2 Application to Coupling Constants

For a coupling g defined over ℚ:
- g_∞ = measured coupling (~0.302 for α_s at M_Z, giving g ≈ 1.95 for QED)
- g_2, g_3, g_5, ... = unknown, possibly constrained by p-adic gauge theory
- Constraint: g_∞ · g_2 · g_3 · g_5 · ... = 1

If all p-adic couplings are O(1), then g_∞ ≈ 1 — which is close to the weak coupling! This is suggestive but needs rigorous development.

### 6.3 Application to the Kappa Framework

In the Kappa framework:
- g₀ is the bare coupling, defined at the UV fixed point
- κ = g₀/g is the scale factor
- g₀_∞ · ∏_p g₀_p = 1 (product formula)
- The cancellation g₀/g₀ in the β-function calculation uses g₀_∞ only
- If g₀_p ≠ 1, the full adelic κ_A may not cancel identically
- **This means the parameter-free result may be a single-place artifact**

---

## 7. Case Studies (Planned)

### 7.1 Fine Structure Constant α = e²/(4πħc)

- π appears explicitly → Archimedean
- What is α_p? Define α_p = e²/(4π_p ħc) with p-adic π_p → π_p doesn't exist
- Alternative: define coupling directly as g² without normalizing by π
- α_∞ = 1/137.036... is this the ∞-place projection of an adelic quantity?

### 7.2 Stefan-Boltzmann Constant σ = π²k⁴/(60ħ³c²)

- π² appears → double Archimedean
- What is p-adic blackbody radiation?
- p-adic integration over phase space may give different Stefan-Boltzmann analogs

### 7.3 Path Integral Normalization

- ∫ Dφ e^{iS[φ]} normalized to 1
- The Gaussian integral ∫ e^{-ax²} dx = √(π/a) uses π and ℝ measure
- p-adic Gaussian integral: ∫_{ℚ_p} χ(ax²) dx where χ is additive character
- Different normalization → different S-matrix elements?

### 7.4 WKB Quantization ∮ p dx = 2πħ(n + γ)

- The 2π is from the phase of a closed orbit in phase space
- p-adic phase space is totally disconnected → no continuous orbits
- p-adic WKB would require fundamentally different formulation

---

## 8. Preliminary Results

### 8.1 The Kappa Cancellation

The SIIT interpretation already provides a clean result: the cancellation g₀/g₀ = 1 is a **scale-separation consequence** — g₀ is observer-imposed at ONE scale, κ carries all scale dependence, so β-functions cannot depend on g₀. This holds for the ∞-place and may hold adelically IF g₀ is genuinely a single scale-independent quantity.

### 8.2 The π-as-Solid-Angle Problem

Many appearances of π in physics are geometric (solid angle, period of circular motion). These are fundamentally Archimedean — they require S¹, which requires connectedness. The question is: do the physical quantities they normalize (couplings, cross sections) have p-adic analogs that DON'T use π?

### 8.3 The Product Formula as a Selection Rule

The adelic product formula may select which completions are physically relevant: only completions where ALL quantities in a formula can be consistently defined simultaneously may contribute to physical predictions.

---

## 9. Deliverables

1. **Completion Failure Catalog** — comprehensive database of π, e, exp, log, Γ, ζ, and other functions/constants in physics with their p-adic status
2. **p-adic Construction Library** — p-adic analogs of key physics formulas where they exist
3. **Adelic Constraint Engine** — automated tool that takes a physics formula and determines which completions are valid
4. **Falsification Design Matrix** — experimental proposals to distinguish between completions
5. **Methodology Paper** — "On the Adelic Incompleteness of Mathematical Physics"

---

## 10. Related Work

### 10.1 p-adic Mathematical Physics (Existing Literature)

- **Volovich (1987)**: p-adic string theory — first proposal of p-adic spacetime
- **Vladimirov, Volovich, Zelenov (1994)**: p-adic analysis and mathematical physics textbook
- **Khrennikov (2004)**: p-adic valued probability and quantum mechanics
- **Dragovich, Khrennikov, Kozyrev, Volovich (2009)**: p-adic mathematical physics review
- **Missarov (1989)**: p-adic φ⁴ theory and renormalization group

**Key difference from this programme**: Existing p-adic physics typically constructs p-adic models as alternatives. This programme critiques the STANDARD formulation for ignoring completions it SHOULD have included.

### 10.2 Adelic Physics

- **Manin (1989)**: Adelic quantum mechanics
- **Dragovich (2004)**: Adelic harmonic oscillator
- This programme extends the adelic approach from model-building to **critique** of existing practice

### 10.3 Number Theory Connections

- Ostrowski (1916): Original theorem
- Tate's thesis (1950): Adelic Fourier analysis and zeta functions
- Langlands program: Adelic representation theory
- The programme connects these to FALSIFIABLE physics predictions

---

## 11. Programme Status

### 11.1 Phase Summary

| Phase | Status | Description |
|:---|:---|:---|
| Phase 0: Scoping | ✅ COMPLETE | Programme defined, taxonomy established, 4 categories (A/B/C/D) |
| Phase 1: Catalog | ✅ COMPLETE | 50+ objects catalogued across Categories A-G; 21 non-cosmetic predictions classified in 4 tiers |
| Phase 2: p-adic Constructions | 🔄 67% COMPLETE | 12/22 workstream tasks executed; Tier 1 Priority (A1, A2, A3) fully executed; Tier 3 fully resolved; Tier 2 partially executed |
| Phase 3: Causal Structure Development | 🔄 SPECIFIED | Bruhat–Tits/p-adic AdS/CFT pipeline defined (C1-RT.2–RT.5); zero computations executed |
| Phase 4: Falsification | ⬜ PLANNED | Falsifiability matrix designed (D4); experimental protocols at conceptual stage only |
| Phase 5: Publication | ⬜ PLANNED | Synthesis paper structure outlined; no draft written |

### 11.2 Phase 2 — Detailed Status

**Workstream A — Tier 1: Numerically Non-Cosmetic (1/5 executed)**

| Task | Status | Deliverable |
|:---|:---|:---|
| A1. Stefan-Boltzmann p-adic analog | ✅ EXECUTED | `artifacts/p-adic-stefan-boltzmann.md` |
| A2. Casimir p-adic analog | ✅ EXECUTED | `artifacts/p-adic-casimir-energy.md` |
| A3. ζ(2n) Basel sums | ✅ EXECUTED | `artifacts/zeta-even-values-basel-p-adic.md` |
| A4. Wien displacement p-adic | ⬜ PENDING | — |
| A5. Loop integral volumes π^{d/2} | ⬜ PENDING | — |

**Workstream B — Tier 2: Structurally Non-Cosmetic (2/6 executed)**

| Task | Status | Deliverable |
|:---|:---|:---|
| B1. p-adic Feynman propagator | ⬜ PENDING | `artifacts/p-adic-feynman-propagator.md` |
| B2. β-function (Missarov comparison) | ✅ EXECUTED | `artifacts/beta-function-missarov-comparison.md` |
| B3. Critical exponents (p-adic φ⁴ vs 3D Ising) | ✅ EXECUTED | `artifacts/critical-exponents-p-adic-phi4.md` |
| B4. Anomalous dimensions γ_φ | ⬜ PENDING | — |
| B5. S-matrix structural failure | ✅ EXECUTED | `artifacts/s-matrix-structural-failure.md` |
| B6. Uncertainty principle C_p | ⬜ PENDING | — |

**Workstream C — Tier 3: Existentially Non-Cosmetic (4/4 executed)**

| Task | Status | Deliverable |
|:---|:---|:---|
| C1. Causality analysis | ✅ EXECUTED | `artifacts/causality-in-qp.md` |
| C1-RT. Causality Red-Team (4 frameworks) | ✅ EXECUTED | `artifacts/causality-redteam-full-analysis.md` |
| C2. Time evolution failure | ✅ EXECUTED | `artifacts/time-evolution-p-adic-failure.md` |
| C3. Noether & continuous symmetries | ✅ EXECUTED | `artifacts/noether-continuous-symmetries-p-adic.md` |
| C4. WKB / geometric quantization | ⬜ PENDING | — |

**Workstream D — α Engine & Product Formula (2/4 executed)**

| Task | Status | Deliverable |
|:---|:---|:---|
| D1. α adelic constraint engine | ⬜ PENDING | `artifacts/alpha-137-cosmetic-vs-adelic.md` (started, partial) |
| D2. Product formula constraint engine | ✅ EXECUTED | `artifacts/product-formula-constraint-engine.md` |
| D3. Cosmological constant cancellation | ⬜ PENDING | — |
| D4. Falsifiability matrix | ✅ EXECUTED | `artifacts/falsifiability-matrix.md` |

**Workstream E — External Literature (1/3 executed)**

| Task | Status | Deliverable |
|:---|:---|:---|
| E1. Literature scan: p-adic QFT/QED | ✅ EXECUTED | `artifacts/p-adic-physics-literature-scan.md` |
| E2. Gap analysis | ⬜ PENDING | — |
| E3. Citation audit | ⬜ PENDING | — |

**Cross-Cutting Deliverables (Phase 2)**

| Task | Status | Deliverable |
|:---|:---|:---|
| Adelic infinity: asymptote / Hilbert's Hotel / taxonomy | ✅ EXECUTED | `artifacts/adelic-infinity-analysis.md` (commits d9611a9, 9d7c8b9) |
| π adelic decomposition deep-dive | ✅ EXECUTED | `pi-adelic-decomposition.md` |
| 21-prediction catalog | ✅ EXECUTED | `non-cosmetic-archimedean-predictions.md` |
| Phase 2 WBS | ✅ EXECUTED | `artifacts/completion-failures-phase2-wbs.md` |

**Phase 2 totals: 12/22 workstream tasks executed + 4/4 cross-cutting = 16/26 (62%)**

### 11.3 Phase 3 — Causal Structure Development (0/4 executed)

| Task | Status | Description |
|:---|:---|:---|
| C1-RT.2 | ⬜ PENDING | p-adic AdS/CFT Mellin amplitudes A_p(s,t) for p=2,3,5 |
| C1-RT.3 | ⬜ PENDING | Tree-to-building generalization (extend from PGL(2) to PGL(n)) |
| C1-RT.4 | ⬜ PENDING | Adelic S-matrix product ⊗'_p S_p |
| C1-RT.5 | ⬜ PENDING | Page-Wootters adelic clock (unique-clock proof via Ostrowski) |

### 11.4 Phase 4 — Falsification Design (0/N executed)

| Task | Status | Description |
|:---|:---|:---|
| P4.1 | ⬜ PENDING | Refine experimental protocols (spin noise, EELS/RIXS, Gromov δ) from CONCEPTUAL → DESIGNED |
| P4.2 | ⬜ PENDING | Simulate expected ultrametric vs. Archimedean signatures |
| P4.3 | ⬜ PENDING | Identify collaboration-ready labs |
| P4.4 | ⬜ PENDING | Derive p-adic corrections to cross sections (from C1-RT.2) |

### 11.5 Phase 5 — Publication (0/N executed)

| Task | Status | Description |
|:---|:---|:---|
| P5.1 | ⬜ PENDING | Synthesis paper: "On the Adelic Incompleteness of Mathematical Physics" |
| P5.2 | ⬜ PENDING | Phase 2 synthesis document from existing 21-prediction catalog |
| P5.3 | ⬜ PENDING | Pandoc+XeLaTeX PDF build |
| P5.4 | ⬜ PENDING | Zenodo DOI deposit |
| P5.5 | ⬜ PENDING | D1 living-paper insert + R2 archive |
| P5.6 | ⬜ PENDING | Dissemination (Buffer, SEO, DNSLink) |

### 11.6 Priority Stack — Remaining Tasks (Execution Order)

**Priority 1 — Tier 1 Numerics (strongest falsifiable predictions)**
→ A1: Stefan-Boltzmann p-adic analog
→ A2: Casimir p-adic analog

**Priority 2 — Foundational Infrastructure**
→ B1: p-adic Feynman propagator (required for ALL Tier 2 computation)

**Priority 3 — Constraint Engine Completion**
→ D1: α adelic constraint engine

**Priority 4 — Remaining Tier 2**
→ B4: Anomalous dimensions
→ B6: Uncertainty principle
→ A4: Wien displacement
→ A5: Loop integral volumes

**Priority 5 — Tier 3 Remaining**
→ C4: WKB quantization

**Priority 6 — Phase 3 (Causal Structure)**
→ C1-RT.2–RT.5: Computational p-adic AdS/CFT pipeline
→ Most mathematically intensive; may require Python/numerical work

**Priority 7 — External Validation**
→ E2: Gap analysis
→ E3: Citation audit

**Priority 8 — Publication**
→ P5.1–5.6: Synthesis paper through full pipeline

---

## Supporting Documents

- `pi-adelic-decomposition.md` — Deep dive on π's adelic meaning and the solid-angle problem
- `adelic-constraint-engine.md` — Expanded catalog (Categories E-G), p-adic Gaussian integral construction, adelic constraint engine for α, refined π hypothesis (cosmetic vs. non-cosmetic), product formula as physical selection rule
- `kappa-siit-extended-reduction-test.md` — SU(2)_L × U(1)_Y extension of the Kappa reduction (the physics case study)

### Related Cross-Domain Work

- `releases/cross-domain/X1.1-alpha-cross-domain-invariant.md` — α as a Cross-Domain Invariant: Derivation of the Adelic-Compton-Harmonic normalization
- `releases/cross-domain/X1.2-adelic-alpha-product.md` — The Adelic Fine-Structure Product: Computing α_adelic from Prime-Indexed p-Adic Couplings

---

*"The Archimedean completion of ℚ was only ONE of infinitely many — and we have been doing physics on only one branch of the universal cover."*
