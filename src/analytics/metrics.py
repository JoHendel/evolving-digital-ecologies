"""Scientific metrics for emergence, diversity, and population dynamics."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from statistics import mean

import numpy as np

from src.agents.agent import Agent
from src.agents.traits import Traits
from src.world.world import World


@dataclass(slots=True)
class BaselineState:
    """Initial reference state used to quantify drift from the starting point."""

    trait_means: np.ndarray
    trait_scales: np.ndarray
    centroid: np.ndarray
    spatial_spread: float
    trait_diversity: float
    lineages: int
    mean_generation: float


@dataclass(slots=True)
class StepMetrics:
    step: int
    population: int
    resources: int
    births: int
    deaths: int
    mean_energy: float
    mean_age: float
    trait_diversity: float
    clustering_index: float
    resource_efficiency: float
    live_lineages: int
    mean_speed: float
    mean_perception_range: float
    mean_metabolism: float
    mean_aggression: float
    mean_social_tendency: float
    trait_baseline_distance: float
    sound_baseline_distance: float
    visual_baseline_distance: float
    baseline_distance: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def trait_matrix(agents: list[Agent]) -> np.ndarray:
    if not agents:
        return np.empty((0, len(fields(Traits))))
    return np.array([[value for _, value in agent.genome.traits.items()] for agent in agents], dtype=float)


def build_baseline_state(agents: list[Agent]) -> BaselineState:
    """Capture the starting population as the perceptual and evolutionary baseline."""

    living = [agent for agent in agents if agent.alive]
    matrix = trait_matrix(living)
    if matrix.size == 0:
        trait_means = np.zeros(len(fields(Traits)))
        trait_scales = np.ones(len(fields(Traits)))
    else:
        trait_means = np.mean(matrix, axis=0)
        trait_scales = np.maximum(np.std(matrix, axis=0), np.maximum(np.abs(trait_means), 1.0) * 0.05)
    positions = np.array([[agent.position.x, agent.position.y] for agent in living], dtype=float) if living else np.zeros((0, 2))
    centroid = np.mean(positions, axis=0) if len(positions) else np.zeros(2)
    spread = _spatial_spread(positions, centroid)
    return BaselineState(
        trait_means=trait_means,
        trait_scales=trait_scales,
        centroid=centroid,
        spatial_spread=spread,
        trait_diversity=trait_diversity(living),
        lineages=max(1, len({agent.lineage_id for agent in living})),
        mean_generation=float(mean(agent.generation for agent in living)) if living else 0.0,
    )


def trait_diversity(agents: list[Agent]) -> float:
    matrix = trait_matrix(agents)
    if matrix.shape[0] <= 1:
        return 0.0
    normalized = matrix / np.maximum(np.mean(matrix, axis=0), 1e-9)
    return float(np.mean(np.std(normalized, axis=0)))


def clustering_index(agents: list[Agent], radius: float = 45.0) -> float:
    if len(agents) <= 1:
        return 0.0
    counts = []
    for agent in agents:
        nearby = sum(1 for other in agents if other.id != agent.id and agent.position.distance_to(other.position) <= radius)
        counts.append(nearby)
    expected = max(1e-9, (len(agents) - 1) * np.pi * radius * radius)
    return float(mean(counts) / expected)


def baseline_distances(agents: list[Agent], baseline: BaselineState | None) -> tuple[float, float, float, float]:
    """Return trait, sound-proxy, visual-proxy, and combined baseline distance.

    The index operationalizes gradual normalization: values near zero resemble
    the initial population, while larger values mean the current system has
    drifted farther from the original visual, acoustic, and trait baseline.
    """

    living = [agent for agent in agents if agent.alive]
    if baseline is None or not living:
        return 0.0, 0.0, 0.0, 0.0
    matrix = trait_matrix(living)
    current_traits = np.mean(matrix, axis=0)
    trait_distance = float(np.mean(np.abs(current_traits - baseline.trait_means) / baseline.trait_scales))
    current_diversity = trait_diversity(living)
    mean_generation = float(mean(agent.generation for agent in living))
    lineage_counts: dict[str, int] = {}
    for agent in living:
        lineage_counts[agent.lineage_id] = lineage_counts.get(agent.lineage_id, 0) + 1
    dominance = max(lineage_counts.values()) / len(living)
    lineage_loss = 1.0 - (len(lineage_counts) / baseline.lineages)
    sound_distance = abs(mean_generation - baseline.mean_generation) / 12.0
    sound_distance += abs(current_diversity - baseline.trait_diversity)
    sound_distance += max(0.0, dominance - (1.0 / baseline.lineages))
    positions = np.array([[agent.position.x, agent.position.y] for agent in living], dtype=float)
    centroid = np.mean(positions, axis=0)
    spread = _spatial_spread(positions, centroid)
    centroid_distance = float(np.linalg.norm(centroid - baseline.centroid) / 500.0)
    spread_distance = abs(spread - baseline.spatial_spread) / max(1.0, baseline.spatial_spread)
    visual_distance = centroid_distance + spread_distance + max(0.0, lineage_loss)
    combined = float(np.mean([trait_distance, sound_distance, visual_distance]))
    return trait_distance, sound_distance, visual_distance, combined


def _spatial_spread(positions: np.ndarray, centroid: np.ndarray) -> float:
    if len(positions) <= 1:
        return 0.0
    return float(np.mean(np.linalg.norm(positions - centroid, axis=1)))


def summarize_step(
    step: int,
    agents: list[Agent],
    world: World,
    births: int,
    deaths: int,
    consumed_energy: float,
    baseline: BaselineState | None = None,
) -> StepMetrics:
    living = [a for a in agents if a.alive]
    if living:
        trait_means = {name: mean(getattr(a.genome.traits, name) for a in living) for name, _ in living[0].genome.traits.items()}
        mean_energy = mean(a.energy for a in living)
        mean_age = mean(a.age for a in living)
    else:
        trait_means = {
            "speed": 0.0,
            "perception_range": 0.0,
            "metabolism": 0.0,
            "aggression": 0.0,
            "social_tendency": 0.0,
        }
        mean_energy = 0.0
        mean_age = 0.0
    trait_distance, sound_distance, visual_distance, combined_distance = baseline_distances(living, baseline)
    return StepMetrics(
        step=step,
        population=len(living),
        resources=len(world.resources),
        births=births,
        deaths=deaths,
        mean_energy=float(mean_energy),
        mean_age=float(mean_age),
        trait_diversity=trait_diversity(living),
        clustering_index=clustering_index(living),
        resource_efficiency=consumed_energy / max(1, len(living)),
        live_lineages=len({a.lineage_id for a in living}),
        mean_speed=float(trait_means.get("speed", 0.0)),
        mean_perception_range=float(trait_means.get("perception_range", 0.0)),
        mean_metabolism=float(trait_means.get("metabolism", 0.0)),
        mean_aggression=float(trait_means.get("aggression", 0.0)),
        mean_social_tendency=float(trait_means.get("social_tendency", 0.0)),
        trait_baseline_distance=trait_distance,
        sound_baseline_distance=sound_distance,
        visual_baseline_distance=visual_distance,
        baseline_distance=combined_distance,
    )
