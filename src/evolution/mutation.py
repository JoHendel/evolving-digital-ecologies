"""Mutation operators for scalar traits and neural genomes."""

from __future__ import annotations

from dataclasses import fields

from src.agents.genome import Genome
from src.agents.traits import Traits
from src.core.config import MutationConfig, TraitConfig
from src.core.geometry import clamp
from src.core.rng import RandomStreams


def mutate_traits(traits: Traits, bounds: TraitConfig, config: MutationConfig, rng: RandomStreams) -> Traits:
    """Mutate traits with bounded Gaussian perturbations."""

    values: dict[str, float] = {}
    major = rng.py.random() < config.major_event_rate
    for f in fields(Traits):
        name = f.name
        value = getattr(traits, name)
        low, high = getattr(bounds, name)
        span = high - low
        if rng.py.random() < config.rate:
            value += rng.py.gauss(0.0, span * config.strength)
        if major and rng.py.random() < 0.35:
            value += rng.py.gauss(0.0, span * config.major_event_strength)
        values[name] = clamp(value, low, high)
    return Traits(**values)


def mutate_genome(genome: Genome, bounds: TraitConfig, config: MutationConfig, rng: RandomStreams) -> Genome:
    """Return a mutated child genome."""

    neural = genome.neural.mutated(config.neural_weight_sigma, rng) if genome.neural is not None else None
    return Genome(traits=mutate_traits(genome.traits, bounds, config, rng), neural=neural)

