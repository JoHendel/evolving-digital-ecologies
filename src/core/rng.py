"""Centralized deterministic random number generation."""

from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np


@dataclass(slots=True)
class RandomStreams:
    """Container for synchronized Python and NumPy random generators."""

    seed: int

    def __post_init__(self) -> None:
        self.py = random.Random(self.seed)
        self.np = np.random.default_rng(self.seed)

    py: random.Random = None  # type: ignore[assignment]
    np: np.random.Generator = None  # type: ignore[assignment]

    def child(self, offset: int) -> "RandomStreams":
        """Create a deterministic child stream for independent run components."""

        return RandomStreams(self.seed + offset * 104_729)

