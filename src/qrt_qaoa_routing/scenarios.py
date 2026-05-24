"""
Scenario definitions for compact ISRU resource-routing examples.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

import numpy as np


EnergyFunction = Callable[[np.ndarray], float]


@dataclass(frozen=True)
class Scenario:
    """A binary routing scenario with labels and an energy function."""
    name: str
    labels: List[str]
    description: str
    energy: EnergyFunction

    @property
    def n_bits(self) -> int:
        return len(self.labels)


def water_recovery() -> Scenario:
    labels = ["inlet", "pretreat", "splitter", "water_store", "oxygen_step", "recycle"]
    power = np.array([0.10, 0.12, 0.30, 0.10, 0.40, 0.12])

    def energy(x: np.ndarray) -> float:
        reward = 1.0 * x[3] + 1.0 * x[4] + 0.5 * x[5]
        power_penalty = (float(power @ x) - 0.90) ** 2
        flow_penalty = (x[0] - (x[2] + x[3])) ** 2
        oxygen_gate = x[4] * (1 - x[2])
        recycle_gate = (x[4] - x[5]) ** 2
        throughput = x[2] + x[3] + x[5]
        minimum_throughput = max(0.0, 1.0 - float(throughput)) ** 2
        return (
            -reward
            + 5.0 * power_penalty
            + 10.0 * flow_penalty
            + 8.0 * oxygen_gate
            + 2.0 * recycle_gate
            + 4.0 * minimum_throughput
        )

    return Scenario(
        name="water_recovery",
        labels=labels,
        description="Water and oxygen routing policy with power and flow-balance constraints.",
        energy=energy,
    )


def thermal_regulation(storm: float = 1.2, power_budget: float = 0.70) -> Scenario:
    labels = ["link_ab", "link_bc", "link_cd", "pcm_a", "pcm_b", "radiator"]
    power = np.array([0.15, 0.15, 0.15, 0.05, 0.05, 0.20])
    benefit = np.array([0.50, 0.50, 0.50, 0.40, 0.30, 0.60])

    def energy(x: np.ndarray) -> float:
        base_load = 1.0 + storm
        delivered = float(benefit @ x)
        unmet_load = max(0.0, base_load - delivered) ** 2
        power_penalty = (float(power @ x) - power_budget) ** 2
        path_active = min(1.0, float(x[0] + x[1] + x[2] + x[3] + x[4]))
        radiator_without_path = x[5] * (1 - path_active)
        return unmet_load + 3.0 * power_penalty + 1.5 * radiator_without_path

    return Scenario(
        name="thermal_regulation",
        labels=labels,
        description="Thermal routing policy balancing load reduction against power budget.",
        energy=energy,
    )


def acid_regolith() -> Scenario:
    labels = ["acid_a", "acid_b", "circulation", "valve", "radiator", "saver", "filter", "product"]
    power = np.array([0.16, 0.16, 0.22, 0.06, 0.18, 0.04, 0.10, 0.28])

    def energy(x: np.ndarray) -> float:
        yield_gain = 1.05 * x[0] + 1.00 * x[1] + 0.65 * x[7]
        circulation_support = 0.55 * x[2] + 0.35 * x[3]
        separation_support = 0.40 * x[6]
        energy_cost = 0.55 * float(power @ x)
        corrosion_penalty = 0.90 * x[4]
        acid_loss_penalty = 0.60 * x[5]
        product_gate = x[7] * (1 - x[6])
        process_gate = max(0.0, 1.0 - float(x[2] + x[3])) ** 2
        acid_gate = max(0.0, 1.0 - float(x[0] + x[1])) ** 2
        return (
            -(yield_gain + circulation_support + separation_support)
            + energy_cost
            + corrosion_penalty
            + acid_loss_penalty
            + 3.0 * product_gate
            + 2.0 * process_gate
            + 2.0 * acid_gate
        )

    return Scenario(
        name="acid_regolith",
        labels=labels,
        description="Acid-regolith processing policy with yield, corrosion, acid-loss, and product-step tradeoffs.",
        energy=energy,
    )


def list_scenarios() -> List[str]:
    return ["water_recovery", "thermal_regulation", "acid_regolith"]


def get_scenario(name: str) -> Scenario:
    scenarios: Dict[str, Scenario] = {
        "water_recovery": water_recovery(),
        "thermal_regulation": thermal_regulation(),
        "acid_regolith": acid_regolith(),
    }
    if name not in scenarios:
        raise KeyError(f"Unknown scenario: {name}. Available: {', '.join(sorted(scenarios))}")
    return scenarios[name]
