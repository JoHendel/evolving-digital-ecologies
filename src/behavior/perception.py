"""Local sensory features made available to controllers."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin

import numpy as np

from src.agents.agent import Agent
from src.core.geometry import Vec2
from src.world.world import World


@dataclass(frozen=True, slots=True)
class Perception:
    """Compact description of local environment and internal state."""

    nearest_resource_vector: Vec2
    nearest_resource_distance: float
    local_agent_count: int
    mean_neighbor_energy: float
    hazard: float
    energy_ratio: float
    age_ratio: float

    def neural_inputs(self, agent: Agent, world: World) -> np.ndarray:
        traits = agent.genome.traits
        max_dist = max(1.0, traits.perception_range)
        return np.array(
            [
                self.nearest_resource_vector.x / max_dist,
                self.nearest_resource_vector.y / max_dist,
                self.nearest_resource_distance / max_dist,
                min(1.0, self.local_agent_count / 12.0),
                self.mean_neighbor_energy / max(1.0, traits.reproduction_threshold),
                self.hazard,
                self.energy_ratio,
                self.age_ratio,
                cos(agent.heading),
                sin(agent.heading),
            ],
            dtype=float,
        )


def perceive(agent: Agent, agents: list[Agent], world: World, max_age: int) -> Perception:
    """Build local sensory features for a single agent."""

    traits = agent.genome.traits
    nearest = world.nearest_resource(agent.position, traits.perception_range)
    if nearest is None:
        resource_vec = Vec2(0.0, 0.0)
        resource_dist = traits.perception_range
    else:
        resource_vec = nearest.position - agent.position
        resource_dist = resource_vec.length()

    neighbor_energies = [
        other.energy
        for other in agents
        if other.id != agent.id and other.alive and agent.position.distance_to(other.position) <= traits.perception_range
    ]
    mean_neighbor_energy = sum(neighbor_energies) / len(neighbor_energies) if neighbor_energies else 0.0
    hazard = min(1.0, world.hazard_damage_at(agent.position))
    return Perception(
        nearest_resource_vector=resource_vec,
        nearest_resource_distance=resource_dist,
        local_agent_count=len(neighbor_energies),
        mean_neighbor_energy=mean_neighbor_energy,
        hazard=hazard,
        energy_ratio=agent.energy / max(1.0, traits.reproduction_threshold),
        age_ratio=agent.age / max(1, max_age),
    )

