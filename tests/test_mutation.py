from src.agents.traits import Traits
from src.core.config import MutationConfig, TraitConfig
from src.core.rng import RandomStreams
from src.evolution.mutation import mutate_traits


def test_mutation_respects_trait_bounds() -> None:
    bounds = TraitConfig()
    traits = Traits.random(bounds, RandomStreams(1))
    mutated = mutate_traits(traits, bounds, MutationConfig(rate=1.0, strength=10.0), RandomStreams(2))
    for name, value in mutated.items():
        low, high = getattr(bounds, name)
        assert low <= value <= high

