"""
Solvers and diagnostics for routing scenarios.
"""
from __future__ import annotations

from .bitstrings import decode_policy
from .energy import energy_table
from .scenarios import Scenario


def exact_solve(scenario: Scenario, top_k: int = 8) -> dict:
    """Solve a small binary scenario by complete enumeration."""
    table = energy_table(scenario)
    best = table[0]
    top = table[:top_k]
    return {
        "scenario": scenario.name,
        "description": scenario.description,
        "bit_labels": scenario.labels,
        "best_bitstring": best["bitstring"],
        "best_policy": decode_policy(best["bitstring"], scenario.labels),
        "best_energy": best["energy"],
        "top_candidates": [
            {
                "rank": i + 1,
                "bitstring": row["bitstring"],
                "energy": row["energy"],
                "policy": decode_policy(row["bitstring"], scenario.labels),
            }
            for i, row in enumerate(top)
        ],
    }
