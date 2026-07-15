# Shor's Algorithm: What It Actually Proves and What It Doesn't
## QNFO Research — Policy Brief | July 2026

---

## THE CLAIM

Shor's 1994 algorithm is widely cited as proof that large-scale quantum computers will break RSA encryption, driving a $50B+ global migration to post-quantum cryptography (PQC).

## THE REALITY

Shor proved **FACTORING ∈ BQP** — that a quantum computer *could* factor integers efficiently. The claim that quantum computers *will* break RSA requires an additional, **unproven** premise: **FACTORING ∉ BPP** — that no polynomial-time classical factoring algorithm exists. After 30+ years, this remains an open problem equivalent to separating major complexity classes.

## THE MATH

```
FACTORING ∈ BQP (PROVEN ✓) + FACTORING ∉ BPP (UNPROVEN ✗) = Quantum Advantage (UNCERTAIN)
```

Without FACTORING ∉ BPP, Shor's algorithm demonstrates that factoring is *in* BQP — but not that BQP is *larger than* BPP. A breakthrough classical factoring algorithm would collapse the quantum advantage claim without disproving anything Shor proved.

## THE PHYSICS

RSA-2048 factoring requires:

| Requirement | Value |
|:------------|:------|
| Logical qubits | 4,099 |
| Physical qubits (median) | 2.1M – 7.9M |
| Gate fidelity at scale | ≥99.99% |
| Optimistic hardware crossover | ~2040 |
| Current state-of-art (2026) | ~127–433 noisy qubits |

**Under the QNFO Era 1 thesis:** The Kapitza thermal ceiling makes gate-based QC at this scale thermodynamically impossible — the required physical qubit count generates more localized heat than cryogenic systems can extract.

## THE ARCHITECTURE

≥80% of known exponential quantum speedups reduce to the **abelian hidden subgroup problem** — the same algebraic trick (period-finding via quantum interference) applied to different problems. Quantum advantage is **narrow**, not general.

## THE NARRATIVES

| Source | What They Say | What's Missing |
|:-------|:-------------|:---------------|
| NIST PQC docs | "Quantum computers will break RSA" | No acknowledgment of FACTORING ∉ BPP uncertainty |
| Expert surveys (Mosca) | RSA-2048 "likely" broken by 2035–2045 | No distinction between BQP membership and practical feasibility |
| Media coverage | "Quantum supremacy achieved" | Conflation of sampling experiments with cryptographic relevance |

## THE P-ADIC CONNECTION

Factoring via period-finding is a **periodicity detection** problem — mapping naturally to p-adic valuation on Bruhat-Tits trees. Ostrowski's Theorem establishes that the only non-trivial absolute values on ℚ are real (Archimedean) and p-adic (ultrametric). Shor's algorithm exploits the abelian (Archimedean) hidden subgroup; the QNFO framework extends this to the ultrametric domain via adelic encoding. The implication: quantum advantage, if real, is narrower than claimed — limited to algebraic problems with abelian group structure.

## RECOMMENDATIONS

1. **Migration timelines should model uncertainty explicitly** — treat FACTORING ∉ BPP as a Bayesian prior, not a settled fact
2. **Hardware roadmaps should report error bars** on crossover estimates reflecting fidelity + thermal sensitivity
3. **The invariant is narrow but genuine:** Shor proves abelian algebraic periodicity is quantum-detectable — not that quantum computers are generically superior
4. **PQC migration is prudent hedging**, not mathematical necessity — cost-benefit should treat it as insurance against an uncertain threat

## KEY NUMBERS

| Metric | Value |
|:-------|:------|
| Shor's proven gate complexity | O(n³) |
| Physical qubits required (median) | 2.1M |
| Logical qubits for RSA-2048 | 4,099 |
| Crossover year (optimistic) | ~2040 |
| GNFS complexity constant c | 1.923 (stable since 1993) |
| Fraction of speeds from abelian HSP | ≥80% |
| Years FACTORING ∉ BPP has been open | 30+ |
| Kapitza thermal ceiling (Era 1) | ~10⁴ qubits at 50 mK |

**Bottom line:** Migrate to PQC — it's prudent insurance. But the urgency narrative rests on an unproven premise, not a proven theorem. Shor's algorithm is a brilliant discovery about quantum interference, not a proof that quantum computers will break the internet. Combined with the QEC thermodynamic ceiling, the case for gate-based QC as an existential cryptographic threat collapses — it requires both a mathematical breakthrough (FACTORING ∉ BPP) AND an engineering breakthrough (thermodynamically viable scaling) that current evidence suggests are unlikely to converge.

---

*Source: \_26195142717.md (07/14 policy brief) + \_26195142113.md (Shor↔p-adic note) | Cross-referenced with QNFO 100YR Forecast*
