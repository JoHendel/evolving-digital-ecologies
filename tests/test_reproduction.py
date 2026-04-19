from src.agents.agent import Agent
from src.agents.genome import Genome
from src.agents.traits import Traits
from src.core.config import AgentConfig, MutationConfig, TraitConfig
from src.core.geometry import Vec2
from src.core.rng import RandomStreams
from src.evolution.population import reproduce


def test_reproduction_inherits_lineage_and_costs_energy() -> None:
    traits = Traits.random(TraitConfig(), RandomStreams(10))
    parent = Agent(Genome(traits), Vec2(10.0, 10.0), energy=200.0, heading=0.0, id="agent-parent", lineage_id="lineage-a")
    child = reproduce(parent, AgentConfig(), MutationConfig(rate=0.0), RandomStreams(11))
    assert child.parent_id == parent.id
    assert child.id != parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert parent.energy < 200.0
