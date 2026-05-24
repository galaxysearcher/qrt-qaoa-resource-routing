"""
Energy-landscape construction for binary routing scenarios.
"""
from __future__ import annotations

from typing import List

import numpy as np

from .bitstrings import bitstring_to_vector, iter_bitstrings
from .scenarios import Scenario


def energy_table(scenario: Scenario) -> List[dict]:
    """Enumerate all bitstrings and evaluate their energy."""
    rows = []
    for bitstring in iter_bitstrings(scenario.n_bits):
        x = bitstring_to_vector(bitstring)
        rows.append({"bitstring": bitstring, "energy": float(scenario.energy(x))})
    rows.sort(key=lambda row: row["energy"])
    return rows


def diagonal_energy(scenario: Scenario) -> np.ndarray:
    """Return the diagonal energy vector ordered by integer bitstring index."""
    dim = 2 ** scenario.n_bits
    diag = np.zeros(dim, dtype=float)
    for bitstring in iter_bitstrings(scenario.n_bits):
        diag[int(bitstring, 2)] = float(scenario.energy(bitstring_to_vector(bitstring)))
    return diag
