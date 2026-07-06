# Beyond the Archimedean Anyon: p-Adic Braid Groups, Ultrametric Distinction, and the Adelic Pattern-Particle Correspondence

**Author:** Rowan Brad Quni-Gudzinas | **Date:** 2026-07-05 | **Version:** v1.2 (Research Plan — All 4 Phases Published)
**License:** QNFO Unified License Agreement (QNFO-ULA): https://legal.qnfo.org/
**Project:** QLoF Extension — Program D (p-adic Anyons & Ultrametric Braid Groups)
**DOI:** [10.5281/zenodo.21208370](https://doi.org/10.5281/zenodo.21208370)

**Note:** v1.0 was lost during thin-client cleanup (R2 upload failed). v1.1 reconstructs from tape evidence.

---

## Abstract

Kauffman's program established rigorous connections from Spencer-Brown's calculus of indications to the Temperley-Lieb algebra, the Jones polynomial, and topological quantum computing. The chain $\text{LoF} \cong \text{TL}(\delta) \to \text{Braid Group} \to \text{Anyons} \to \text{Topological QC}$ is mathematically correct but physically incomplete: Fibonacci anyons have never been experimentally confirmed; the gate overhead from the Solovay-Kitaev theorem is prohibitive; and the "anyon" concept itself presupposes an archimedean continuum that Ostrowski's theorem shows is only one of infinitely many equally fundamental completions of $\mathbb{Q}$. This research plan proposes to reconstruct anyon physics at non-archimedean places: defining p-adic braid groups on Bruhat-Tits buildings, identifying the TL algebra parameter $d = A^2 + A^{-2}$ with p-adic cyclotomic units, and reframing the "anyon" as an adelic avatar — a pattern that manifests differently at each place, with the real-number anyon being a single special case. The central conjecture is that ultrametric braid group representations provide a more natural setting for topological quantum computation because the hierarchical structure of Bruhat-Tits buildings eliminates the continuous-braiding overhead that makes archimedean anyons prohibitive.

---

## 1. Introduction: What Kauffman Actually Proved

### 1.1 The Established Correspondences

Kauffman's program [@Kauffman1991; @Kauffman2001; @Kauffman2019] established the following chain of rigorous mathematical relationships:

1. **Laws of Form $\to$ Temperley-Lieb Algebra**: The primary algebra of Spencer-Brown (two axioms: calling and crossing) is isomorphic to the Temperley-Lieb algebra $\text{TL}(\delta)$ at the Jones parameter $\delta = -A^2 - A^{-2}$. The marked state corresponds to the TL idempotent; the unmarked cross corresponds to the TL generator $U_i$ satisfying $U_i^2 = \delta U_i$ and $U_i U_{i\pm 1} U_i = U_i$.

2. **TL Algebra $\to$ Braid Group $\to$ Knot Invariants**: The TL algebra supports a Markov trace which yields the Jones polynomial $V_L(t)$ via the Kauffman bracket. Braid group representations $\sigma_i = AI + A^{-1}U_i$ factor through the TL algebra, giving diagrammatic proofs of knot invariance.

3. **Braid Group $\to$ Anyons $\to$ Topological QC**: In 2+1 dimensions, particle exchange is governed by the braid group $B_n$ rather than the permutation group $S_n$. Non-abelian anyons (specifically Fibonacci anyons at level $k=3$ $\text{SU}(2)$ Chern-Simons theory) are universal for quantum computation: braiding approximates any unitary gate via the Solovay-Kitaev theorem.

### 1.2 What the Chain Does NOT Prove

The critical gap: every step in this chain is constructed over $\mathbb{R}$ or $\mathbb{C}$ — archimedean completions of $\mathbb{Q}$. Ostrowski's theorem [@Ostrowski1918] states that the only non-trivial absolute values on $\mathbb{Q}$ are the archimedean absolute value $|\cdot|_\infty$ and the p-adic absolute values $|\cdot|_p$ for each prime $p$. The chain:

$$\text{LoF} \to \text{TL}(\delta) \to B_n \to \text{Anyons} \to \text{TQC}$$

...has only been verified at the $\infty$ place. The non-archimedean places are completely unexplored.

**Question:** Can the same chain be constructed at a p-adic place? If so, does it yield different physics — and potentially more computationally useful — anyon species?

---

## 2. Five Central Conjectures

**Conjecture 1 (p-adic Braid Group Existence):** There exists a well-defined p-adic braid group $B_n(\mathbb{Q}_p)$ on the Bruhat-Tits building $\mathcal{B}(\text{SL}_n, \mathbb{Q}_p)$ whose standard generators $\sigma_i$ satisfy the braid relations $\sigma_i\sigma_{i+1}\sigma_i = \sigma_{i+1}\sigma_i\sigma_{i+1}$ and whose geometric interpretation involves parallel transport along geodesics in the building rather than continuous paths in $\mathbb{R}^2$.

**Conjecture 2 (Ultrametric TL Parameter):** The TL algebra parameter $\delta = -A^2 - A^{-2}$ at a p-adic place naturally takes values in the cyclotomic units $\mathbb{Z}_p[\zeta_{p^k}]$, making $A$ a $p^k$-th root of unity. This connects to the standard anyon fusion rules via $A = e^{i\pi/(k+2)}$ at the archimedean place, which lifts to a p-adic root of unity via the embedding $\bar{\mathbb{Q}} \hookrightarrow \bar{\mathbb{Q}}_p$.

**Conjecture 3 (Ultrametric Distinction Principle):** In the p-adic setting, particle "indistinguishability" acquires a hierarchical structure: two patterns are distinguishable at precision $\varepsilon$ iff their p-adic distance satisfies $|x - y|_p > \varepsilon$. This replaces the binary distinguishable/indistinguishable dichotomy with a hierarchical nesting of equivalence classes — exactly the structure of a Bruhat-Tits building.

**Conjecture 4 (Adelic Anyon Correspondence):** An "anyon" is an adelic avatar — a single arithmetic object that manifests as a standard anyon at the archimedean place $\infty$ and as a distinct "p-adic anyon" at each finite place $p$. The adelic product over all places yields the complete pattern: the same braid group representation, evaluated at different completions, yields different physical (and computational) properties.

**Conjecture 5 (Hierarchy → Gate Efficiency):** The ultrametric structure of the Bruhat-Tits building eliminates the Solovay-Kitaev overhead. In the archimedean setting, approximating a gate to precision $\varepsilon$ requires $O(\log^c(1/\varepsilon))$ braids. In the p-adic setting, the hierarchical geometry of the building means gates at different precision levels live on different apartment levels, yielding $O(1)$ gate compilation subject to p-adic caching principles.

---

## 3. Research Phases

### Phase 1: Define p-Adic Braid Groups on Bruhat-Tits Buildings ✅ PUBLISHED

**DOI:** [10.5281/zenodo.21208366](https://doi.org/10.5281/zenodo.21208366)

**Goal:** Construct a mathematically rigorous definition of $B_n(\mathbb{Q}_p)$ on the Bruhat-Tits building $\mathcal{B}(\text{SL}_n, \mathbb{Q}_p)$.

**Key steps:**

1. **Bruhat-Tits building as configuration space:** The standard braid group $B_n$ is $\pi_1(\text{Conf}_n(\mathbb{R}^2))$ where $\text{Conf}_n(\mathbb{R}^2)$ is the configuration space of $n$ distinct points in $\mathbb{R}^2$. The p-adic analog replaces $\mathbb{R}^2$ with $\mathbb{Q}_p^2$ and the configuration space with the space of $n$ distinct vertices in the Bruhat-Tits tree $\mathcal{T}_p$ for $\text{SL}_2(\mathbb{Q}_p)$.

2. **Bruhat-Tits building fundamentals:** The Bruhat-Tits building for $\text{SL}_n(\mathbb{Q}_p)$ is a simplicial complex whose vertices correspond to homothety classes of lattices in $\mathbb{Q}_p^n$. Apartments are Euclidean spaces of dimension $n-1$. The building is CAT(0) and has a natural metric.

3. **Geodesic braiding on the tree:** For $\text{SL}_2(\mathbb{Q}_p)$, the building is a $(p+1)$-regular tree $\mathcal{T}_p$. Braid generators $\sigma_i$ correspond to the operation of swapping two lattice homothety classes by moving them along geodesics in the tree. The key difference from $\mathbb{R}^2$: the tree has discrete branching, so braiding is inherently discrete.

4. **Arithmetic braid group:** Define generators and relations:
   - Generators $\sigma_1, \ldots, \sigma_{n-1}$
   - Braid relations: $\sigma_i\sigma_{i+1}\sigma_i = \sigma_{i+1}\sigma_i\sigma_{i+1}$
   - Commutation: $\sigma_i\sigma_j = \sigma_j\sigma_i$ for $|i - j| > 1$
   - Additional p-adic relations coming from the building geometry
   
5. **Comparison with classical braid group:** Show that $B_n(\mathbb{Q}_p)$ reduces to the standard $B_n$ in the limit $p \to \infty$ (the "archimedean limit") or when evaluated at the generic fiber over $\mathbb{C}_p$.

**Deliverables:**
- Phase 1 paper: "p-Adic Braid Groups on Bruhat-Tits Buildings" (paper.md + paper.pdf)
- Python scripts demonstrating p-adic braid computations
- R2 upload + KG seeding

### Phase 2: Identify TL Algebra Parameter with p-Adic Cyclotomic Units ✅ PUBLISHED

**DOI:** [10.5281/zenodo.21208368](https://doi.org/10.5281/zenodo.21208368)

**Goal:** Prove that the TL algebra parameter $\delta = -A^2 - A^{-2}$ at a p-adic place is naturally a p-adic cyclotomic unit, connecting the Jones polynomial evaluation at roots of unity to p-adic valuations.

### Phase 3: Define p-Adic Anyon Fusion and Braiding ✅ PUBLISHED

**DOI:** [10.5281/zenodo.21208491](https://doi.org/10.5281/zenodo.21208491)

**Goal:** Construct p-adic anyon models using Verma modules over $U_q(\mathfrak{sl}_2)$ with $q$ a $p^k$-th root of unity. Compute fusion rules and braiding matrices.

### Phase 4: Adelic Synthesis — The Pattern-Particle Correspondence ✅ PUBLISHED

**DOI:** [10.5281/zenodo.21208568](https://doi.org/10.5281/zenodo.21208568)

**Goal:** Unify archimedean and non-archimedean anyon theories via the adelic framework. Show that "anyons" are adelic patterns and that the full physical theory requires ALL places, not just $\infty$.

**Result:** Constructed the adelic braid group $\mathbb{B}_n(\mathbb{A})$, adelic Temperley-Lieb algebra $\mathbb{TL}(\mathbb{A})$, and adelic anyon fusion category $\mathcal{F}(\mathbb{A})$. Proved the Pattern-Particle Correspondence: anyon types are adelic patterns, with the same Verma module $V_j$ manifesting differently at each completion. Computed the adelic Verlinde algebra factorization. Proposed Adelic Topological Quantum Computation (ATQC) paradigm.

---

## 4. Methodology

Each phase follows the QNFO/QWAV research protocol:

1. **Literature grounding** — arXiv + Semantic Scholar for existing work
2. **Mathematical construction** — rigorous definitions, theorems, proofs
3. **Computational verification** — Python/sage scripts for examples and counter-examples
4. **Publication** — Markdown paper → PDF → Zenodo → Cloudflare Pages → R2 → KG
5. **Gate enforcement** — Red-team + DoD after every phase

---

## 5. References

1. Kauffman, L.H. (1991). *Knots and Physics*. World Scientific. [@Kauffman1991]
2. Kauffman, L.H. (2001). The mathematics of Charles Sanders Peirce. *Cybernetics & Human Knowing*. [@Kauffman2001]
3. Kauffman, L.H. (2019). Laws of Form and the logic of non-duality. *Progress in Biophysics & Molecular Biology*. [@Kauffman2019]
4. Spencer-Brown, G. (1969). *Laws of Form*. Allen & Unwin. [@SpencerBrown1969]
5. Jones, V.F.R. (1985). A polynomial invariant for knots via von Neumann algebras. *Bull. AMS*. [@Jones1985]
6. Ostrowski, A. (1918). Über einige Lösungen der Funktionalgleichung $\varphi(x)\varphi(y)=\varphi(xy)$. *Acta Math*. [@Ostrowski1918]
7. Bruhat, F. & Tits, J. (1972). Groupes réductifs sur un corps local. *Publ. Math. IHÉS*. [@BruhatTits1972]
8. Serre, J.-P. (1980). *Trees*. Springer. [@Serre1980]
9. Abramenko, P. & Brown, K.S. (2008). *Buildings: Theory and Applications*. Springer. [@AbramenkoBrown2008]
10. Kitaev, A.Y. (2003). Fault-tolerant quantum computation by anyons. *Annals of Physics*. [@Kitaev2003]
11. Nayak, C. et al. (2008). Non-abelian anyons and topological quantum computation. *Rev. Mod. Phys*. [@Nayak2008]
12. Freedman, M.H. et al. (2003). A magnetic model with a possible Chern-Simons phase. *Ann. Phys*. [@Freedman2003]
13. Temperley, H.N.V. & Lieb, E.H. (1971). Relations between the 'percolation' and 'colouring' problem. *Proc. R. Soc. Lond*. [@TemperleyLieb1971]
14. Witten, E. (1989). Quantum field theory and the Jones polynomial. *Comm. Math. Phys*. [@Witten1989]
15. Reshetikhin, N. & Turaev, V.G. (1991). Invariants of 3-manifolds via link polynomials and quantum groups. *Invent. Math*. [@ReshetikhinTuraev1991]
16. Drinfeld, V.G. (1987). Quantum groups. *Proc. ICM*. [@Drinfeld1987]
17. Jimbo, M. (1985). A q-difference analogue of U(g) and the Yang-Baxter equation. *Lett. Math. Phys*. [@Jimbo1985]
18. Goldman, W.M. & Iwahori, N. (1963). The space of p-adic norms. *Acta Math*. [@GoldmanIwahori1963]
19. Macdonald, I.G. (1971). *Spherical Functions on a Group of p-adic Type*. Ramanujan Institute. [@Macdonald1971]
20. Cartier, P. (1973). Géométrie et analyse sur les arbres. *Sém. Bourbaki*. [@Cartier1973]
21. Schneider, P. & Teitelbaum, J. (2002). Banach space representations and Iwasawa theory. *Israel J. Math*. [@SchneiderTeitelbaum2002]
22. Breuil, C. & Mézard, A. (2002). Multiplicités modulaires et représentations de $\text{GL}_2(\mathbb{Z}_p)$. *Duke Math. J*. [@BreuilMezard2002]
23. Colmez, P. (2010). Représentations de $\text{GL}_2(\mathbb{Q}_p)$ et $(\phi, \Gamma)$-modules. *Astérisque*. [@Colmez2010]
24. Ginzburg, V. & Kapranov, M. (1994). Koszul duality for operads. *Duke Math. J*. [@GinzburgKapranov1994]
25. Manin, Y.I. (1988). *Quantum Groups and Non-commutative Geometry*. CRM. [@Manin1988]
26. Khovanov, M. (2000). A categorification of the Jones polynomial. *Duke Math. J*. [@Khovanov2000]
27. Bourbaki, N. (1968). *Groupes et algèbres de Lie*, Ch. 4-6. Hermann. [@Bourbaki1968]
28. Quni-Gudzinas, R.B. (2026e). Adelic Synthesis: The Pattern-Particle Correspondence and the Complete Arithmetic Theory of Anyons. Zenodo. DOI: 10.5281/zenodo.21208568 [@QuniGudzinas2026e]
29. Tate, J. (1967). Fourier analysis in number fields and Hecke's zeta-functions. In *Algebraic Number Theory* (Cassels & Fröhlich, eds.). [@Tate1967]
30. Weil, A. (1967). *Basic Number Theory*. Springer. [@Weil1967]
31. Langlands, R.P. (1970). Problems in the theory of automorphic forms. *Lecture Notes in Math*. [@Langlands1970]

---

*PADIC-ANYONS-RESEARCH-PLAN v1.2 — All 4 Phases published. Phase 1 [10.5281/zenodo.21208366], Phase 2 [10.5281/zenodo.21208368], Phase 3 [10.5281/zenodo.21208491], Phase 4 [10.5281/zenodo.21208568]. Program complete.*
