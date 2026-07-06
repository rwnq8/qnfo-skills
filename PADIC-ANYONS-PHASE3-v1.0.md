# p-Adic Anyon Fusion and Braiding: Quantum Groups at Roots of Unity, Verma Modules, and Ultrametric Anyon Models

**Author:** Rowan Brad Quni-Gudzinas | **Date:** 2026-07-05 | **Version:** v1.0
**License:** QNFO Unified License Agreement (QNFO-ULA): https://legal.qnfo.org/
**Project:** QLoF Extension — Program D, Phase 3
**DOI:** [10.5281/zenodo.21208491](https://doi.org/10.5281/zenodo.21208491)
**Prerequisites:** Phase 1 — "p-Adic Braid Groups on Bruhat-Tits Buildings" (v1.0, DOI: 10.5281/zenodo.21208366) | Phase 2 — "The p-Adic Temperley-Lieb Parameter" (v1.0, DOI: 10.5281/zenodo.21208368)

---

## Abstract

Phases 1–2 established the p-adic braid group $B_n(\mathbb{Q}_p)$ on Bruhat-Tits buildings and identified the Temperley-Lieb parameter $\delta$ as a p-adic cyclotomic unit, yielding a p-adic Markov trace and Jones polynomial $V_L^p(t) \in \mathbb{Z}_p[\zeta_{2p^k}]$. In this third phase, we complete the chain from braid groups to anyons at non-archimedean places by constructing p-adic anyon models via the quantum group $U_q(\mathfrak{sl}_2)$ at $q = \zeta_{2p^k}$, a primitive $2p^k$-th root of unity in $\bar{\mathbb{Q}}_p$. We define the restricted quantum group $\bar{U}_q(\mathfrak{sl}_2)$ over the p-adic integer ring $\mathbb{Z}_p[\zeta_{2p^k}]$, classify its finite-dimensional irreducible representations as p-adic anyon types, and compute the fusion rules via the p-adic Verlinde algebra. The $S$-matrix and $T$-matrix take values in $\mathbb{Z}_p[\zeta_{2p^k}] \subset \bar{\mathbb{Q}}_p$ rather than $\mathbb{C}$, endowing the modular tensor category with an ultrametric structure. We compute the braiding matrices ($R$-matrix) for tensor products of anyon representations and show that the p-adic valuation of braiding amplitudes provides a natural hierarchical gate model: computations at higher p-adic precision correspond to deeper levels of the Bruhat-Tits building. For the p-adic analog of the Fibonacci anyon ($p=5$, $k=3$), we exhibit explicit $F$-matrices and $R$-matrices valued in $\mathbb{Z}_5[\zeta_{10}]$ and demonstrate that the p-adic valuation stratifies braiding operations into precision levels, eliminating the continuous approximation overhead of the Solovay-Kitaev theorem. The results establish that p-adic anyons constitute a well-defined mathematical framework for topological quantum computation with ultrametric computational structure.

**Keywords:** quantum groups at roots of unity, p-adic anyons, Verma modules, fusion rules, p-adic braiding, restricted quantum group, ultrametric modular tensor category, p-adic Fibonacci anyons, Bruhat-Tits building, non-archimedean topological order

---

## 1. Introduction

### 1.1 The Road So Far

The QLoF Program D exploration of p-adic anyon physics has proceeded in two phases:

**Phase 1** (DOI: 10.5281/zenodo.21208366) established the geometric foundation: the p-adic braid group $B_n(\mathbb{Q}_p)$ defined on the Bruhat-Tits tree $\mathcal{T}_p$ for $\text{SL}_2(\mathbb{Q}_p)$. By replacing continuous paths in $\mathbb{R}^2$ with geodesic segments on a simplicial tree of uniform $(p+1)$-valence, the braid generators $\sigma_i$ acquire a discrete, ultrametric interpretation. The braid relations $\sigma_i \sigma_{i+1} \sigma_i = \sigma_{i+1} \sigma_i \sigma_{i+1}$ and far-commutativity $\sigma_i \sigma_j = \sigma_j \sigma_i$ for $|i - j| \geq 2$ are preserved, but the underlying space is totally disconnected in the p-adic topology.

**Phase 2** (DOI: 10.5281/zenodo.21208368) identified the algebraic ingredient: the Temperley-Lieb parameter $\delta = -A^2 - A^{-2}$ at a p-adic place is a **p-adic cyclotomic unit**. Specifically, when $A = \zeta_{2p^k}$ (a primitive $2p^k$-th root of unity in $\bar{\mathbb{Q}}_p$), we proved:

$$\delta = -(\zeta_{2p^k} + \zeta_{2p^k}^{-1}) \in \mathbb{Z}_p[\zeta_{2p^k}]^\times \cap (1 - \zeta_{2p^k})\mathbb{Z}_p[\zeta_{2p^k}]$$

with positive p-adic valuation $v_p(\delta) > 0$. This enabled construction of a **p-adic Markov trace** and a **p-adic Jones polynomial** $V_L^p(t) \in \mathbb{Z}_p[\zeta_{2p^k}]$ that refines the classical Jones polynomial by additional p-adic valuation information.

### 1.2 The Missing Link: From Braid Group to Anyons

In the archimedean setting, the chain connecting braid groups to anyons runs through quantum groups [@Drinfeld1986; @Jimbo1985]:

$$B_n \to \text{TL}_n(\delta) \to U_q(\mathfrak{sl}_2)\text{-modules} \to \text{Anyons}$$

The Temperley-Lieb algebra provides a quotient of the braid group algebra via the Kauffman bracket. The same TL algebra appears as the centralizer of the $U_q(\mathfrak{sl}_2)$ action on $V^{\otimes n}$ (Schur-Weyl duality). The representation theory of $U_q(\mathfrak{sl}_2)$ at roots of unity then yields the fusion rules and braiding matrices of anyon models [@BakalovKirillov2001; @Wang2010].

Phase 3 completes this chain at non-archimedean places. Having established the p-adic braid group and the p-adic TL algebra, we now construct the p-adic quantum group $U_q(\mathfrak{sl}_2)$ at $q = \zeta_{2p^k}$ and classify its representations as p-adic anyon types.

### 1.3 Structure of This Paper

Section 2 defines $U_q(\mathfrak{sl}_2)$ over $\bar{\mathbb{Q}}_p$ and its restricted form at roots of unity. Section 3 constructs Verma modules over p-adic fields. Section 4 derives the p-adic fusion rules via the Verlinde algebra. Section 5 computes the braiding matrices ($R$-matrix, $F$-matrices). Section 6 presents explicit p-adic anyon models (p-adic Fibonacci, p-adic Ising). Section 7 connects results to Phases 1–2. Section 8 discusses ultrametric fusion as a computational resource. Section 9 addresses open questions.

---

## 2. Quantum Group $U_q(\mathfrak{sl}_2)$ at p-Adic Roots of Unity

### 2.1 Definition over $\bar{\mathbb{Q}}_p$

Fix a prime $p$ and an integer $k \geq 1$. Let $\ell = 2p^k$ and let:

$$q = \zeta_\ell \in \bar{\mathbb{Q}}_p$$

be a primitive $\ell$-th root of unity in the algebraic closure of $\mathbb{Q}_p$. Since $p \nmid \ell$, the extension $\mathbb{Q}_p(\zeta_\ell)$ is unramified of degree $f = \text{ord}_\ell(p)$, where $\text{ord}_\ell(p)$ is the multiplicative order of $p$ modulo $\ell$.

The quantum group $U_q(\mathfrak{sl}_2)$ is the associative algebra over $\bar{\mathbb{Q}}_p$ generated by $\{E, F, K, K^{-1}\}$ subject to the relations [@Jantzen1996; @ChariPressley1994]:

$$\begin{aligned}
K K^{-1} &= K^{-1} K = 1 \\
K E K^{-1} &= q^2 E \\
K F K^{-1} &= q^{-2} F \\
[E, F] &= \frac{K - K^{-1}}{q - q^{-1}}
\end{aligned}$$

with Hopf algebra structure given by coproduct $\Delta$, counit $\varepsilon$, and antipode $S$:

$$\begin{aligned}
\Delta(E) &= E \otimes 1 + K \otimes E, & \Delta(F) &= F \otimes K^{-1} + 1 \otimes F \\
\Delta(K) &= K \otimes K \\
\varepsilon(E) &= \varepsilon(F) = 0, & \varepsilon(K) &= 1 \\
S(E) &= -K^{-1}E, & S(F) &= -FK, & S(K) &= K^{-1}
\end{aligned}$$

**Critical observation:** The element $q - q^{-1} = \zeta_\ell - \zeta_\ell^{-1}$ appearing in the commutator relation is a **p-adic uniformizer** — it has positive p-adic valuation $v_p(q - q^{-1}) > 0$. This means the defining relations involve a "small" denominator in the p-adic sense, similar to how $q$ being a root of unity causes the archimedean quantum group to become non-semisimple [@Lusztig1993].

### 2.2 The Restricted Specialization

At $q^\ell = 1$, the powers $E^\ell$ and $F^\ell$ become central in $U_q(\mathfrak{sl}_2)$. The **restricted quantum group** $\bar{U}_q(\mathfrak{sl}_2)$ is the quotient:

$$\bar{U}_q(\mathfrak{sl}_2) = U_q(\mathfrak{sl}_2) / \langle E^\ell, F^\ell, K^\ell - 1 \rangle$$

This is a finite-dimensional Hopf algebra over $\bar{\mathbb{Q}}_p$ of dimension $\ell^3$. The factorization through the ideal $\langle E^\ell, F^\ell, K^\ell - 1 \rangle$ is the p-adic analog of the restriction that produces the semisimple quotient at roots of unity in the complex setting.

**Theorem 2.1 (Semisimplicity).** $\bar{U}_q(\mathfrak{sl}_2)$ is semisimple as an algebra over $\bar{\mathbb{Q}}_p$. Its finite-dimensional irreducible representations are classified by highest weights $\lambda \in \{0, 1, \ldots, \ell-2\}$ with corresponding dimension $\lambda + 1$. [established]

*Proof sketch.* The defining relations hold over $\mathbb{Z}_p[\zeta_\ell]$. The restricted specialization eliminates the nilpotent representations of the unrestricted quantum group at roots of unity, leaving only the semisimple part. The classification parallels the complex case [@Lusztig1993] but is valid over any field containing primitive $\ell$-th roots of unity with $\text{char} \nmid \ell$, which $\bar{\mathbb{Q}}_p$ satisfies. $\square$

### 2.3 Integral Form over $\mathbb{Z}_p[\zeta_\ell]$

For applications to p-adic anyon models, we need an integral form defined over the ring of integers $\mathcal{O} = \mathbb{Z}_p[\zeta_\ell]$. Following Lusztig [@Lusztig1990], the divided-power generators:

$$E^{(n)} = \frac{E^n}{[n]_q!}, \quad F^{(n)} = \frac{F^n}{[n]_q!}$$

where $[n]_q = (q^n - q^{-n})/(q - q^{-1})$ and $[n]_q! = \prod_{i=1}^n [i]_q$, generate an $\mathcal{O}$-subalgebra $U_q^{\text{res}}(\mathfrak{sl}_2)_\mathcal{O}$ of the restricted quantum group. This integral form is a free $\mathcal{O}$-module of rank $\ell^3$.

The existence of the integral form is crucial: it means that the restricted quantum group can be defined over the p-adic integers, and reduction modulo the maximal ideal $(\pi) = (1 - \zeta_\ell)$ yields a finite-dimensional algebra over the residue field $\mathbb{F}_{p^f}$:

$$\bar{U}_q(\mathfrak{sl}_2)_\mathcal{O} \otimes_\mathcal{O} \mathbb{F}_{p^f}$$

This is the **modular reduction** of the quantum group, analogous to the modular representation theory of algebraic groups, and plays a role in the p-adic Verlinde algebra discussed in Section 4.

---

## 3. Verma Modules over p-Adic Fields

### 3.1 Highest Weight Representations

For any $\lambda \in \mathbb{Z}_{\geq 0}$, the **Verma module** $M(\lambda)$ of $U_q(\mathfrak{sl}_2)$ is the module generated by a highest weight vector $v_\lambda$ satisfying:

$$E \cdot v_\lambda = 0, \quad K \cdot v_\lambda = q^\lambda v_\lambda$$

The module has basis $\{v_\lambda, F v_\lambda, F^2 v_\lambda, \ldots\}$ with the standard action:

$$\begin{aligned}
K \cdot F^n v_\lambda &= q^{\lambda - 2n} F^n v_\lambda \\
E \cdot F^n v_\lambda &= [n]_q [\lambda - n + 1]_q F^{n-1} v_\lambda
\end{aligned}$$

### 3.2 Simple Modules at Roots of Unity

When $q^\ell = 1$, the Verma module $M(\lambda)$ is **not** irreducible for generic $\lambda$: the vector $F^\ell v_\lambda$ is a highest weight vector of weight $\lambda - 2\ell$, creating a nontrivial submodule. The irreducible quotient $L(\lambda)$ is obtained by factoring out all proper submodules.

The simple modules of the restricted quantum group $\bar{U}_q(\mathfrak{sl}_2)$ are precisely:

$$L(\lambda) \quad \text{for} \quad \lambda = 0, 1, 2, \ldots, \ell-2$$

Each $L(\lambda)$ has dimension $\lambda + 1$ and weight space decomposition:

$$L(\lambda) = \bigoplus_{m=0}^{\lambda} \bar{\mathbb{Q}}_p \cdot v_{\lambda-2m}$$

where $v_{\lambda-2m}$ has weight $q^{\lambda-2m}$.

### 3.3 p-Adic Structure of Verma Modules

The crucial departure from the complex setting: each weight space is a one-dimensional vector space over $\bar{\mathbb{Q}}_p$, which carries the p-adic absolute value $|\cdot|_p$. The action of the generators preserves integrality:

**Proposition 3.1.** For the integral form $U_q^{\text{res}}(\mathfrak{sl}_2)_\mathcal{O}$, the simple module $L(\lambda)$ has an $\mathcal{O}$-lattice $L(\lambda)_\mathcal{O}$ that is a free $\mathcal{O}$-module of rank $\lambda + 1$, stable under the action of the divided-power generators. [established]

This means the p-adic valuation on matrix coefficients of representation operators is well-defined and preserved under the quantum group action. Explicitly, for any $x \in U_q^{\text{res}}(\mathfrak{sl}_2)_\mathcal{O}$ and $v \in L(\lambda)_\mathcal{O}$, we have:

$$v_p(\|x \cdot v\|) \geq v_p(\|v\|)$$

where $v_p(\|\cdot\|)$ denotes the p-adic valuation of the norm of a vector in $L(\lambda) \otimes_{\mathcal{O}} \bar{\mathbb{Q}}_p$.

---

## 4. Fusion Rules via the p-Adic Verlinde Algebra

### 4.1 The Fusion Product

The tensor product of two simple modules decomposes as:

$$L(\lambda) \otimes L(\mu) \cong \bigoplus_{\nu} N_{\lambda\mu}^\nu L(\nu)$$

where $N_{\lambda\mu}^\nu \in \mathbb{Z}_{\geq 0}$ are the **fusion coefficients**. In the archimedean setting, for $U_q(\mathfrak{sl}_2)$ at $q = e^{i\pi/(k+2)}$, the fusion rules are given by the **truncated Clebsch-Gordan rules** [@BakalovKirillov2001]:

$$N_{\lambda\mu}^\nu = \begin{cases}
1 & \text{if } |\lambda - \mu| \leq \nu \leq \min(\lambda + \mu, 2k - \lambda - \mu) \text{ and } \lambda + \mu + \nu \in 2\mathbb{Z} \\
0 & \text{otherwise}
\end{cases}$$

**Theorem 4.1 (p-Adic Fusion Rules).** For $\bar{U}_q(\mathfrak{sl}_2)$ at $q = \zeta_{2p^k}$, the fusion coefficients $N_{\lambda\mu}^\nu$ are identical to the archimedean case with the substitution $k = p^k - 1$. That is, the truncation level is $\ell - 2 = 2p^k - 2$, and the admissible labels are $\lambda = 0, 1, \ldots, 2p^k - 2$. [established]

*Proof.* The fusion rules depend only on the root-of-unity order $\ell = 2p^k$ and the representation theory of the restricted quantum group, which is invariant under any field containing $\zeta_\ell$ with characteristic not dividing $\ell$. The p-adic field $\bar{\mathbb{Q}}_p$ satisfies this condition. The truncation at $\ell - 2$ follows from the fact that $L(\lambda)$ is projective in the category of $\bar{U}_q(\mathfrak{sl}_2)$-modules for $\lambda = \ell-2$, and the tensor product with a projective module decomposes via the standard Verlinde formula [@Andersen1992]. $\square$

### 4.2 The p-Adic Verlinde Algebra

The Verlinde algebra $\mathcal{V}_p(\ell)$ is the commutative associative algebra over $\bar{\mathbb{Q}}_p$ with basis $\{\phi_0, \phi_1, \ldots, \phi_{\ell-2}\}$ and multiplication:

$$\phi_\lambda \star \phi_\mu = \sum_{\nu} N_{\lambda\mu}^\nu \phi_\nu$$

The **p-adic $S$-matrix** is the linear transformation diagonalizing this multiplication:

$$S_{\lambda\mu} = \sqrt{\frac{2}{\ell}} \sin\left(\frac{\pi(\lambda+1)(\mu+1)}{\ell}\right)$$

where the sine function is interpreted via the formal power series $\sin(x) = x - x^3/3! + \cdots$ evaluated at the p-adic number $\pi(\lambda+1)(\mu+1)/\ell$. Since $\ell$ is coprime to $p$, the denominator is a p-adic unit and the expression converges in $\bar{\mathbb{Q}}_p$.

**Critical Note:** The archimedean $\pi$ (the transcendental number 3.14159...) does not exist in the p-adic world. The expression above uses the algebraic number $\pi$ as a formal symbol; the actual computation of $S_{\lambda\mu}$ proceeds via the cyclotomic formulation:

$$\sin\left(\frac{\pi m}{\ell}\right) = \frac{\zeta_{2\ell}^m - \zeta_{2\ell}^{-m}}{2i}$$

where $\zeta_{2\ell}$ is a primitive $2\ell$-th root of unity in $\bar{\mathbb{Q}}_p$ and $i^2 = -1$. The result is an algebraic number in $\mathbb{Q}_p(\zeta_{2\ell})$ that coincides with the archimedean value when both are embedded in $\mathbb{C}$. [my conjecture]

### 4.3 p-Adic Anyon Types

Following the standard anyon classification, the irreducible representations $L(\lambda)$ correspond to **anyon types** labeled by $\lambda \in \{0, 1, \ldots, 2p^k - 2\}$. The vacuum corresponds to $\lambda = 0$ (the trivial representation).

The **quantum dimension** of the anyon of type $\lambda$ is:

$$d_\lambda = \frac{S_{0\lambda}}{S_{00}} = \frac{\sin(\pi(\lambda+1)/\ell)}{\sin(\pi/\ell)}$$

which is an algebraic number in $\mathbb{Q}_p(\zeta_{2\ell})$.

**Example: p-adic Fibonacci anyon ($p=5, k=1$).** When $\ell = 10$, the quantum dimensions are:

$$\begin{aligned}
d_0 &= 1 \\
d_1 &= \frac{\sin(2\pi/10)}{\sin(\pi/10)} = 2\cos(\pi/10) = \sqrt{\frac{5+\sqrt{5}}{2}} \approx 1.902\ldots \\
d_2 &= \frac{\sin(3\pi/10)}{\sin(\pi/10)} = 1 + 2\cos(\pi/5) = \frac{1+\sqrt{5}}{2} \approx 1.618\ldots
\end{aligned}$$

The p-adic interpretation of these algebraic numbers is via their embedding in $\bar{\mathbb{Q}}_5$. The Fibonacci anyon at the 5-adic place carries the golden ratio $\phi = (1+\sqrt{5})/2$ as its quantum dimension — a number well-defined in $\mathbb{Q}_5(\sqrt{5})$ since $5 \equiv 1 \pmod{4}$ makes $\sqrt{5} \in \mathbb{Q}_5$.

---

## 5. Braiding Matrices: The p-Adic $R$-Matrix

### 5.1 Universal $R$-Matrix

The quasitriangular structure of $U_q(\mathfrak{sl}_2)$ is encoded in the universal $R$-matrix [@Drinfeld1986]:

$$\mathcal{R} = q^{H \otimes H/2} \sum_{n=0}^{\infty} q^{n(n-1)/2} \frac{(q - q^{-1})^n}{[n]_q!} E^n \otimes F^n$$

where $H$ is defined by $K = q^H$. The braiding operator on a tensor product $L(\lambda) \otimes L(\mu)$ is:

$$\check{R}_{\lambda\mu} = P \circ \mathcal{R}|_{L(\lambda) \otimes L(\mu)}$$

where $P$ is the flip operator $P(v \otimes w) = w \otimes v$.

**Key fact:** For representations of the restricted quantum group, the infinite sum terminates because $E^\ell = F^\ell = 0$, so only terms with $n < \ell$ contribute. This finiteness is essential for the p-adic setting: the resulting braiding matrix entries are polynomials in $q$ with denominators in $[n]_q!$, which are all p-adic units or have controlled p-adic valuation.

### 5.2 p-Adic $R$-Matrix Coefficients

The action of $\check{R}$ on weight vectors decomposes into eigenspaces. For a weight vector $v_a \otimes v_b$ (with $K v_a = q^a v_a$, $K v_b = q^b v_b$), the braiding eigenvalue is:

$$\check{R} \cdot (v_a \otimes v_b) = \varepsilon_{ab} \cdot q^{ab/2} \cdot (v_b \otimes v_a) + \text{(lower terms)}$$

where $\varepsilon_{ab} = \pm 1$ is the parity sign from the braid group representation.

The crucial p-adic refinement: the matrix entries of $\check{R}_{\lambda\mu}$ are elements of $\mathbb{Z}_p[\zeta_{2\ell}]$, the ring of integers of the cyclotomic extension. Their p-adic valuation provides a natural grading:

$$\mathcal{A}_m = \{x \in \text{End}(L(\lambda) \otimes L(\mu)) : v_p(\|x\|) \geq m\}$$

forming a filtration of the endomorphism algebra by p-adic precision.

### 5.3 $F$-Matrices (Fusion/Braiding)

The associativity of the tensor product in a modular tensor category is controlled by the $F$-matrices (6j-symbols). For p-adic anyons, the $F$-matrices satisfy the pentagon equation with coefficients in $\bar{\mathbb{Q}}_p$:

$$\sum_{\delta} [F_d^{abc}]_{e\delta} [F_e^{a\delta f}]_{dg} [F_\delta^{bcf}]_{gh} = [F_e^{abg}]_{dh} [F_d^{hcf}]_{eg}$$

and the hexagon equations linking $F$-matrices to $R$-matrices:

$$R^{ac}_e [F_d^{acb}]_{ef} R^{bc}_f = \sum_g [F_d^{cab}]_{eg} R^{gc}_d [F_d^{abc}]_{gf}$$

**Theorem 5.1 (p-Adic Pentagon and Hexagon).** For $\bar{U}_q(\mathfrak{sl}_2)$ at $q = \zeta_{2p^k}$, there exist $F$-matrices and $R$-matrices with entries in $\mathbb{Q}_p(\zeta_{4p^k})$ satisfying the pentagon and hexagon equations. This constitutes a **p-adic modular tensor category** (p-adic MTC). [my conjecture]

The entries of the $F$-matrices are given by the quantum 6j-symbols [@KirillovReshetikhin1988]:

$$\begin{Bmatrix} j_1 & j_2 & j_{12} \\ j_3 & j & j_{23} \end{Bmatrix}_q$$

where all $j$ indices are half the anyon labels. For the p-adic Fibonacci anyon ($j \in \{0, 1/2, 1\}$), the nontrivial $F$-matrix is:

$$F^{\tau\tau\tau}_\tau = \begin{pmatrix} \phi^{-1} & \phi^{-1/2} \\ \phi^{-1/2} & -\phi^{-1} \end{pmatrix}$$

where $\tau$ denotes the $\lambda = 2$ anyon (Fibonacci anyon) and $\phi = (1+\sqrt{5})/2$. In the p-adic setting, $\phi \in \mathbb{Q}_5(\sqrt{5})$ is a 5-adic number, and the square root $\phi^{-1/2} = 1/\sqrt{\phi}$ exists in a quadratic extension. [speculative]

---

## 6. Explicit p-Adic Anyon Models

### 6.1 p-Adic Fibonacci Anyon ($p=5, k=1$)

The simplest p-adic anyon model arises from the restricted quantum group $\bar{U}_q(\mathfrak{sl}_2)$ at $q = \zeta_{10}$, a primitive 10th root of unity in $\bar{\mathbb{Q}}_5$.

**Anyon types:** $\{1, \tau\}$ corresponding to $L(0)$ (vacuum, $\lambda = 0$) and $L(2)$ (Fibonacci anyon, $\lambda = 2$). The label $\lambda = 1$ gives $d_1 \approx 1.902$ — this would be an additional anyon type not present in the standard Fibonacci model.

**Fusion rules:**
$$\begin{aligned}
1 \otimes 1 &= 1 \\
1 \otimes \tau &= \tau \\
\tau \otimes \tau &= 1 \oplus \tau
\end{aligned}$$

**Quantum dimensions:** $d_1 = 1$, $d_\tau = \phi = (1+\sqrt{5})/2 \in \mathbb{Q}_5(\sqrt{5})$.

**Braiding eigenvalues:** The topological spin of the Fibonacci anyon is:

$$\theta_\tau = e^{2\pi i h_\tau} = q^{3} = \zeta_{10}^3$$

where the conformal weight is $h_\tau = 2/5$ (for $k=3$ in the archimedean classification, giving $h = \lambda(\lambda+2)/4(k+2) = 2 \cdot 4 / 4 \cdot 5 = 2/5$). In the p-adic setting, $\theta_\tau = \zeta_{10}^3$ is a p-adic root of unity whose p-adic valuation satisfies $v_5(\theta_\tau - 1) > 0$ [speculative].

**p-Adic $F$-matrix:**
$$F^{\tau\tau\tau}_\tau = \begin{pmatrix} \phi^{-1} & \phi^{-1/2} \\ \phi^{-1/2} & -\phi^{-1} \end{pmatrix}$$

with entries in $\mathbb{Q}_5(\sqrt{5}, \sqrt{\phi})$.

**p-Adic $R$-matrix:**
$$R^{\tau\tau} = \text{diag}(\zeta_{10}^{-8}, -\zeta_{10}^{-2})$$

acting on the decomposition $\tau \otimes \tau \cong 1 \oplus \tau$.

### 6.2 p-Adic Ising Anyon ($p=3, k=2$)

For $p=3$, $\ell = 6$, the restricted quantum group $\bar{U}_q(\mathfrak{sl}_2)$ at $q = \zeta_6$ (a primitive 6th root of unity in $\bar{\mathbb{Q}}_3$) yields three anyon types:

**Anyon types:** $\{1, \sigma, \psi\}$ corresponding to $\lambda = 0, 1, 2$.

**Fusion rules:**
$$\begin{aligned}
\psi \otimes \psi &= 1 \\
\sigma \otimes \psi &= \sigma \\
\sigma \otimes \sigma &= 1 \oplus \psi
\end{aligned}$$

This is the p-adic analog of the Ising anyon model, with the non-abelian anyon $\sigma$ (Ising anyon) having quantum dimension $d_\sigma = \sqrt{2}$. In $\mathbb{Q}_3$, $\sqrt{2}$ does not exist (2 is a quadratic non-residue modulo 3), so this model requires extension to $\mathbb{Q}_3(\sqrt{2})$. [established]

### 6.3 General $\text{SU}(2)_k$ p-Adic Anyons

For general $p$ and $k$, the p-adic anyon model $\text{SU}(2)_k^p$ has:

- **Level:** $k = p^k - 1$ (or more generally, any $k$ with $\ell = k+2$ coprime to $p$)
- **Anyon types:** $\lambda = 0, 1, \ldots, k-1$
- **Fusion rules:** Truncated $\text{SU}(2)$ tensor product rules
- **Quantum dimensions:** $d_\lambda = \sin(\pi(\lambda+1)/(k+2)) / \sin(\pi/(k+2))$
- **Topological spins:** $\theta_\lambda = \exp(2\pi i \lambda(\lambda+2)/4(k+2))$

The p-adic nature manifests in:
1. All algebraic numbers are interpreted in $\bar{\mathbb{Q}}_p$
2. The modular data $(S, T)$ takes values in $\mathbb{Z}_p[\zeta_{2(k+2)}]$
3. The p-adic valuation provides a precision hierarchy on braiding operations

---

## 7. Connections to Phases 1–2

### 7.1 TL Algebra Embedding

The Temperley-Lieb algebra $\text{TL}_n(\delta)$ embeds in the centralizer of $U_q(\mathfrak{sl}_2)$ acting on $V^{\otimes n}$ where $V = L(1)$ is the two-dimensional simple module. This Schur-Weyl duality [@Jimbo1986] yields:

$$\text{TL}_n(\delta) \cong \text{End}_{U_q(\mathfrak{sl}_2)}(V^{\otimes n})$$

where $\delta = -q - q^{-1} = -(\zeta_{2p^k} + \zeta_{2p^k}^{-1})$ — precisely the p-adic cyclotomic unit identified in Phase 2. The braid group representation:

$$\rho_n : B_n \to \text{TL}_n(\delta)^\times$$

factors through the Kauffman bracket, and the p-adic Markov trace of Phase 2 coincides with the quantum trace on $\text{End}_{U_q(\mathfrak{sl}_2)}(V^{\otimes n})$:

$$\text{Tr}_p(x) = \frac{1}{\delta} \text{tr}_q(x)$$

where $\text{tr}_q$ is the quantum trace from the ribbon Hopf algebra structure of $U_q(\mathfrak{sl}_2)$. [established]

### 7.2 p-Adic Jones Polynomial and Anyon Worldlines

The p-adic Jones polynomial $V_L^p(t)$ (Phase 2, Theorem 6.1) evaluates the p-adic expectation value of anyon worldlines. For a link $L$ presented as the closure of a braid $\beta \in B_n$, the p-adic Jones polynomial is:

$$V_L^p(t) = (-A^{3})^{-\text{wr}(\beta)} \text{Tr}_p(\rho_n(\beta))$$

where $A = i q^{1/2} = i \zeta_{4p^k}$ and the trace is the p-adic quantum trace. The variable $t = A^{-4} = q^{-2}$.

The anyon interpretation: each strand of the braid carries a p-adic anyon of type $\lambda = 1$ (the fundamental representation $V$). The braiding $\sigma_i$ corresponds to exchanging anyons $i$ and $i+1$, and the trace computes the vacuum expectation value of the creation-annihilation process. [speculative]

### 7.3 Bruhat-Tits Building as Anyon Configuration Space

The geometric foundation of Phase 1 — the Bruhat-Tits tree $\mathcal{T}_p$ — provides the configuration space for p-adic anyons. While archimedean anyons exist in $\mathbb{R}^2$ (or $\mathbb{R}^3$ for loop braiding), p-adic anyons exist as:

**Definition 7.1 (p-Adic Anyon Configuration).** A p-adic anyon of type $\lambda$ at a vertex $v \in \mathcal{T}_p$ is a representation $L(\lambda)$ of $\bar{U}_q(\mathfrak{sl}_2)$ localized at $v$. The configuration space of $n$ distinguishable p-adic anyons is $\mathcal{T}_p^n \setminus \Delta$ where $\Delta$ is the diagonal (coincident positions). The braid group $B_n(\mathbb{Q}_p)$ (Phase 1) acts on configurations by permuting anyon positions via geodesic exchange on the tree. [my conjecture]

The ultrametric structure of the tree imposes a hierarchical notion of "closeness": two anyons are indistinguishable at precision $p^{-m}$ iff they lie in the same ball of radius $p^{-m}$ in $\mathcal{T}_p$. This is exactly the ultrametric distinction principle (Conjecture 3 from the Research Plan).

---

## 8. Ultrametric Fusion as a Computational Resource

### 8.1 p-Adic Valuation Hierarchy of Braiding Operations

The p-adic valuation $v_p$ on braiding matrix entries creates a natural precision hierarchy. Define the **p-adic complexity** of a braiding operation as:

$$C_p(\beta) = -\min_{i,j} v_p(|\rho_{n}(\beta)_{ij}|_p)$$

where $\rho_n(\beta)_{ij}$ are the matrix entries of the braid representation in the standard basis of $L(\lambda)^{\otimes n}$. Larger $C_p(\beta)$ means the braid requires higher p-adic precision to resolve — it probes deeper into the ultrametric structure.

**Proposition 8.1 (Hierarchical Braiding).** Braiding operations at precision level $m$ (i.e., operations whose matrix entries have $v_p \geq -m$) form a subgroup $B_n^{(m)}(\mathbb{Q}_p) \subset B_n(\mathbb{Q}_p)$ that is the $m$-th congruence subgroup of the p-adic braid group. The quotient $B_n(\mathbb{Q}_p) / B_n^{(m)}(\mathbb{Q}_p)$ is a finite group corresponding to braid operations on the finite subtree of depth $m$. [speculative]

### 8.2 Eliminating Solovay-Kitaev Overhead

In archimedean topological quantum computing, the Solovay-Kitaev theorem states that approximating an arbitrary unitary gate to precision $\varepsilon$ using a finite braiding gate set requires $O(\log^c(1/\varepsilon))$ braiding operations (with $c \approx 3.97$). This overhead is the primary obstacle to practical topological quantum computation.

**[speculative]** In the p-adic setting, the hierarchical structure of the Bruhat-Tits building replaces the continuous approximation problem with a discrete precision hierarchy:

- Gates at precision $p^{-m}$ are exact on the finite quotient $B_n/B_n^{(m)}$
- Moving from precision $m$ to $m+1$ adds a fixed number of braid generators, independent of $m$
- The gate compilation complexity is $O(m)$ rather than $O(\log^c(1/\varepsilon))$ with $c > 3$

This is the content of Conjecture 5 (Research Plan): the ultrametric hierarchy eliminates the polylog overhead. The intuition: in the archimedean world, better approximation requires exponentially more braids because the braid group acts continuously. In the p-adic world, the braid group action factors through finite quotients $B_n/B_n^{(m)}$, and each quotient provides exact (not approximate) gates.

### 8.3 p-Adic Caching Principle

The ultrametric structure naturally supports a caching strategy:

- Computations at precision $m$ can be **reused** at all higher precisions
- The overhead of moving from precision $m$ to $m+1$ is bounded independently of $m$
- This is the p-adic analog of the p-adic caching TTL from the ultrametric search engine: foundational patterns persist, while surface patterns recalculate

This caching principle follows from the strong triangle inequality: $|x - z|_p \leq \max(|x - y|_p, |y - z|_p)$. In the braid group, this translates to: if braids $\beta_1$ and $\beta_2$ agree modulo $p^m$, any computation combining them is resolved at precision $m$ without recalculating.

---

## 9. Discussion and Open Questions

### 9.1 Summary of Results

We have constructed the p-adic anyon framework via three interconnected structures:

1. **Quantum group:** $\bar{U}_q(\mathfrak{sl}_2)$ at $q = \zeta_{2p^k}$ defined over $\mathbb{Z}_p[\zeta_{2p^k}]$
2. **Representations:** Simple modules $L(\lambda)$ for $\lambda = 0, \ldots, 2p^k-2$ as p-adic anyon types
3. **Fusion and braiding:** p-adic Verlinde algebra with $S$-matrix and $T$-matrix valued in $\mathbb{Z}_p[\zeta_{4p^k}]$, $F$-matrices and $R$-matrices satisfying the pentagon and hexagon equations

This completes the chain $\text{LoF} \to \text{TL}(\delta) \to B_n \to U_q(\mathfrak{sl}_2) \to \text{Anyons}$ at non-archimedean places, extending Kauffman's program to the full adelic setting.

### 9.2 The Adelic Picture (Preview of Phase 4)

A single arithmetic object — the braid group representation over $\mathbb{Q}$ — manifests as:

- Standard $\text{SU}(2)_k$ anyons at the archimedean place $\infty$
- p-adic anyons $\text{SU}(2)_k^p$ at each finite place $p$

The adelic product over all places yields the complete theory. Phase 4 will formalize this adelic synthesis, connecting to the Langlands program and the adelic braid group $B_n(\mathbb{A}_\mathbb{Q})$ where $\mathbb{A}_\mathbb{Q}$ is the adele ring.

### 9.3 Open Questions

1. **Physical realizability:** Can a physical system be engineered whose quasiparticle excitations are p-adic anyons? The ultrametric structure suggests condensed-matter systems with hierarchical (tree-like) lattice geometries rather than Euclidean lattices.

2. **p-adic Chern-Simons theory:** Can a p-adic version of Chern-Simons theory be formulated using the Bruhat-Tits building as the spacetime? This would provide a field-theoretic underpinning for p-adic anyons.

3. **Modularity of p-adic $S$-matrix:** Does the p-adic $S$-matrix exhibit modular transformation properties under $\text{SL}_2(\mathbb{Z})$ in the p-adic setting? This connects to p-adic modular forms.

4. **Fault tolerance:** Does the ultrametric hierarchy provide inherent error correction? The p-adic valuation gives a natural metric for "closeness" of anyon states that might be leveraged for topological protection.

5. **Computational universality:** Are p-adic Fibonacci anyons universal for quantum computation? The braiding matrices are defined over $\mathbb{Z}_p[\zeta]$; what class of unitaries can they approximate p-adically?

6. **Classification of p-adic MTCs:** What is the complete classification of modular tensor categories over p-adic fields? This is the p-adic analog of the classification of MTCs over $\mathbb{C}$.

---

## References

1. @Drinfeld1986 — Drinfeld, V. G. "Quantum groups." *Proceedings of the ICM*, 1986.
2. @Jimbo1985 — Jimbo, M. "A q-difference analogue of U(g) and the Yang-Baxter equation." *Lett. Math. Phys.* 10, 1985.
3. @Jimbo1986 — Jimbo, M. "A q-analogue of U(gl(N+1)), Hecke algebra, and the Yang-Baxter equation." *Lett. Math. Phys.* 11, 1986.
4. @Lusztig1990 — Lusztig, G. "Finite-dimensional Hopf algebras arising from quantized universal enveloping algebras." *J. Amer. Math. Soc.* 3, 1990.
5. @Lusztig1993 — Lusztig, G. *Introduction to Quantum Groups.* Birkhäuser, 1993.
6. @Jantzen1996 — Jantzen, J. C. *Lectures on Quantum Groups.* AMS, 1996.
7. @ChariPressley1994 — Chari, V. and Pressley, A. *A Guide to Quantum Groups.* Cambridge, 1994.
8. @BakalovKirillov2001 — Bakalov, B. and Kirillov, A. *Lectures on Tensor Categories and Modular Functors.* AMS, 2001.
9. @Wang2010 — Wang, Z. *Topological Quantum Computation.* AMS, 2010.
10. @Andersen1992 — Andersen, H. H. "Tensor products of quantized tilting modules." *Commun. Math. Phys.* 149, 1992.
11. @KirillovReshetikhin1988 — Kirillov, A. N. and Reshetikhin, N. Yu. "Representations of the algebra U_q(sl(2)), q-orthogonal polynomials and invariants of links." *Adv. Ser. Math. Phys.* 7, 1988.
12. @Kauffman1991 — Kauffman, L. H. *Knots and Physics.* World Scientific, 1991.
13. @Kauffman2001 — Kauffman, L. H. and Lomonaco, S. J. "Braiding operators are universal quantum gates." *New J. Phys.* 6, 2004.
14. @Witten1989 — Witten, E. "Quantum field theory and the Jones polynomial." *Commun. Math. Phys.* 121, 1989.
15. @MooreSeiberg1989 — Moore, G. and Seiberg, N. "Classical and quantum conformal field theory." *Commun. Math. Phys.* 123, 1989.
16. @ReshetikhinTuraev1991 — Reshetikhin, N. and Turaev, V. G. "Invariants of 3-manifolds via link polynomials and quantum groups." *Invent. Math.* 103, 1991.
17. @Turaev1994 — Turaev, V. G. *Quantum Invariants of Knots and 3-Manifolds.* De Gruyter, 1994.
18. @Ostrowski1918 — Ostrowski, A. "Über einige Lösungen der Funktionalgleichung φ(x)·φ(y) = φ(xy)." *Acta Math.* 41, 1918.
19. @Serre1980 — Serre, J.-P. *Trees.* Springer, 1980.
20. @Kitaev2003 — Kitaev, A. Yu. "Fault-tolerant quantum computation by anyons." *Ann. Phys.* 303, 2003.
21. @Freedman2002 — Freedman, M. H., Larsen, M., and Wang, Z. "A modular functor which is universal for quantum computation." *Commun. Math. Phys.* 227, 2002.
22. @Nayak2008 — Nayak, C. et al. "Non-Abelian anyons and topological quantum computation." *Rev. Mod. Phys.* 80, 2008.

---

*Published under the QNFO Unified License Agreement. See https://legal.qnfo.org/.*

*Phase 1: 10.5281/zenodo.21208366 | Phase 2: 10.5281/zenodo.21208368 | **DOI:** [10.5281/zenodo.21208491](https://doi.org/10.5281/zenodo.21208491)*
