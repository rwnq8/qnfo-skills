# Amice Transform of Interface Quality
## Formalizing RQ-039: Do Dominant Ultrametric Scales Emerge from the Amice Transform?

**Version:** v1.0 | **Date:** 2026-07-05
**Connects:** RQ-039, Berkovich Optimal Interface, Number Theory Track
**Status:** Formal definition + computational algorithm + testable predictions

---

## Abstract

The Amice transform maps a function f on the p-adic integers to its Mahler expansion coefficients. When applied to "interface quality" — user satisfaction as a function of ultrametric depth — the Amice spectrum reveals which tree levels are most informative. We define interface quality as a p-adic function, compute its Amice transform, and predict that spectral peaks correspond to taxonomy levels (domain → program → project). The spectral sparsity (number of non-zero Mahler coefficients) measures the effective depth of the ultrametric tree for a given user.

---

## 1. The Amice Transform (Mathematical Preliminaries)

### 1.1 Definition

For a function f: Z_p → C_p (p-adic integers to p-adic complex numbers), the Amice transform A_f is the sequence of Mahler coefficients {a_n}:

$$f(x) = \sum_{n=0}^{\infty} a_n \binom{x}{n}$$

where:
- \binom{x}{n} = x(x-1)...(x-n+1)/n! is the Mahler binomial basis
- a_n = \sum_{k=0}^n (-1)^{n-k} \binom{n}{k} f(k) are the Mahler coefficients

**Key property:** A function is locally constant (i.e., constant on balls of radius p^{-m}) if and only if a_n = 0 for all n ≥ p^m. This directly links the Amice spectrum to the depth of the ultrametric tree.

### 1.2 Locally Constant Functions and Tree Depth

If f is constant on balls of radius p^{-d} (i.e., doesn't distinguish beyond depth d in the tree), then:

$$a_n = 0 \quad \text{for all } n \geq p^d$$

The number of non-zero Mahler coefficients is exactly p^d — the number of leaves in a depth-d tree with constant branching factor p.

---

## 2. Interface Quality as a p-adic Function

### 2.1 Defining Interface Quality

Interface quality Q: Z_p → [0, 1] measures user satisfaction when presented with the ultrametric tree at resolution level |x|_p:

$$Q(x) = \text{satisfaction at p-adic resolution } |x|_p$$

where:
- |x|_p = p^{-v_p(x)} is the p-adic absolute value
- v_p(x) = -\log_p |x|_p is the p-adic valuation (tree depth)
- Higher |x|_p means finer resolution (deeper in the tree)

### 2.2 Empirical Measurement of Q

For each user u and each tree depth d:

1. Present the user with the QNFO Knowledge Graph truncated to depth d
2. Measure task completion rate (finding a specific paper)
3. Measure self-reported satisfaction (1-5 Likert)
4. Normalize Q_u(d) to [0, 1]

**Expected shape:** Q_u(d) should rise with d (more information), peak at the optimal depth d* (Berkovich optimal point), then decline (cognitive overload).

$$Q_u(d) \approx \frac{d}{d^*} \exp(1 - d/d^*)$$

### 2.3 Embedding into Z_p

Map tree depth d to p-adic integer x:

$$x_d = 1 + p + p^2 + ... + p^{d-1} = \frac{p^d - 1}{p - 1}$$

This has valuation v_p(x_d) = 0 (x_d is a p-adic unit at all depths — the depth information is encoded in the p-adic expansion, not the valuation).

Then Q_u: Z_p → [0, 1] is defined by:
$$Q_u(x) = Q_u(\text{depth of x in the tree})$$

---

## 3. Computational Algorithm

### 3.1 Computing Mahler Coefficients

For a finite tree of depth D (leaves at depth D), f is determined by its values at x = 0, 1, 2, ..., p^D - 1:

```python
def mahler_coefficients(f_values, p, max_n):
    """Compute Mahler coefficients {a_n} for n = 0 to max_n."""
    a = []
    for n in range(max_n + 1):
        # a_n = sum_{k=0}^n (-1)^{n-k} binom(n,k) f(k)
        a_n = sum(
            (-1)**(n - k) * binom(n, k) * f_values[k]
            for k in range(n + 1)
        )
        a.append(a_n)
    return a
```

### 3.2 Spectral Analysis

The Amice spectrum is the sequence {|a_n|_p} of p-adic absolute values of Mahler coefficients.

**Key insight:** Large |a_n|_p means the n-th Mahler basis function contributes significantly — this corresponds to tree level floor(log_p n).

**Spectral peaks at:**
- n ≈ p^0 = 1 → domain level (coarsest distinction)
- n ≈ p^1 = p → program level
- n ≈ p^2 → project level
- n ≈ p^3 → paper level

### 3.3 Sparsity Metric

Define the **Amice sparsity** S(f) as the effective number of non-zero coefficients:

$$S(f) = \left(\sum_n |a_n|\right)^2 / \sum_n |a_n|^2$$

This is the inverse participation ratio — small S(f) means few dominant scales (simple interface), large S(f) means many scales contribute (complex interface requiring many tree levels).

---

## 4. Testable Predictions

### 4.1 Taxonomy-Level Peaks

**Prediction P1:** For the QNFO Knowledge Graph with p = 2 (binary tree), the Amice transform of interface quality Q_u should show spectral peaks at:

| n | Tree Level | Expected Peak? |
|:--|:-----------|:--------------|
| 1 | Root (all papers) | YES — coarsest distinction |
| 2 | Domain level | YES — QWAV Physics vs Research Programs vs Infrastructure |
| 4 | Program level | YES — 10+ programs |
| 8 | Project level | PARTIAL — some projects, not all |
| 16+ | Paper level | WEAK — individual papers blur together |

**Disconfirmation:** If NO spectral peaks appear (all a_n have similar magnitude), then the ultrametric tree has no intrinsic level structure — the interface is equally informative at all depths.

### 4.2 Personalized Amice Signatures

**Prediction P2:** Different users have different Amice spectra reflecting their expertise:

| User Type | Expected Spectrum | Peak at |
|:----------|:-----------------|:-------|
| Novice | Sparse (2-3 peaks) | Low n (domain/program level) |
| Domain expert | Moderate (3-5 peaks) | Medium n (program/project level) |
| Researcher | Dense (5-8 peaks) | High n (project/paper level) |

**Disconfirmation:** If all users have identical Amice spectra, then personalization is irrelevant — a single optimal interface works for everyone.

### 4.3 Amice Sparsity as Interface Complexity

**Prediction P3:** S(Q_u) should correlate negatively with task completion time and positively with self-reported satisfaction:

$$S(Q_u) \uparrow \implies \text{time} \uparrow, \text{satisfaction} \downarrow$$

More spectral scales → more complex interface → harder to navigate.

---

## 5. Connection to Other Frameworks

### 5.1 Berkovich Optimal Interface

The Berkovich point ξ* that maximizes interface quality corresponds to the p-adic valuation where the Amice spectral density peaks:

$$v_p(\xi^*) = \arg\max_n |a_n|_p$$

### 5.2 Falsifiability Scorecard

RQ-039 is ranked at falsifiability score 0.35 (CONCEPTUAL tier). The Amice transform provides the mathematical machinery to upgrade it to DESIGNED tier — the predictions in Section 4 are specific and falsifiable.

### 5.3 Number Theory / Ultrametric Engine

The Amice transform is Principle #20 of the ultrametric engine (20-principle stack). This formalization provides the computational implementation.

---

## 6. References

1. Amice, Y. *Les nombres p-adiques* (1975)
2. Schikhof, W.H. *Ultrametric Calculus* (1984)
3. RQ-039: Amice Transform of Interface Quality
4. Berkovich Optimal Interface (2026-07-05)
5. Falsifiability Scorecard (2026-07-05)
6. Ultrametric Engine Skill (20 principles)

---

*Amice Transform Formalization v1.0. Defines interface quality as p-adic function, computes Mahler coefficients, predicts taxonomy-level spectral peaks. Ready for empirical validation when D3 navigation data is collected.*
