"""Audio mapping for making evolutionary dynamics audible during live runs."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import numpy as np

from src.agents.agent import Agent


@dataclass(frozen=True, slots=True)
class SonificationState:
    """Aggregate population state mapped to sound."""

    dominant_lineage: str
    dominance: float
    mean_generation: float
    trait_diversity: float
    baseline_distance: float


def summarize_for_sound(agents: list[Agent], trait_diversity: float, baseline_distance: float = 0.0) -> SonificationState:
    """Compute compact lineage and generation information for sound synthesis."""

    if not agents:
        return SonificationState("", 0.0, 0.0, trait_diversity, baseline_distance)
    lineage_counts = Counter(agent.lineage_id for agent in agents)
    dominant_lineage, count = lineage_counts.most_common(1)[0]
    mean_generation = sum(agent.generation for agent in agents) / len(agents)
    return SonificationState(
        dominant_lineage=dominant_lineage,
        dominance=count / max(1, len(agents)),
        mean_generation=mean_generation,
        trait_diversity=trait_diversity,
        baseline_distance=baseline_distance,
    )


def synthesize_tone(
    state: SonificationState,
    sample_rate: int,
    duration_ms: int,
    volume: float,
) -> np.ndarray:
    """Create a short stereo tone representing generation, dominance, and diversity.

    Mapping:
    - Mean generation controls pitch.
    - Dominance controls clarity and volume.
    - Trait diversity adds a second interval; diverse populations sound less settled.
    - Baseline distance bends the pitch upward as the original state is lost.
    """

    duration_s = max(0.03, duration_ms / 1000.0)
    t = np.linspace(0.0, duration_s, int(sample_rate * duration_s), endpoint=False)
    base = 180.0 + min(720.0, state.mean_generation * 18.0) + min(260.0, state.baseline_distance * 90.0)
    diversity_interval = 1.0 + min(0.75, state.trait_diversity)
    dominance_gain = 0.35 + 0.65 * state.dominance
    wave = np.sin(2.0 * np.pi * base * t)
    wave += (1.0 - state.dominance) * 0.55 * np.sin(2.0 * np.pi * base * diversity_interval * t)
    wave += 0.20 * state.trait_diversity * np.sin(2.0 * np.pi * base * 2.01 * t)
    wave += 0.16 * min(1.0, state.baseline_distance) * np.sin(2.0 * np.pi * (base * 0.5) * t)
    envelope = np.minimum(1.0, t / 0.025) * np.minimum(1.0, (duration_s - t) / 0.035)
    mono = wave * envelope * volume * dominance_gain
    mono = np.clip(mono, -1.0, 1.0)
    stereo = np.column_stack([mono, mono])
    return (stereo * np.iinfo(np.int16).max).astype(np.int16)
