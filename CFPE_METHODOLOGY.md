# The Cascading Bayesian Foresight Engine (CFPE)
## A Methodology for Probability-Weighted Multi-Era Paradigm Forecasting

**Date:** 2026-07-15 | **Authors:** QNFO Research / QWAV | **Version:** 1.0

---

## Abstract

We present the Cascading Bayesian Foresight Engine (CFPE), a formal methodology for evaluating long-term, multi-phase strategic initiatives across scientific, technological, economic, and policy domains. Existing forecasting methods treat each phase as an independent milestone; CFPE instead models phases as a network of cascading conditional probabilities where P(Phase_n) = Σ P(Phase_n | Phase_{n-1}) · P(Phase_{n-1}). The methodology integrates five components: (1) domain scoping with historical reference class anchoring, (2) paradigm-shift candidate generation with mandatory continuity baselines, (3) multi-adversarial red-team questioning, (4) Bayesian cascading dependency modeling with DAG construction and portfolio optimization, and (5) a dated prediction register with back-testing cadence for calibration tracking. The methodology is LLM-executable via the `impact_matrix.py` reference implementation.

---

## 1. The Problem

Strategic roadmaps systematically overestimate success because they treat each phase as independent. CFPE replaces the independence assumption with explicit conditional probability matrices:

```
P(Era_n) = Σ P(Era_n | Era_{n-1} = state) · P(Era_{n-1} = state)
```

For each era, three scenario states are tracked: Optimistic, Baseline, Pessimistic.

---

## 2. Five Components

### 2.1 Reference Class Anchoring
Calibrate all priors against historical hit-rates of similar forecasts. Prevents base-rate neglect.

**Rule:** If every candidate's prior exceeds the reference class base rate by 3×, flag [PRIOR-WARNING].

### 2.2 Continuity Baseline
Always include a Candidate #0: "Incremental Progress — No Paradigm Shift." Every candidate must compete against normal science.

### 2.3 Multi-Adversarial Red-Team
Five role-played adversaries challenge each candidate:
1. The rigorous empiricist ("Where is the evidence?")
2. The Kuhnian conservative ("Anomalies are always resolvable within the current paradigm.")
3. The Bayesian skeptic ("Given the base rate, the prior is tiny.")
4. The institutional realist ("Sociology of science prevents adoption for decades.")
5. The alternative explainer ("Here is a simpler explanation requiring no paradigm shift.")

Classify: KILLED | WOUNDED (probability reduced >50%) | SURVIVED

### 2.4 Bayesian Cascading Model (impact_matrix.py)

| Feature | Description |
|:--------|:------------|
| DAG Construction | Enables, blocks, synergizes edges between candidates |
| Portfolio Optimization | Maximize Σ EV × x_i subject to budget |
| Choke Node ID | Highest P(Pessimistic) × cascade EV |
| Leverage Node ID | P(Opt|Prior_Opt) > 0.80 edges |
| Anti-Fragility Floor | Minimum EV if choke node pessimistic materializes |
| Prior Stability | Halve all priors, check if portfolio changes |

### 2.5 Calibration Register
Every prediction with P > 0.10 must have:
- Date-stamped probability estimate
- Specific, observable, time-bound falsification test
- ±X% confidence interval
- 6-month/1-year/2-year/5-year check cadence

---

## 3. Resource Allocation Rules (CFPE Doctrine)

| Rule | When Applied | Action |
|:-----|:-------------|:-------|
| **Leverage Node Rule** | P(Era_n_Opt | Era_{n-1}_Opt) > 0.80 | Allocate 40-50% of budget to Era_{n-1} |
| **Choke Node Rule** | Highest P(Pessimistic) in cascade | Add adoption incentives, regulatory mandates, demonstration missions |
| **Red-Team Hardening Loop** | Final era P(Opt) < 0.30 | Return to Stage 4, introduce countermeasure |

---

## 4. Reference Implementation

```bash
# Candidates mode (flat DAG with dependencies)
python impact_matrix.py --input candidates.json --output results.json

# Eras mode (multi-era cascade with conditional matrices)
python impact_matrix.py --input eras.json --output results.json --mode eras

# Executive summary option
python impact_matrix.py -i candidates.json -o results.json --discount 0.03 --budget 15
```

**Input format:** JSON with candidates array (candidates mode) or eras array (eras mode). Full specification in `impact_matrix.py` docstring.

---

## 5. Validation Results (QNFO 100-Year Forecast)

| Metric | Value |
|:-------|:------|
| Total lifecycle EV | 20.60 / 39.30 (52.43%) |
| Primary choke node | E1 (FCI Passive QC), P(Pess)=0.15 |
| Primary leverage node | FCI→Ultrametric Qudit, P>0.80 |
| Anti-fragility floor | 91.17% of optimal (ROBUST) |
| Prior stability | PRIOR-ROBUST |

---

## 6. When to Use CFPE

| Situation | Use CFPE | Use Alternative |
|:----------|:---------|:----------------|
| Multi-phase, multi-decade dependency chain | ✅ | |
| Need auditable, falsifiable methodology | ✅ | |
| Decision-makers need resource allocation rules | ✅ | |
| Rapid directional decision (<1 day) | | Expert elicitation (5 experts, ~2 hours) |
| Single-phase near-term decision | | Standard cost-benefit or decision tree |

---

## 7. Limitations

- Prior probabilities are inherently subjective (mitigated by reference class anchoring + halve-all-priors check)
- Cannot predict genuinely novel phenomena (unknown unknowns)
- Institutional inertia may extend timelines beyond model estimates
- Requires domain expertise to calibrate conditional matrices

---

*Generated by deep-research skill v1.1 + impact_matrix.py | 2026-07-15*
