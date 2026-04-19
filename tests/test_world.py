from src.core.config import WorldConfig
from src.core.rng import RandomStreams
from src.world.world import World


def test_world_initializes_and_spawns_resources() -> None:
    cfg = WorldConfig()
    cfg.resources.initial_count = 5
    cfg.resources.spawn_rate = 2.0
    cfg.resources.max_count = 10
    world = World(cfg, RandomStreams(3))
    world.initialize()
    assert len(world.resources) == 5
    world.update()
    assert 5 < len(world.resources) <= 10

