from src.core.config import AppConfig
from src.simulation.engine import run_simulation


def small_config(seed: int) -> AppConfig:
    cfg = AppConfig()
    cfg.simulation.seed = seed
    cfg.simulation.steps = 80
    cfg.simulation.metrics_interval = 5
    cfg.agents.initial_population = 15
    cfg.world.resources.initial_count = 40
    cfg.world.resources.spawn_rate = 0.8
    cfg.world.resources.max_count = 80
    cfg.simulation.run_name = f"test_seed_{seed}"
    return cfg


def test_seeded_runs_are_reproducible() -> None:
    first = run_simulation(small_config(77)).metrics
    second = run_simulation(small_config(77)).metrics
    assert [m.to_dict() for m in first] == [m.to_dict() for m in second]


def test_generated_agent_ids_are_unique() -> None:
    result = run_simulation(small_config(88))
    ids = [agent.id for agent in result.agents]
    assert len(ids) == len(set(ids))
