# Bayesian Cascading Dependency Model — Full Specification

> Load this reference when executing Stage 5 of the deep-research pipeline. Contains the complete mathematical specification, DAG construction rules, and portfolio optimization algorithm.

---

## Table of Contents
1. Prior Probability Estimation
2. Conditional Dependencies & DAG Construction
3. Impact Factor Multi-Dimensional Scoring
4. Expected Value Computation
5. Portfolio Optimization
6. Sensitivity Analysis
7. Implementation Notes

---

## 1. Prior Probability Estimation

### Source Decomposition
The prior P(shift_i) for each paradigm-shift candidate is computed as the product of independently assessed assumption probabilities:

```
P(shift_i) = ∏ P(assumption_k | evidence_k) × P(enabling_conditions)
```

### Assumption Confidence Calibration (Stage 3)
Convert qualitative confidence tags to quantitative priors:

| Tag | Probability Range | Default |
|:----|:-----------------|:--------|
| CRITICAL + HIGH confidence | 0.80–0.95 | 0.875 |
| CRITICAL + MEDIUM confidence | 0.50–0.80 | 0.65 |
| CRITICAL + LOW confidence | 0.10–0.50 | 0.30 |
| ENABLING + HIGH | 0.70–0.90 | 0.80 |
| ENABLING + MEDIUM | 0.40–0.70 | 0.55 |
| ENABLING + LOW | 0.05–0.40 | 0.225 |

### Red-Team Adjustment (Stage 4)
After adversarial questioning, apply multiplicative adjustments:

| Classification | Adjustment Factor |
|:---------------|:------------------|
| KILLED | P → 0 (remove from model) |
| WOUNDED | × (0.2–0.5) depending on wound severity |
| SURVIVED | × 1.0 (no adjustment) or × 1.1 if red-team revealed strengthening evidence |

### Base-Rate Anchor
Use the historical base rate of paradigm shifts (~0.5-2 per decade across all science, or ~1-4 per century per major field) as an anchor. If the computed prior exceeds the base rate by >5×, flag for review.

```
If P(shift_i) > 5 × base_rate_per_field: mark [PRIOR-WARNING: exceeds historical base rate]
```

---

## 2. Conditional Dependencies & DAG Construction

### Dependency Types

| Type | Symbol | Meaning | Probability Effect |
|:-----|:-------|:--------|:-------------------|
| **Enables** | S_i → S_j | S_i is a prerequisite for S_j | P(S_j | ¬S_i) ≈ 0 |
| **Blocks** | S_i ⊘ S_j | S_i makes S_j impossible | P(S_j | S_i) ≈ 0 |
| **Synergizes** | S_i ⇄ S_j | Shifts amplify each other | P(S_j | S_i) > P(S_j) |
| **Independent** | S_i ⊥ S_j | No causal relationship | P(S_j | S_i) = P(S_j) |

### DAG Construction Rules
1. Nodes = paradigm-shift candidates
2. Edges = dependency relationships (directed)
3. No cycles permitted (must be a DAG — if cycles exist, the shifts are not well-defined)
4. Each edge has a conditional probability table (CPT)

### CPT Specification
For enabling edge S_i → S_j:
```
P(S_j = true | S_i = true) = p_enable
P(S_j = true | S_i = false) = p_block (typically near 0)
```

For blocking edge S_i ⊘ S_j:
```
P(S_j = true | S_i = true) = p_block (typically near 0)
P(S_j = true | S_i = false) = p_base
```

For synergy edge S_i ⇄ S_j:
```
P(S_j = true | S_i = true) = p_synergy (> p_base)
```

### Joint Probability Computation
```
P(all shifts) = ∏ P(shift_i | parents(shift_i))
```
Where parents() includes all enabling, blocking, and synergy relationships.

---

## 3. Impact Factor Multi-Dimensional Scoring

### Impact Dimensions (0–10 scale each)

| Dimension | Description | Weight (default) |
|:----------|:------------|:-----------------|
| **Scientific (S)** | New questions made askable; explanatory power gain | 0.35 |
| **Technological (T)** | New capabilities enabled; engineering breakthroughs | 0.25 |
| **Societal (C)** | Quality-of-life impact; institutional change | 0.20 |
| **Economic (E)** | Market creation; productivity gains | 0.20 |

Weights are configurable. For fundamental research, increase S weight. For applied, increase T/E.

### Composite Impact Score
```
I(shift_i) = w_S × S_i + w_T × T_i + w_C × C_i + w_E × E_i
```

### Time-Horizon Weighting
Nearer impacts are weighted higher (time-value of knowledge):

```
w(t) = 1 / (1 + r)^t
```
Where r = time discount rate (default r = 0.05 for annual, 0.03 for generational)

Time-horizon weight multipliers:
| Horizon | Distance (years) | Weight (r=0.05) | Weight (r=0.03) |
|:--------|:-----------------|:----------------|:----------------|
| 10-year | 10 | 0.614 | 0.744 |
| 20-year | 20 | 0.377 | 0.554 |
| 50-year | 50 | 0.087 | 0.228 |
| 100-year | 100 | 0.008 | 0.052 |

---

## 4. Expected Value Computation

### Individual EV
```
EV(shift_i) = P(shift_i) × I(shift_i) × w(t_i)
```

### Cascade EV (with dependencies)
For a shift that enables or synergizes with downstream shifts:
```
EV_total(shift_i) = EV(shift_i) + Σ[P(dep_k | shift_i) × I(dep_k) × w(t_k)]
```

Where dep_k are all shifts that depend on shift_i, and the sum runs over all downstream shifts weighted by the conditional probability that they occur given shift_i.

### Net Present Knowledge Value (NPKV)
For comparing shifts across different time horizons on a common scale:
```
NPKV(shift_i) = EV_total(shift_i) × (1 + r)^(-t_i)
```

---

## 5. Portfolio Optimization

### Problem Formulation
Given N candidates, budget B, and resource costs c_i:

```
Maximize: Σ_i Σ_j EV(shift_i | shift_j) × x_i × x_j
Subject to:
  x_i ∈ {0, 1}  (binary inclusion)
  Σ_i c_i × x_i ≤ B  (budget constraint)
  If S_i ⊘ S_j then x_i + x_j ≤ 1  (blocking constraint)
  If S_i → S_j then x_j ≤ x_i  (enabling constraint)
```

### Solution Approach
For small N (≤15): brute-force enumeration of all 2^N portfolios.
For larger N: greedy heuristic:
1. Compute standalone EV for each candidate
2. Sort by EV / cost ratio
3. Add candidates in descending order, skipping blocked ones
4. Recompute cascade EVs after each addition
5. Stop when budget exhausted

### Pareto Frontier
Compute the set of non-dominated portfolios (no other portfolio has both higher EV and lower cost). Present the frontier to the user for manual selection.

---

## 6. Sensitivity Analysis

### One-Way Sensitivity
Vary each prior probability by ±20% and recompute top-3 portfolio:
```
For each assumption k in shift_i:
  P_k_low = max(0.01, P_k × 0.8)
  P_k_high = min(0.99, P_k × 1.2)
  Recompute EV
  Record ΔEV
```

### Tornado Chart (textual)
Rank assumptions by ΔEV magnitude:
```
Assumption           | P_base | P_low | P_high | ΔEV_range
---------------------|--------|-------|--------|-----------
shift_1 / assumption_3 | 0.65  | 0.52  | 0.78   | ±0.34
shift_2 / assumption_1 | 0.80  | 0.64  | 0.96   | ±0.28
...
```

### Weight Sensitivity
Vary dimension weights and recompute:
- Scientific-heavy: S=0.50, T=0.20, C=0.15, E=0.15
- Applied-heavy: S=0.20, T=0.35, C=0.20, E=0.25
- Societal-heavy: S=0.25, T=0.15, C=0.40, E=0.20

### Structural Sensitivity
Remove each enabling dependency edge and recompute to identify which assumptions the model is most sensitive to.

---

## 7. Implementation Notes

### LLM Execution Strategy
- Compute P(shift_i) from assumption products (simple arithmetic)
- Construct DAG and CPTs (qualitative → quantitative conversion)
- Compute cascade EVs (simple arithmetic chain)
- For small N (≤15): brute-force portfolio optimization
- For sensitivity: recompute with varied inputs

### Python Script
See `scripts/impact_matrix.py` for the executable implementation. Run with:
```
python impact_matrix.py --input candidates.json --output results.json
```

### Input JSON Format
```json
{
  "candidates": [
    {
      "id": "shift_1",
      "name": "Room-temperature superconductivity",
      "horizon": 20,
      "prior_probability": 0.35,
      "impact": {"scientific": 9, "technological": 10, "societal": 8, "economic": 9},
      "resource_cost": 3,
      "dependencies": {"enables": ["shift_3"], "blocked_by": [], "synergizes_with": ["shift_2"]}
    }
  ],
  "config": {
    "weights": {"scientific": 0.35, "technological": 0.25, "societal": 0.20, "economic": 0.20},
    "discount_rate": 0.05,
    "budget": 10
  }
}
```

### Output Format
```json
{
  "ranked_candidates": [...],
  "dag": {...},
  "portfolio": {"selected": [...], "total_ev": 42.7, "total_cost": 8},
  "sensitivity": {"tornado": [...], "weight_sensitivity": {...}},
  "pareto_frontier": [...]
}
```

---

> **Version:** v1.0
