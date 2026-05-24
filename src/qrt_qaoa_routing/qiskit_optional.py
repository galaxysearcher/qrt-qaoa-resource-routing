"""
Optional Qiskit diagonal-ansatz runner.

The exact enumeration solver is the default validation baseline. This module provides
a local simulator path when Qiskit and qiskit-aer are installed.
"""
from __future__ import annotations

import math
from typing import Dict

import numpy as np

from .energy import diagonal_energy
from .scenarios import Scenario


def run_diagonal_qaoa_sweep(scenario: Scenario, grid: int = 7, shots: int = 1024) -> Dict:
    """Run a small Qiskit diagonal-ansatz sweep for one scenario."""
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit.library import Diagonal
        from qiskit_aer.primitives import Sampler
    except Exception as exc:
        raise RuntimeError("Qiskit optional dependencies are not installed") from exc

    energy = diagonal_energy(scenario)
    n_bits = scenario.n_bits
    gammas = np.linspace(0.0, 2 * math.pi, grid)
    betas = np.linspace(0.0, math.pi, grid)
    sampler = Sampler()

    best = {"expected_energy": float("inf"), "gamma": None, "beta": None, "counts": None}

    for gamma in gammas:
        phases = np.exp(-1j * gamma * energy)
        for beta in betas:
            qc = QuantumCircuit(n_bits)
            qc.h(range(n_bits))
            qc.append(Diagonal(phases), range(n_bits))
            for q in range(n_bits):
                qc.rx(2 * beta, q)
            qc.measure_all()

            result = sampler.run([qc], shots=shots).result()
            if hasattr(result, "quasi_dists"):
                dist = result.quasi_dists[0]
                counts = {format(k, f"0{n_bits}b"): int(v * shots) for k, v in dist.items()}
            else:
                counts = result[0].data.meas.get_counts()

            total = max(1, sum(counts.values()))
            expected = 0.0
            for bitstring, count in counts.items():
                expected += (count / total) * float(energy[int(bitstring, 2)])

            if expected < best["expected_energy"]:
                best = {
                    "expected_energy": float(expected),
                    "gamma": float(gamma),
                    "beta": float(beta),
                    "counts": counts,
                }

    return {
        "scenario": scenario.name,
        "bit_labels": scenario.labels,
        "grid": grid,
        "shots": shots,
        "best": best,
    }
