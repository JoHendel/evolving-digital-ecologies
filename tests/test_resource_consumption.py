from src.agents.agent import Agent
from src.agents.genome import Genome
from src.agents.traits import Traits
from src.core.config import AppConfig, TraitConfig
from src.core.geometry import Vec2
from src.core.rng import RandomStreams
from src.simulation.engine import SimulationEngine
from src.world.resources import Resource


def test_agent_consumes_resource_and_gains_energy() -> None:
    cfg = AppConfig()
    engine = SimulationEngine(cfg)
    engine.initialize()
    traits = Traits.random(TraitConfig(), RandomStreams(9))
    agent = Agent(Genome(traits), Vec2(20.0, 20.0), 10.0, 0.0)
    engine.world.resources = [Resource(Vec2(20.0, 20.0), 12.0, 3.0)]
    gained = engine._consume_resources(agent)
    assert gained == 12.0
    assert agent.energy == 22.0
    assert not engine.world.resources

