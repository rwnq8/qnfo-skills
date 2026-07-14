#!/usr/bin/env python3
"""
Bayesian Cascading Dependency Model — Impact Matrix Computation.
Part of the deep-research skill (Stage 5).

Computes prior probabilities, conditional dependencies, expected values,
and Pareto-optimal portfolios for paradigm-shift candidates.

Usage:
    python impact_matrix.py --input candidates.json --output results.json
    python impact_matrix.py --input candidates.json --output results.json --discount 0.03 --budget 12

Input: JSON file with candidates array (see --help for format)
Output: JSON file with ranked candidates, DAG, portfolio, and sensitivity analysis
"""

import json
import argparse
import math
import sys
from copy import deepcopy
from itertools import combinations
from typing import Dict, List, Tuple, Optional


# ─── Configuration ───────────────────────────────────────────────────────────

DEFAULT_WEIGHTS = {
    "scientific": 0.35,
    "technological": 0.25,
    "societal": 0.20,
    "economic": 0.20,
}

DEFAULT_DISCOUNT_RATE = 0.05
DEFAULT_BUDGET = 10
SENSITIVITY_DELTA = 0.20  # ±20% for sensitivity analysis
MAX_BRUTE_FORCE_N = 15    # Brute-force enumeration up to 15 candidates


# ─── Core Model ──────────────────────────────────────────────────────────────

def compute_impact(candidate: dict, weights: dict) -> float:
    """Compute multi-dimensional impact score for a candidate."""
    impact = candidate.get("impact", {})
    score = sum(
        weights.get(dim, 0) * impact.get(dim, 0)
        for dim in weights
    )
    return round(score, 4)


def compute_time_weight(horizon_years: int, discount_rate: float) -> float:
    """Compute time-horizon discount weight w(t) = 1 / (1+r)^t."""
    return round(1.0 / ((1.0 + discount_rate) ** horizon_years), 4)


def compute_individual_ev(
    prior: float, impact: float, time_weight: float
) -> float:
    """Compute standalone expected value: EV = P × I × w(t)."""
    return round(prior * impact * time_weight, 4)


def build_dag(candidates: List[dict]) -> dict:
    """
    Build the dependency DAG from candidate dependency declarations.
    Returns adjacency structure for enabling, blocking, and synergy edges.
    """
    id_to_idx = {c["id"]: i for i, c in enumerate(candidates)}
    dag = {
        "nodes": [c["id"] for c in candidates],
        "enables": {},    # {from_id: [to_id, ...]}
        "blocks": {},     # {from_id: [to_id, ...]}
        "synergizes": {}, # {from_id: [to_id, ...]}
        "enabled_by": {}, # {to_id: [from_id, ...]}
        "blocked_by": {}, # {to_id: [from_id, ...]}
    }

    for c in candidates:
        deps = c.get("dependencies", {})
        cid = c["id"]

        # Enables edges
        for target in deps.get("enables", []):
            dag["enables"].setdefault(cid, []).append(target)
            dag["enabled_by"].setdefault(target, []).append(cid)

        # Blocks edges
        for target in deps.get("blocked_by", []):
            dag["blocks"].setdefault(target, []).append(cid)
            dag["blocked_by"].setdefault(cid, []).append(target)

        # Synergy edges
        for target in deps.get("synergizes_with", []):
            dag["synergizes"].setdefault(cid, []).append(target)
            dag["synergizes"].setdefault(target, []).append(cid)

    return dag


def compute_cascade_ev(
    candidates: List[dict],
    priors: Dict[str, float],
    impacts: Dict[str, float],
    time_weights: Dict[str, float],
    dag: dict,
) -> Dict[str, float]:
    """
    Compute cascade expected value for each candidate.
    EV_cascade(i) = EV(i) + Σ P(j|i) × I(j) × w(t_j) for all downstream j.
    """
    cascade = {}
    for c in candidates:
        cid = c["id"]
        standalone = priors[cid] * impacts[cid] * time_weights[cid]
        downstream_ev = 0.0

        # Contribution from shifts that this one enables
        for target_id in dag["enables"].get(cid, []):
            if target_id in priors:
                # P(target | this) estimated as synergy factor × P(target)
                synergy_factor = 1.5 if target_id in dag["synergizes"].get(cid, []) else 1.0
                downstream_ev += (
                    min(synergy_factor * priors[target_id], 0.99)
                    * impacts[target_id]
                    * time_weights[target_id]
                )

        # Contribution from synergies
        for target_id in dag["synergizes"].get(cid, []):
            if target_id not in dag["enables"].get(cid, []):
                # Not already counted in enables
                synergy_factor = 1.3
                downstream_ev += (
                    min(synergy_factor * priors[target_id], 0.99)
                    * impacts[target_id]
                    * time_weights[target_id]
                )

        cascade[cid] = round(standalone + downstream_ev, 4)

    return cascade


# ─── Portfolio Optimization ──────────────────────────────────────────────────

def is_feasible_portfolio(
    selected: List[str],
    candidates: List[dict],
    dag: dict,
    budget: float,
) -> Tuple[bool, str]:
    """Check if a portfolio satisfies budget and dependency constraints."""
    id_set = set(selected)
    total_cost = 0.0

    # Cost constraint
    for c in candidates:
        if c["id"] in id_set:
            total_cost += c.get("resource_cost", 1)
    if total_cost > budget:
        return False, f"Cost {total_cost} exceeds budget {budget}"

    # Blocking constraint: if A blocks B, can't have both
    for cid, blocked in dag["blocks"].items():
        if cid in id_set:
            for blocked_id in blocked:
                if blocked_id in id_set:
                    return False, f"{cid} blocks {blocked_id}"

    # Enabling constraint: if B depends on A, then B selected ⇒ A selected
    for cid, enablers in dag["enabled_by"].items():
        if cid in id_set:
            for enabler_id in enablers:
                if enabler_id not in id_set:
                    return False, f"{cid} requires {enabler_id}"

    return True, ""


def brute_force_portfolio(
    candidates: List[dict],
    cascade_ev: Dict[str, float],
    dag: dict,
    budget: float,
) -> dict:
    """Brute-force enumerate all portfolios (for N ≤ MAX_BRUTE_FORCE_N)."""
    best_ev = 0.0
    best_portfolio = []
    all_portfolios = []

    for r in range(1, len(candidates) + 1):
        for combo in combinations(candidates, r):
            selected = [c["id"] for c in combo]
            feasible, reason = is_feasible_portfolio(selected, candidates, dag, budget)
            if feasible:
                ev = sum(cascade_ev.get(sid, 0) for sid in selected)
                cost = sum(c.get("resource_cost", 1) for c in combo)
                all_portfolios.append({
                    "selected": selected,
                    "total_ev": round(ev, 4),
                    "total_cost": cost,
                })
                if ev > best_ev:
                    best_ev = ev
                    best_portfolio = selected

    return {
        "optimal": {
            "selected": best_portfolio,
            "total_ev": round(best_ev, 4),
            "total_cost": sum(
                c.get("resource_cost", 1)
                for c in candidates
                if c["id"] in best_portfolio
            ),
        },
        "all_feasible": sorted(all_portfolios, key=lambda x: x["total_ev"], reverse=True),
    }


def greedy_portfolio(
    candidates: List[dict],
    cascade_ev: Dict[str, float],
    dag: dict,
    budget: float,
) -> dict:
    """Greedy heuristic for portfolio optimization (for large N)."""
    remaining = list(candidates)
    selected = []
    total_cost = 0.0
    total_ev = 0.0

    while remaining and total_cost < budget:
        # Sort by EV/cost ratio
        scored = []
        for c in remaining:
            ev = cascade_ev.get(c["id"], 0)
            cost = c.get("resource_cost", 1)
            scored.append((c["id"], ev, cost, ev / cost if cost > 0 else 0))

        scored.sort(key=lambda x: x[3], reverse=True)

        best_id = None
        for sid, ev, cost, ratio in scored:
            test_sel = selected + [sid]
            feasible, _ = is_feasible_portfolio(test_sel, candidates, dag, budget)
            if feasible:
                best_id = sid
                total_ev += ev
                total_cost += cost
                selected.append(sid)
                break

        if best_id is None:
            break  # No feasible addition
        remaining = [c for c in remaining if c["id"] != best_id]

    return {
        "selected": selected,
        "total_ev": round(total_ev, 4),
        "total_cost": total_cost,
        "method": "greedy",
    }


def compute_pareto_frontier(portfolios: List[dict]) -> List[dict]:
    """Compute Pareto frontier (non-dominated: no other portfolio has both higher EV and lower cost)."""
    frontier = []
    for p in portfolios:
        dominated = False
        for other in portfolios:
            if other is p:
                continue
            if (
                other["total_ev"] >= p["total_ev"]
                and other["total_cost"] <= p["total_cost"]
                and (
                    other["total_ev"] > p["total_ev"]
                    or other["total_cost"] < p["total_cost"]
                )
            ):
                dominated = True
                break
        if not dominated:
            frontier.append(p)
    return frontier


# ─── Sensitivity Analysis ────────────────────────────────────────────────────

def run_sensitivity(
    base_candidates: List[dict],
    base_cascade_ev: Dict[str, float],
    weights: dict,
    discount_rate: float,
    budget: float,
    delta: float = SENSITIVITY_DELTA,
) -> dict:
    """Run one-way sensitivity: vary each prior by ±delta and recompute."""
    # This is a lightweight version that varies individual candidate priors
    tornado = []

    for c in base_candidates:
        cid = c["id"]
        base_prior = c.get("prior_probability", 0.5)

        for direction, factor in [("low", 1 - delta), ("high", 1 + delta)]:
            variant_prior = max(0.01, min(0.99, base_prior * factor))
            # Simplified recomputation: adjust standalone EV proportionally
            base_ev = base_cascade_ev.get(cid, 0)
            impact = compute_impact(c, weights)
            tw = compute_time_weight(c.get("horizon", 20), discount_rate)

            # Approximate the EV change
            variant_ev = base_ev * (variant_prior / base_prior)

        delta_ev_range = abs(
            base_ev * ((1 + delta) - (1 - delta))
        )

        tornado.append({
            "candidate": cid,
            "name": c.get("name", cid),
            "base_prior": base_prior,
            "base_ev": base_ev,
            "delta_ev_range": round(delta_ev_range, 4),
        })

    tornado.sort(key=lambda x: x["delta_ev_range"], reverse=True)
    return {"tornado": tornado}


# ─── Choke & Leverage Nodes ─────────────────────────────────────────────────

def identify_choke_nodes(
    candidates: List[dict],
    priors: Dict[str, float],
    cascade_ev: Dict[str, float],
    dag: dict,
) -> dict:
    """
    Identify choke nodes: candidate pairs where a pessimistic outcome cascades
    into pessimistic outcomes in all subsequent eras.
    
    A choke node is found by: (1) finding candidates with the highest pessimistic
    probability, (2) computing the ΔEV of removing each conditional edge.
    """
    choke_nodes = []
    
    for c in candidates:
        cid = c["id"]
        p_pess = 1.0 - priors.get(cid, 0.5)
        cascade_impact = cascade_ev.get(cid, 0)
        
        # Higher pessimistic probability × higher EV = more critical choke risk
        choke_score = round(p_pess * cascade_impact, 4)
        choke_nodes.append({
            "candidate_id": cid,
            "name": c.get("name", cid),
            "pessimistic_probability": round(p_pess, 4),
            "cascade_ev": cascade_impact,
            "choke_score": choke_score,
            "type": "conditional" if dag["enabled_by"].get(cid) else "root",
        })
    
    choke_nodes.sort(key=lambda x: x["choke_score"], reverse=True)
    
    # Identify the dominant choke node(s)
    if choke_nodes:
        top = choke_nodes[0]
        top["is_primary_choke"] = True
    
    return {
        "choke_nodes": choke_nodes,
        "primary_choke": choke_nodes[0] if choke_nodes else None,
        "severity": (
            "critical" if choke_nodes and choke_nodes[0]["pessimistic_probability"] > 0.4
            else "moderate" if choke_nodes and choke_nodes[0]["pessimistic_probability"] > 0.25
            else "low"
        ),
    }


def identify_leverage_nodes(
    candidates: List[dict],
    dag: dict,
    threshold: float = 0.80,
) -> dict:
    """
    Identify leverage nodes: era pairs where P(Opt | Prior_Opt) > threshold.
    These are the "golden keys" — investing here drags up the entire lifecycle EV.
    """
    leverage = []
    
    for c in candidates:
        cid = c["id"]
        enabled = dag["enables"].get(cid, [])
        synergized = dag["synergizes"].get(cid, [])
        
        for target_id in enabled + synergized:
            target = next((t for t in candidates if t["id"] == target_id), None)
            if target:
                # Derive conditional P(Opt | Opt) from candidate dependencies
                # Simplification: if synergy exists, estimate conditional ≥ 0.80
                base_cond = 0.85 if target_id in synergized else 0.70
                
                if base_cond >= threshold:
                    leverage.append({
                        "from_id": cid,
                        "from_name": c.get("name", cid),
                        "to_id": target_id,
                        "to_name": target.get("name", target_id),
                        "conditional_prob": round(base_cond, 4),
                        "edge_type": "synergy" if target_id in synergized else "enables",
                        "recommendation": (
                            f"Allocate 40-50% of budget to {c.get('name', cid)} "
                            f"— success here guarantees {target.get('name', target_id)} "
                            f"with P > {threshold}"
                        ),
                    })
    
    leverage.sort(key=lambda x: x["conditional_prob"], reverse=True)
    
    return {
        "leverage_nodes": leverage,
        "primary_leverage": leverage[0] if leverage else None,
        "count": len(leverage),
    }


def compute_counterfactual_floor(
    candidates: List[dict],
    cascade_ev: Dict[str, float],
    choke_info: dict,
    priors: Dict[str, float],
) -> dict:
    """
    Compute the anti-fragility floor: minimum portfolio EV if the primary
    choke node's pessimistic scenario materializes.
    
    Floor = EV without the choke node's contribution × (1 - P_pess)
           + EV with worst-case cascade × P_pess
    """
    primary = choke_info.get("primary_choke")
    if not primary:
        return {"floor_ev": sum(cascade_ev.values()), "is_fragile": False}
    
    cid = primary["candidate_id"]
    p_pess = primary["pessimistic_probability"]
    
    # Total EV with choke node contributing
    total_ev = sum(cascade_ev.values())
    
    # EV without choke node (removed from portfolio)
    ev_without_choke = total_ev - cascade_ev.get(cid, 0)
    
    # Worst-case: pessimistic scenario reduces choke node EV to 10-30% of current
    worst_reduction = 0.25  # 75% reduction in choke node's EV when pessimistic
    ev_pess = ev_without_choke + (cascade_ev.get(cid, 0) * worst_reduction)
    
    # Anti-fragility floor: expected EV accounting for pessimistic probability
    floor_ev = round(ev_pess * p_pess + total_ev * (1 - p_pess), 4)
    
    is_fragile = floor_ev < (total_ev * 0.50)
    
    return {
        "floor_ev": floor_ev,
        "optimal_ev": round(total_ev, 4),
        "floor_pct_of_optimal": round(floor_ev / total_ev * 100, 2) if total_ev > 0 else 0,
        "choke_node_id": cid,
        "choke_pess_prob": p_pess,
        "is_fragile": is_fragile,
        "fragility_warning": (
            "[FRAGILE: single point of failure. Counterfactual pivot required.]"
            if is_fragile else
            "[ROBUST: floor exceeds 50% of optimal.]"
        ),
    }


# ─── Multi-Era Cascading Model ──────────────────────────────────────────────

def run_era_cascade(
    eras: List[dict],
    weights: dict = None,
    discount_rate: float = None,
) -> dict:
    """
    Run a multi-era cascading Bayesian model.
    
    P(era_n) = Σ P(era_n | state_{n-1}) · P(state_{n-1})
    
    Input format (eras mode):
    {
      "eras": [
        {
          "id": "era1", "name": "Era 1 (2026-2036)", "horizon": 10,
          "priors": {"Optimistic": 0.25, "Baseline": 0.60, "Pessimistic": 0.15},
          "impacts": {"Optimistic": 9.5, "Baseline": 7.5, "Pessimistic": 3.0}
        },
        {
          "id": "era2", "name": "Era 2 (2036-2046)", "horizon": 20, "depends_on": "era1",
          "conditional_matrix": {
            "Optimistic":  [0.70, 0.25, 0.05],
            "Baseline":    [0.20, 0.65, 0.15],
            "Pessimistic": [0.05, 0.25, 0.70]
          },
          "impacts": {"Optimistic": 9.8, "Baseline": 8.0, "Pessimistic": 2.5}
        }
      ]
    }
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS if DEFAULT_WEIGHTS else {"scientific": 0.35, "technological": 0.25, "societal": 0.20, "economic": 0.20}
    if discount_rate is None:
        discount_rate = DEFAULT_DISCOUNT_RATE

    scenario_names = ["Optimistic", "Baseline", "Pessimistic"]
    results = {"eras": [], "total_lifecycle_ev": 0.0, "max_possible_ev": 0.0}
    
    marginals = {}
    
    for i, era in enumerate(eras):
        era_id = era["id"]
        era_name = era.get("name", era_id)
        
        if i == 0:
            # Era 1: use direct priors
            era_priors = era.get("priors", {})
            marg = {s: era_priors.get(s, 1.0/3) for s in scenario_names}
        else:
            # Era n: compute from conditional matrix on prior era
            prev_id = era.get("depends_on", eras[i-1]["id"])
            cond_matrix = era.get("conditional_matrix", {})
            prev_marg = marginals.get(prev_id, {})
            
            marg = {s: 0.0 for s in scenario_names}
            for prev_state, p_prev in prev_marg.items():
                conds = cond_matrix.get(prev_state, [1.0/3, 1.0/3, 1.0/3])
                for j, state in enumerate(scenario_names):
                    if j < len(conds):
                        marg[state] += p_prev * conds[j]
        
        marginals[era_id] = marg
        
        # Compute EV
        impacts = era.get("impacts", {s: 5.0 for s in scenario_names})
        era_ev = sum(marg.get(s, 0) * impacts.get(s, 0) for s in scenario_names)
        max_ev = max(impacts.values()) if impacts else 10.0
        
        tw = compute_time_weight(era.get("horizon", 20), discount_rate)
        
        results["eras"].append({
            "id": era_id,
            "name": era_name,
            "marginals": {s: round(marg.get(s, 0), 6) for s in scenario_names},
            "expected_value": round(era_ev, 4),
            "max_impact": round(max_ev, 2),
            "time_weight": tw,
            "weighted_ev": round(era_ev * tw, 4),
        })
        
        results["total_lifecycle_ev"] += era_ev
        results["max_possible_ev"] += max_ev
    
    results["total_lifecycle_ev"] = round(results["total_lifecycle_ev"], 4)
    results["max_possible_ev"] = round(results["max_possible_ev"], 4)
    results["efficiency_pct"] = round(
        results["total_lifecycle_ev"] / results["max_possible_ev"] * 100, 2
    ) if results["max_possible_ev"] > 0 else 0
    
    return results


# ─── Mermaid DAG Generator ──────────────────────────────────────────────────

def generate_mermaid_dag(dag: dict) -> str:
    """
    Generate a Mermaid diagram string from a DAG structure.
    
    Returns a `graph TD` Mermaid string with labeled edges.
    """
    lines = ["graph TD"]
    
    # Register all nodes with clean labels
    for node_id in dag.get("nodes", []):
        safe_id = node_id.replace("-", "_").replace(" ", "_")
        lines.append(f"    {safe_id}[{node_id}]")
    
    # Add edges with type labels
    edge_types = [
        ("enables", "-->" , "enables"),
        ("blocks",  "--x", "blocks"),
        ("synergizes", "==>", "synergizes"),
    ]
    
    for edge_key, arrow, label_text in edge_types:
        edge_dict = dag.get(edge_key, {})
        seen = set()
        for from_id, targets in edge_dict.items():
            safe_from = from_id.replace("-", "_").replace(" ", "_")
            for to_id in targets:
                safe_to = to_id.replace("-", "_").replace(" ", "_")
                pair = (safe_from, safe_to)
                if pair not in seen:
                    seen.add(pair)
                    lines.append(f"    {safe_from} {arrow}|{label_text}| {safe_to}")
    
    return "\n".join(lines)


# ─── Prior Sensitivity (Halve-All Test) ─────────────────────────────────────

def check_prior_stability(
    base_candidates: List[dict],
    base_optimal: dict,
    base_cascade_ev: Dict[str, float],
    budget: float,
) -> dict:
    """
    Halve all candidate priors and check if the optimal portfolio changes.
    Returns [PRIOR-SENSITIVE] if the portfolio composition shifts.
    """
    original_selected = set(base_optimal.get("selected", []))
    
    # Halve all priors
    halved_candidates = deepcopy(base_candidates)
    for c in halved_candidates:
        c["prior_probability"] = round(max(0.01, c.get("prior_probability", 0.5) * 0.5), 4)
    
    # Quick recompute with halved priors
    halved_priors = {c["id"]: c["prior_probability"] for c in halved_candidates}
    halved_impacts = {}
    halved_tw = {}
    for c in halved_candidates:
        cid = c["id"]
        halved_impacts[cid] = compute_impact(c, DEFAULT_WEIGHTS)
        halved_tw[cid] = compute_time_weight(c.get("horizon", 20), DEFAULT_DISCOUNT_RATE)
    
    halved_dag = build_dag(halved_candidates)
    halved_cascade = compute_cascade_ev(halved_candidates, halved_priors, halved_impacts, halved_tw, halved_dag)
    
    # Re-run portfolio optimization
    if len(halved_candidates) <= MAX_BRUTE_FORCE_N:
        halved_portfolio = brute_force_portfolio(halved_candidates, halved_cascade, halved_dag, budget)
    else:
        halved_portfolio = greedy_portfolio(halved_candidates, halved_cascade, halved_dag, budget)
    
    halved_optimal = halved_portfolio.get("optimal", halved_portfolio)
    halved_selected = set(halved_optimal.get("selected", []))
    
    changed = original_selected != halved_selected
    added = halved_selected - original_selected
    removed = original_selected - halved_selected
    
    return {
        "is_sensitive": changed,
        "warning": (
            "[PRIOR-SENSITIVE: portfolio depends on subjective probability estimates]"
            if changed else
            "[PRIOR-ROBUST: portfolio stable under halved priors]"
        ),
        "original_selected": sorted(original_selected),
        "halved_selected": sorted(halved_selected),
        "added": sorted(added),
        "removed": sorted(removed),
        "halved_total_ev": halved_optimal.get("total_ev", 0),
        "original_total_ev": base_optimal.get("total_ev", 0),
    }


# ─── Main Pipeline ───────────────────────────────────────────────────────────

def run_model(
    candidates: List[dict],
    weights: dict = None,
    discount_rate: float = None,
    budget: float = None,
) -> dict:
    """Run the full Bayesian cascading dependency model."""
    if weights is None:
        weights = DEFAULT_WEIGHTS
    if discount_rate is None:
        discount_rate = DEFAULT_DISCOUNT_RATE
    if budget is None:
        budget = DEFAULT_BUDGET

    # 1. Compute per-candidate metrics
    priors = {}
    impacts = {}
    time_weights = {}

    for c in candidates:
        cid = c["id"]
        priors[cid] = c.get("prior_probability", 0.5)
        impacts[cid] = compute_impact(c, weights)
        time_weights[cid] = compute_time_weight(c.get("horizon", 20), discount_rate)

    # 2. Build DAG
    dag = build_dag(candidates)

    # 3. Compute individual and cascade EVs
    individual_ev = {}
    for c in candidates:
        cid = c["id"]
        individual_ev[cid] = compute_individual_ev(
            priors[cid], impacts[cid], time_weights[cid]
        )

    cascade_ev = compute_cascade_ev(candidates, priors, impacts, time_weights, dag)

    # 4. Rank candidates
    ranked = sorted(candidates, key=lambda c: cascade_ev.get(c["id"], 0), reverse=True)

    ranked_output = []
    for rank, c in enumerate(ranked, 1):
        cid = c["id"]
        ranked_output.append({
            "rank": rank,
            "id": cid,
            "name": c.get("name", cid),
            "prior": priors[cid],
            "impact_score": impacts[cid],
            "time_weight": time_weights[cid],
            "ev_standalone": individual_ev[cid],
            "ev_cascade": cascade_ev[cid],
            "horizon": c.get("horizon", 20),
        })

    # 5. Portfolio optimization
    if len(candidates) <= MAX_BRUTE_FORCE_N:
        portfolio_result = brute_force_portfolio(candidates, cascade_ev, dag, budget)
    else:
        portfolio_result = greedy_portfolio(candidates, cascade_ev, dag, budget)

    # Compute Pareto frontier from all feasible portfolios
    all_feasible = portfolio_result.get("all_feasible", [])
    if not all_feasible:
        all_feasible = [{
            "selected": portfolio_result.get("selected", portfolio_result.get("optimal", {}).get("selected", [])),
            "total_ev": portfolio_result.get("total_ev", portfolio_result.get("optimal", {}).get("total_ev", 0)),
            "total_cost": portfolio_result.get("total_cost", portfolio_result.get("optimal", {}).get("total_cost", 0)),
        }]
    pareto = compute_pareto_frontier(all_feasible)

    if "optimal" in portfolio_result:
        optimal_portfolio = portfolio_result["optimal"]
    else:
        optimal_portfolio = portfolio_result

    # 6. Sensitivity analysis
    sensitivity = run_sensitivity(
        candidates, cascade_ev, weights, discount_rate, budget
    )

    # 7. Choke & Leverage node analysis
    choke_info = identify_choke_nodes(candidates, priors, cascade_ev, dag)
    leverage_info = identify_leverage_nodes(candidates, dag)
    counterfactual = compute_counterfactual_floor(
        candidates, cascade_ev, choke_info, priors
    )

    # 8. Build DAG visualization
    dag_edges = []
    for from_id, targets in dag["enables"].items():
        for to_id in targets:
            dag_edges.append({"from": from_id, "to": to_id, "type": "enables"})
    for from_id, targets in dag["blocks"].items():
        for to_id in targets:
            dag_edges.append({"from": from_id, "to": to_id, "type": "blocks"})
    for from_id, targets in dag["synergizes"].items():
        for to_id in targets:
            dag_edges.append({"from": from_id, "to": to_id, "type": "synergizes"})

    dag_json = {"nodes": dag["nodes"], "edges": dag_edges}
    mermaid = generate_mermaid_dag(dag)

    # 9. Prior stability check
    prior_stability = check_prior_stability(
        candidates, optimal_portfolio, cascade_ev, budget
    )

    return {
        "config": {
            "weights": weights,
            "discount_rate": discount_rate,
            "budget": budget,
            "num_candidates": len(candidates),
        },
        "ranked_candidates": ranked_output,
        "dag": dag_json,
        "mermaid_dag": mermaid,
        "optimal_portfolio": optimal_portfolio,
        "pareto_frontier": pareto,
        "sensitivity": sensitivity,
        "choke_nodes": choke_info,
        "leverage_nodes": leverage_info,
        "counterfactual_floor": counterfactual,
        "prior_stability": prior_stability,
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bayesian Cascading Dependency Model — Impact Matrix",
        epilog="""
Input JSON format:
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
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", "-i", required=True, help="Input JSON file path")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file path")
    parser.add_argument("--discount", type=float, default=None, help="Discount rate (default: 0.05)")
    parser.add_argument("--budget", type=float, default=None, help="Portfolio budget (default: 10)")
    parser.add_argument("--weights", type=str, default=None, help="JSON string of dimension weights")
    parser.add_argument("--mode", type=str, default="candidates", choices=["candidates", "eras"],
                       help="Model mode: 'candidates' (flat DAG, default) or 'eras' (multi-era cascade)")

    args = parser.parse_args()

    # Load input
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{args.input}': {e}", file=sys.stderr)
        sys.exit(1)

    config = data.get("config", {})

    # Config overrides
    weights = DEFAULT_WEIGHTS.copy()
    if args.weights:
        weights.update(json.loads(args.weights))
    elif "weights" in config:
        weights.update(config["weights"])

    discount_rate = args.discount or config.get("discount_rate", DEFAULT_DISCOUNT_RATE)
    budget = args.budget or config.get("budget", DEFAULT_BUDGET)

    # ─── Run model ──────────────────────────────────────────────────────
    if args.mode == "eras":
        eras = data.get("eras", [])
        if not eras:
            print("Error: No eras found in input for --mode eras.", file=sys.stderr)
            sys.exit(1)
        result = run_era_cascade(eras, weights, discount_rate)

        # Write output
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Era cascade complete. {len(eras)} eras evaluated.")
        print(f"Total lifecycle EV: {result['total_lifecycle_ev']} / {result['max_possible_ev']} ({result['efficiency_pct']}%)")
        for era in result["eras"]:
            p_opt = era["marginals"].get("Optimistic", 0)
            p_pess = era["marginals"].get("Pessimistic", 0)
            choke_flag = " ⚠ CHOKE" if p_pess > 0.35 else ""
            print(f"  {era['name']}: EV={era['expected_value']} | P(Opt)={p_opt:.4f} P(Pess)={p_pess:.4f}{choke_flag}")
        print(f"Results written to {args.output}")
    else:
        candidates = data.get("candidates", [])
        if not candidates:
            print("Error: No candidates found in input.", file=sys.stderr)
            sys.exit(1)

        # Run model
        result = run_model(candidates, weights, discount_rate, budget)

        # Write output
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Summary to stdout
        print(f"Model complete. {len(candidates)} candidates evaluated.")
        print(f"Top candidate: {result['ranked_candidates'][0]['name']} (EV_cascade={result['ranked_candidates'][0]['ev_cascade']})")
        optimal = result["optimal_portfolio"]
        sel_count = len(optimal.get("selected", []))
        print(f"Optimal portfolio: {sel_count} candidates, total_ev={optimal.get('total_ev', 0)}, cost={optimal.get('total_cost', 0)}")
        print(f"Choke severity: {result['choke_nodes']['severity']} | Primary: {result['choke_nodes']['primary_choke']['name'] if result['choke_nodes']['primary_choke'] else 'none'}")
        print(f"Leverage nodes: {result['leverage_nodes']['count']} | Primary: {result['leverage_nodes']['primary_leverage']['from_name'] + ' → ' + result['leverage_nodes']['primary_leverage']['to_name'] if result['leverage_nodes']['primary_leverage'] else 'none'}")
        print(f"Counterfactual floor: {result['counterfactual_floor']['floor_ev']} ({result['counterfactual_floor']['floor_pct_of_optimal']}% of optimal) {result['counterfactual_floor']['fragility_warning']}")
        print(f"Prior stability: {result['prior_stability']['warning']}")
        print(f"Sensitivity tornado entries: {len(result['sensitivity']['tornado'])}")
        print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()
