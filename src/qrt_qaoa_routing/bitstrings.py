"""
Bitstring utilities for binary policy vectors.
"""
from __future__ import annotations

from itertools import product
from typing import Iterable, List

import numpy as np


def iter_bitstrings(n_bits: int) -> Iterable[str]:
    """Yield all bitstrings of length n_bits in lexical order."""
    for bits in product("01", repeat=n_bits):
        yield "".join(bits)


def bitstring_to_vector(bitstring: str) -> np.ndarray:
    """Convert a bitstring into a numeric vector."""
    return np.asarray([1 if c == "1" else 0 for c in bitstring], dtype=float)


def decode_policy(bitstring: str, labels: List[str]) -> dict:
    """Map a bitstring to named boolean decisions."""
    if len(bitstring) != len(labels):
        raise ValueError("bitstring and labels must have the same length")
    return {label: bool(int(bitstring[i])) for i, label in enumerate(labels)}
