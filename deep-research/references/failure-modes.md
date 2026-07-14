# Failure Modes & Remedies — Deep-Research Pipeline

> Load this reference when: a stage produces weak/questionable output, the model seems stuck, or red-team iteration isn't productive. Each stage's failures, causes, and remedies are documented below.

---

## Stage 0: Domain Scoping

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Domain too broad ("all of physics") | No boundary constraint | Narrow to a subfield or intersection. A good domain has ~50-500 active research groups |
| Domain too narrow ("my specific grant proposal") | Cannot identify multiple paradigm candidates | Widen to the field that would be affected |
| Rate-of-change estimate is guesswork | No quantitative indicators used | Use citation velocity, preprint growth rate, or funding trajectory as proxy metrics |
| Historical precedent is cherry-picked | Confirmation bias in selecting "analogous" past shifts | Require at least 2 counter-examples (shifts that DIDN'T happen when expected) |
| Reference class examples are too distant ("astrology was once a paradigm") | Cherry-picking weak historical analogs | Reference class must be within the same field or a closely adjacent field with similar methodology |

---

## Stage 1: Finding Synthesis

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Only finding what confirms the field's narrative | Confirmation bias from canonical sources | Actively search for "crisis in [field]," "replication failure [field]," "unexplained anomaly [field]" |
| Over-reliance on recent papers (recency bias) | API results sorted by date | Require at least 5 papers from 5+ years ago (classics that defined the current framework) |
| Treating high citation count as quality signal | Confusing popularity with truth | Cross-reference with replication status. Flag all unreplicated high-citation papers |
| Missing the most important anomaly | The anomaly is too strange to be in mainstream venues | Search fringe/conference proceedings, preprints with "unexpected," "anomalous," "puzzling" in titles |

---

## Stage 2: Candidate Generation

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| All candidates look like incremental progress | Risk aversion; avoiding bold claims | Force at least one candidate per horizon that, if true, would make the current field's textbooks obsolete |
| 100+ year candidates are too vague ("we'll understand everything") | No constraint on long-range speculation | Each 100+ year candidate must specify a concrete falsification test (even if we can't run it) |
| Candidates are not mutually distinguishable | They overlap too much — a single observation confirms/refutes all of them | Ensure at least one discriminating observation exists between every pair of candidates |
| Missing "dark horse" candidates | Only considering the consensus-adjacent possibilities | Deliberately search for heterodox views: controversial papers, outsider perspectives, retired scientists' speculations |
| Continuity Baseline omitted or given trivial prior | Forecasting bias — wanting to find revolutions | Enforce: Continuity Baseline must use reference class base rate from Stage 0. If P(continuity) < 0.50 over any multi-decade window, flag [BASE-RATE-NEGLECT] |

---

## Stage 3: Assumption Audit

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Enabling assumptions are too vague ("new technology will exist") | Avoiding specificity | Every assumption must be tagged with a concrete observable: "technology X with specification Y available at cost Z" |
| All assumptions rated [MEDIUM] | Uncertainty aversion | Force at least one [HIGH] and one [LOW] per candidate |
| Falsification criteria are unfalsifiable ("we'll know it when we see it") | Avoiding commitment | Every falsification criterion must include: observation, instrument/method, by-when date, and what counts as "yes" vs "no" |
| Counterfactual is a strawman | Red-team lite | The counterfactual must be genuinely plausible — it should make you uncertain about the original candidate |

---

## Stage 4: Red-Team Iteration

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Red-team is performative ("good point, but the candidate still stands") | Social desirability bias; LLM avoids confrontation | Role-play each adversary with genuine commitment. The empiricist MUST find at least one evidential weakness |
| All candidates SURVIVE | Red-team too weak | If >80% survive, the red-team is broken. Restart with stricter criteria or add a 6th adversary |
| All candidates KILLED | Red-team too aggressive or candidates too weak | Distinguish "currently unsupported" from "falsified." A candidate without evidence is WOUNDED, not KILLED |
| Iteration converges to same answer | Red-team fixed points | After 2 iterations, if the same debate repeats, accept the current state and move on |

---

## Stage 5: Bayesian Model

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Priors are too uniform (all ~0.30-0.70) | Anchoring to indifference | Use base-rate calibration: what's the historical frequency of shifts in this domain? That's your anchor |
| Dependencies create unrealistic cascades (EV > sum of parts) | Double-counting impact in the cascade sum | Verify: EV_total ≤ Σ I(shift_i) — total EV cannot exceed total impact |
| Portfolio selects too many shifts (budget constraint non-binding) | Resource costs too low relative to budget | Normalize costs so budget buys exactly 30-50% of candidates |
| Sensitivity analysis shows everything is fragile | No robust findings | Identify which assumption, if varied, does NOT change the portfolio. That's your robust finding |
| Portfolio changes when all priors are halved | Subjective priors dominate the model | Flag [PRIOR-SENSITIVE]. Consider expert elicitation, reference class tightening, or reporting a range rather than point estimates |
| Mermaid DAG is not rendered | Skipping the visual step | The DAG loses its audibility without visualization. Always render as Mermaid after constructing the dependency structure |

---

## Stage 6: Thesis Optimization

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Thesis is too safe ("X may be important") | Avoiding falsifiability | The thesis must assert something a reasonable person could disagree with |
| Alternative futures are all variants of the same story | Failure of imagination | Force the wildcard scenario: what if the most-cited finding in the field is wrong? |
| Signposts timeline has no intermediate checkpoints | All-or-nothing thinking | Insert at least one checkpoint per 5-year interval in the first 20 years |

---

## Stage 7: Roadmap

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Phase 0 requires resources the LLM doesn't have | Forgetting LLM scope constraints | All Phase 0 tasks must use: web search, public APIs, code execution, file I/O only |
| Go/no-go criteria are always "go" | No real decision gates | Each gate must have at least one condition that would realistically fail |
| Roadmap doesn't account for funding cycles | Assuming infinite resources | Map phases to standard grant cycles (3-5 years each) |

---

## Stage 8: Self-Critique

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Self-critique is dismissive ("these are minor issues") | Defensiveness about generated work | Each blind spot must have a severity of at least [SIGNIFICANT] — if none do, you're not looking hard enough |
| All blind spots are about "lack of data" | Generic catch-all | At least one blind spot must be methodological (is the Bayesian framework itself misleading here?) |
| Missing the LLM-centered blind spot | Forgetting you're an LLM | What does the training data distribution bias? What post-training events could change everything? |

---

## Stage 9: Calibration Register

| Failure Mode | Cause | Remedy |
|:-------------|:------|:-------|
| Calibration register omitted ("this forecast is too speculative to track") | Avoiding accountability | A forecast without a register is unfalsifiable storytelling. The register disciplines speculation |
| Falsification tests have no concrete deadline | Avoiding commitment | Every test must specify a check date. "By 2030" is acceptable; "eventually" is not |
| All predictions classified as INCONCLUSIVE at check time | Falsification tests are unfalsifiable | Redesign tests so a clear yes/no observation is possible within the check window |

---

## Cross-Cutting Failure Modes

| Pattern | Detection | Fix |
|:--------|:----------|:----|
| **Template compliance over thinking:** Output follows the structure perfectly but contents are hollow | Each stage's digest reveals no insight you couldn't have guessed before starting | Restart with a narrower domain and higher bar for what counts as "surprising" |
| **Overconfidence cascade:** Early-stage overconfidence propagates and compounds | Most candidates have P > 0.5 and most assumptions are [HIGH] | Apply a blanket 0.7× multiplier to all priors and re-run |
| **Garbage in, garbage out:** Domain scoping was poor and everything downstream is noise | Stage 2-5 outputs feel disconnected from the domain you know | Go back to Stage 0 and re-scope |

---

> **Version:** v1.0
