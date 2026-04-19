from src.agents.agent import Agent
from src.agents.genome import Genome
from src.agents.traits import Traits
from src.analytics.metrics import summarize_step, trait_diversity
from src.core.config import TraitConfig, WorldConfig
from src.core.geometry import Vec2
from src.core.rng import RandomStreams
from src.world.world import World


def test_metrics_handle_empty_and_nonempty_populations() -> None:
    world = World(WorldConfig(), RandomStreams(4))
    world.initialize()
    empty = summarize_step(0, [], world, births=0, deaths=0, consumed_energy=0.0)
    assert empty.population == 0
    traits = Traits.random(TraitConfig(), RandomStreams(5))
    agents = [Agent(Genome(traits), Vec2(1.0, 1.0), 50.0, 0.0)]
    metric = summarize_step(1, agents, world, births=1, deaths=0, consumed_energy=10.0)
    assert metric.population == 1
    assert trait_diversity(agents) == 0.0

