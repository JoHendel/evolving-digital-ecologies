"""Digital organism implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import pi
from typing import Optional

from src.agents.genome import Genome
from src.core.geometry import Vec2, from_angle
from src.core.rng import RandomStreams


class LifeState(str, Enum):
    ALIVE = "alive"
    DEAD = "dead"


@dataclass(slots=True)
class Agent:
    """Autonomous organism situated in the continuous world."""

    genome: Genome
    position: Vec2
    energy: float
    heading: float
    id: str = ""
    parent_id: Optional[str] = None
    lineage_id: str = ""
    age: int = 0
    health: float = 1.0
    births: int = 0
    generation: int = 0
    state: LifeState = LifeState.ALIVE
    cause_of_death: Optional[str] = None

    @classmethod
    def random(cls, genome: Genome, energy: float, world_width: float, world_height: float, rng: RandomStreams) -> "Agent":
        agent_id = f"agent-{rng.py.getrandbits(96):024x}"
        return cls(
            genome=genome,
            position=Vec2(rng.py.uniform(0.0, world_width), rng.py.uniform(0.0, world_height)),
            energy=energy,
            heading=rng.py.uniform(-pi, pi),
            id=agent_id,
            lineage_id=f"lineage-{agent_id}",
        )

    @property
    def alive(self) -> bool:
        return self.state == LifeState.ALIVE

    @property
    def velocity_direction(self) -> Vec2:
        return from_angle(self.heading)

    def mark_dead(self, cause: str) -> None:
        self.state = LifeState.DEAD
        self.cause_of_death = cause
