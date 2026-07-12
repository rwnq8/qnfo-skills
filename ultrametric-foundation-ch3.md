# Chapter 3: Berkovich Spaces and Analytic Geometry

**Ultrametric Foundation Thesis** | **Author:** Rowan Brad Quni-Gudzinas  
**Date:** 2026-07-12 | **Status:** Draft v0.1

---

## 3.1 Introduction: Beyond Rigid Geometry

Chapter 2 established Bruhat-Tits buildings as the geometric realization of reductive groups over non-Archimedean fields. This chapter introduces **Berkovich analytic spaces** — a formalism that unifies rigid analytic geometry (Tate) with the topological intuition of complex analytic geometry, providing the natural analytic category for ultrametric physics [established].

The Berkovich approach solves a fundamental problem: Tate's rigid analytic spaces have a Grothendieck topology but lack honest topological points in the classical sense. Berkovich spaces restore point-set topology by "adding" seminorms as new points, creating a compact Hausdorff space from any affinoid algebra — a construction that mirrors the Gelfand transform for commutative $C^*$-algebras [established].

## 3.2 The Berkovich Spectrum

### 3.2.1 Seminorms as Points

Let $K$ be a complete non-Archimedean field with valuation $v: K \to \mathbb{R} \cup \{\infty\}$. An **affinoid algebra** $\mathcal{A}$ is a quotient of the Tate algebra $K\langle T_1, \ldots, T_n \rangle$ (the algebra of power series converging on the closed unit polydisc).

**Definition 3.1 (Berkovich Spectrum):** The Berkovich spectrum $\mathcal{M}(\mathcal{A})$ is the set of all bounded multiplicative seminorms $|\cdot|_x: \mathcal{A} \to \mathbb{R}_{\geq 0}$ extending the valuation on $K$:

$$\mathcal{M}(\mathcal{A}) = \{x: \mathcal{A} \to \mathbb{R}_{\geq 0} \mid x \text{ is a bounded multiplicative seminorm}, x|_K = |\cdot|_K\}$$

The topology on $\mathcal{M}(\mathcal{A})$ is the weakest topology making the evaluation maps $x \mapsto |f|_x$ continuous for all $f \in \mathcal{A}$ [established].

### 3.2.2 Types of Points

Points in $\mathcal{M}(\mathcal{A})$ come in four types, classified by the residue field $\widetilde{\mathcal{H}(x)}$ and the value group $|\mathcal{H}(x)^\times|$ [established]:

| Type | Description | Example |
|:-----|:------------|:--------|
| **Type 1** | Classical rigid points; residue field is finite over $K$ | $x = a \in K^n$ with $|f|_x = |f(a)|$ |
| **Type 2** | Generic points of affinoid subdomains; residue field has transcendence degree 1 | Gauss point on the closed disc |
| **Type 3** | Points with non-discrete value group | "Irrational radius" points on the closed disc |
| **Type 4** | Limit points of descending chains of affinoid subdomains | Only appear when $K$ is not spherically complete |

### 3.2.3 The Berkovich Closed Disc

For $\mathcal{A} = K\langle T \rangle$ (the one-dimensional Tate algebra), the Berkovich spectrum $\mathcal{M}(K\langle T \rangle)$ is the **Berkovich closed unit disc** $\mathbb{D}^1_K$. Its structure is a tree:

- **Root (Type 2):** The Gauss point $\eta_{0,1}$ defined by $|\sum a_n T^n|_{\eta} = \max_n |a_n|$
- **Branches (Type 2):** For each $a \in K$ with $|a| \leq 1$ and $r \in |K^\times|$, the point $\eta_{a,r}$ defined by $|\sum b_n (T-a)^n|_{\eta_{a,r}} = \max_n |b_n| r^n$
- **Leaves (Type 1):** Classical points $T = a$ for $a \in K$ with $|a| \leq 1$
- **Edges (Type 3):** Points connecting Type 2 points at different radii

The tree structure of $\mathbb{D}^1_K$ is precisely the $p$-ary tree encountered in the Bruhat-Tits building for $\mathrm{SL}(2, K)$ — a concrete demonstration of the building-Berkovich correspondence [established].

## 3.3 Comparison with Other Geometries

### 3.3.1 Berkovich vs. Rigid Analytic

Tate's rigid analytic spaces have a Grothendieck topology whose admissible opens are affinoid subdomains. The functor:

$$\{\text{rigid spaces over } K\} \to \{\text{Berkovich spaces over } K\}$$

sends a rigid space $X$ to its Berkovich analytification $X^{\text{Berk}}$, which adds Type 2, 3, and 4 points to $X$. This functor is **fully faithful** on the category of rigid spaces with good analytic properties [established].

### 3.3.2 Berkovich vs. Adic Spaces (Huber)

Huber's adic spaces generalize Berkovich spaces by allowing valuations that are not necessarily rank-1. The comparison:

$$\{\text{Berkovich } K\text{-analytic spaces}\} \hookrightarrow \{\text{adic spaces over } K\}$$

is a full embedding. Adic spaces are more general and are the natural setting for perfectoid geometry (Scholze), but Berkovich spaces are more geometric and sufficient for the ultrametric physics applications of this thesis [established].

### 3.3.3 Berkovich vs. Complex Analytic

The Berkovich spectrum is the non-Archimedean analogue of the Gelfand spectrum for commutative $C^*$-algebras. For a complex commutative Banach algebra $B$, the Gelfand spectrum is:

$$\Sigma(B) = \{\text{characters } \chi: B \to \mathbb{C}\}$$

For a Berkovich affinoid algebra $\mathcal{A}$, the spectrum is:

$$\mathcal{M}(\mathcal{A}) = \{\text{bounded multiplicative seminorms } |\cdot|: \mathcal{A} \to \mathbb{R}_{\geq 0}\}$$

Both constructions produce compact Hausdorff spaces and form the basis for a functional-analytic approach to geometry. The distinction — characters vs. seminorms — reflects the fundamental difference between Archimedean and non-Archimedean analysis [established].

## 3.4 Sheaf Theory on Berkovich Spaces

### 3.4.1 The Structure Sheaf

A Berkovich space $(X, \mathcal{O}_X)$ is a locally ringed space where $\mathcal{O}_X$ is the sheaf of analytic functions. For an affinoid algebra $\mathcal{A}$, the space $\mathcal{M}(\mathcal{A})$ is equipped with the structure sheaf $\mathcal{O}_{\mathcal{M}(\mathcal{A})}$ where:

$$\mathcal{O}_{\mathcal{M}(\mathcal{A})}(U) = \{\text{analytic functions on } U\}$$

for affinoid subdomains $U \subset \mathcal{M}(\mathcal{A})$ [established].

### 3.4.2 Coherent Sheaves and Kiehl's Theorem

The analogue of Cartan's Theorems A and B for Berkovich spaces is Kiehl's Theorem: for any coherent sheaf $\mathcal{F}$ on an affinoid space $\mathcal{M}(\mathcal{A})$:

1. $\mathcal{F}$ is generated by its global sections (Theorem A)
2. $H^q(\mathcal{M}(\mathcal{A}), \mathcal{F}) = 0$ for all $q \geq 1$ (Theorem B)

These vanishing theorems are essential for the deformation theory and cohomological computations that underlie the ultrametric topos construction (Chapter 6) [established].

## 3.5 The Berkovich-Gelfand Transform

### 3.5.1 Definition

For an affinoid algebra $\mathcal{A}$, the **Berkovich-Gelfand transform** maps elements of $\mathcal{A}$ to continuous functions on $\mathcal{M}(\mathcal{A})$:

$$\Gamma: \mathcal{A} \to C^0(\mathcal{M}(\mathcal{A}), \mathbb{R}), \quad f \mapsto (x \mapsto |f|_x)$$

This is a bounded homomorphism from the algebra to the Banach algebra of continuous functions on the spectrum. The image is the algebra of **Berkovich-analytic functions** on the spectrum [established].

### 3.5.2 The Maximum Modulus Principle

**Theorem 3.1 (Berkovich Maximum Modulus):** For any $f \in \mathcal{A}$, the function $x \mapsto |f|_x$ attains its maximum on $\mathcal{M}(\mathcal{A})$ at a Type 1 (classical) point. Specifically:

$$\sup_{x \in \mathcal{M}(\mathcal{A})} |f|_x = \max_{x \in X(K)} |f(x)|$$

where $X(K)$ is the set of classical rigid points [established].

This theorem is the non-Archimedean analogue of the classical maximum modulus principle and is fundamental for the spectral theory developed in Chapter 4 (Tate-Amice analysis).

## 3.6 Berkovich Spaces and Ultrametric Trees

### 3.6.1 The Tree of Seminorms

For a one-dimensional affinoid algebra $\mathcal{A}$ over $\mathbb{Q}_p$, the Berkovich spectrum $\mathcal{M}(\mathcal{A})$ is a **tree** when considered as a metric graph. The vertices are Type 2 points and the edges are composed of Type 3 points. This tree structure is isomorphic to the Bruhat-Tits tree for $\mathrm{SL}(2, \mathbb{Q}_p)$ studied in Chapter 2 [established].

### 3.6.2 Adelic Factorization

For multiple primes $\{p_1, \ldots, p_n\}$, the product of Berkovich spectra factorizes:

$$\mathcal{M}(\mathcal{A} \otimes \prod_i \mathbb{Q}_{p_i}) \cong \prod_i \mathcal{M}(\mathcal{A} \otimes \mathbb{Q}_{p_i})$$

This factorization is the geometric expression of the adelic structure exploited by the Kepler Program's QEC architecture [established].

### 3.6.3 The Ultrametric Interpretation

Every Berkovich space carries a natural ultrametric on the set of Type 1 (classical) points induced by the tree structure on $\mathcal{M}(\mathcal{A})$. For two classical points $x, y \in X(K)$, define:

$$d(x, y) = \inf\{r > 0 : \eta_{x,r} = \eta_{y,r}\}$$

where $\eta_{x,r}$ is the point of type 2 at radius $r$ centered at $x$. This distance is an ultrametric — the "tree distance" in the Berkovich spectrum — and generalizes the $p$-adic metric on $\mathbb{Q}_p$ to arbitrary affinoids [my conjecture].

## 3.7 Open Questions

| RQ | Question | Status |
|:---|:---------|:------|
| RQ-041 | Do Berkovich analytic spaces form a sheaf topos over $\mathbf{Ult}$? | Open |
| RQ-042 | Does Tate's rigid analytic geometry embed faithfully in the Berkovich topos? | Open |
| RQ-041b | Is there a geometric morphism from the Berkovich site to the ultrametric topos (Ch6)? | Open |

## References

1. Berkovich, V. G. (1990). *Spectral Theory and Analytic Geometry over Non-Archimedean Fields*. AMS Mathematical Surveys and Monographs, 33.
2. Berkovich, V. G. (1993). Étale cohomology for non-Archimedean analytic spaces. *Publications Mathématiques de l'IHÉS*, 78, 5–161.
3. Bosch, S., Güntzer, U., & Remmert, R. (1984). *Non-Archimedean Analysis*. Springer.
4. Fresnel, J. & van der Put, M. (2004). *Rigid Analytic Geometry and Its Applications*. Birkhäuser.
5. Temkin, M. (2015). Introduction to Berkovich analytic spaces. In *Berkovich Spaces and Applications*, Springer Lecture Notes 2119, 3–66.
6. Baker, M. & Rumely, R. (2010). *Potential Theory and Dynamics on the Berkovich Projective Line*. AMS Mathematical Surveys and Monographs, 159.

---

*Chapter 3 of the Ultrametric Foundation Thesis. Next: Chapter 4 — Tate-Amice Spectral Analysis.*
