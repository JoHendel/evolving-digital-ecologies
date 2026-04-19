"""Genomes combine scalar traits with optional neural controller weights."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.agents.traits import Traits
from src.neuroevolution.network import NeuralGenome


@dataclass(slots=True)
class Genome:
    """Heritable organism state."""

    traits: Traits
    neural: Optional[NeuralGenome] = None

    def has_neural_controller(self) -> bool:
        return self.neural is not None

