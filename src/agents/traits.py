"""Heritable phenotypic trait representation."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Iterator

from src.core.config import TraitConfig
from src.core.geometry import clamp
from src.core.rng import RandomStreams


@dataclass(slots=True)
class Traits:
    """Continuous traits exposed to mutation, selection, and analysis."""

    speed: float
    perception_range: float
    turning_tendency: float
    metabolism: float
    reproduction_threshold: float
    fertility_cost: float
    aggression: float
    social_tendency: float
    exploration_tendency: float
    risk_sensitivity: float
    communication_tendency: float

    @classmethod
    def random(cls, bounds: TraitConfig, rng: RandomStreams) -> "Traits":
        values = {
            f.name: rng.py.uniform(*getattr(bounds, f.name))
            for f in fields(cls)
        }
        return cls(**values)

    def items(self) -> Iterator[tuple[str, float]]:
        for f in fields(self):
            yield f.name, getattr(self, f.name)

    def clipped(self, bounds: TraitConfig) -> "Traits":
        values = {
            name: clamp(value, *getattr(bounds, name))
            for name, value in self.items()
        }
        return Traits(**values)

