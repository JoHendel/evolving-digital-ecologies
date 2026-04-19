"""Main simulation engine integrating world, agents, evolution, and metrics."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from src.agents.agent import Agent
from src.analytics.metrics import BaselineState, StepMetrics, build_baseline_state, summarize_step
from src.behavior.controllers import BehaviorController, controller_for_mode
from src.behavior.perception import perceive
from src.core.config import AppConfig, save_config
from src.core.geometry import Vec2
from src.core.rng import RandomStreams
from src.evolution.lineage import LineageTracker
from src.evolution.population import initialize_population, reproduce
from src.world.world import World


@dataclass(slots=True)
class RunResult:
    """Completed simulation state and sampled metrics."""

    config: AppConfig
    metrics: list[StepMetrics]
    agents: list[Agent]
    output_dir: Path
    extinct: bool


@dataclass(slots=True)
class SimulationEngine:
    """Deterministic artificial-life simulation orchestrator."""

    config: AppConfig
    rng: RandomStreams = field(init=False)
    behavior_rng: RandomStreams = field(init=False)
    reproduction_rng: RandomStreams = field(init=False)
    world: World = field(init=False)
    agents: list[Agent] = field(init=False, default_factory=list)
    controller: BehaviorController = field(init=False)
    lineage_tracker: LineageTracker = field(default_factory=LineageTracker)
    metrics: list[StepMetrics] = field(default_factory=list)
    baseline_state: BaselineState | None = None
    step_index: int = 0

    def __post_init__(self) -> None:
        self.rng = RandomStreams(self.config.simulation.seed)
        self.behavior_rng = self.rng.child(3)
        self.reproduction_rng = self.rng.child(4)
        self.world = World(self.config.world, self.rng.child(1))
        self.controller = controller_for_mode(self.config.behavior.mode)

    def initialize(self) -> None:
        self.world.initialize()
        self.agents = initialize_population(
            self.config.agents,
            self.config.behavior,
            self.config.world.width,
            self.config.world.height,
            self.rng.child(2),
        )
        for agent in self.agents:
            self.lineage_tracker.register_founder(agent.id, agent.lineage_id)
            self.lineage_tracker.birth(agent.lineage_id, agent.generation, 0)
        self.metrics.clear()
        self.baseline_state = build_baseline_state(self.agents)
        self.step_index = 0

    def step(self) -> StepMetrics | None:
        self.step_index += 1
        self.world.update()
        births = 0
        deaths = 0
        consumed_energy = 0.0
        offspring: list[Agent] = []
        living_snapshot = [a for a in self.agents if a.alive]

        for agent in living_snapshot:
            if not agent.alive:
                continue
            perception = perceive(agent, living_snapshot, self.world, self.config.agents.max_age)
            action = self.controller.decide(agent, perception, self.world, self.behavior_rng)
            self._apply_motion(agent, action.turn, action.thrust)
            consumed_energy += self._consume_resources(agent)
            self._apply_interactions(agent, action.attack, living_snapshot)
            self._apply_costs(agent, perception.local_agent_count)
            if action.reproduce and agent.energy >= agent.genome.traits.fertility_cost + 1.0:
                child = reproduce(agent, self.config.agents, self.config.mutation, self.reproduction_rng)
                child.position = self.world.normalize_position(child.position)
                offspring.append(child)
                births += 1
                self.lineage_tracker.birth(child.lineage_id, child.generation, self.step_index)
            self._check_death(agent)
            if not agent.alive:
                deaths += 1
                self.lineage_tracker.death(agent.lineage_id, self.step_index)

        self.agents.extend(offspring)
        self.agents = [agent for agent in self.agents if agent.alive]
        if self.step_index % self.config.simulation.metrics_interval == 0 or deaths or births:
            metric = summarize_step(self.step_index, self.agents, self.world, births, deaths, consumed_energy, self.baseline_state)
            self.metrics.append(metric)
            return metric
        return None

    def run(self, progress_callback: Callable[["SimulationEngine"], None] | None = None) -> RunResult:
        self.initialize()
        for _ in range(self.config.simulation.steps):
            self.step()
            if progress_callback is not None:
                progress_callback(self)
            if self.config.simulation.stop_on_extinction and not self.agents:
                break
        return self.finish()

    def finish(self) -> RunResult:
        """Finalize a run and write the exact configuration snapshot."""

        output_dir = self.output_directory()
        output_dir.mkdir(parents=True, exist_ok=True)
        save_config(self.config, output_dir / "config_snapshot.yaml")
        return RunResult(self.config, self.metrics, self.agents, output_dir, extinct=not self.agents)

    def output_directory(self) -> Path:
        return Path(self.config.simulation.output_dir) / self.config.simulation.run_name

    def _apply_motion(self, agent: Agent, turn: float, thrust: float) -> None:
        traits = agent.genome.traits
        agent.heading += turn
        displacement = agent.velocity_direction * (traits.speed * thrust * self.config.simulation.dt)
        agent.position = self.world.normalize_position(agent.position + displacement)

    def _consume_resources(self, agent: Agent) -> float:
        for resource in list(self.world.resources):
            if agent.position.distance_to(resource.position) <= resource.radius + 2.0:
                agent.energy += resource.energy
                self.world.consume_resource(resource)
                return resource.energy
        return 0.0

    def _apply_interactions(self, agent: Agent, attack: bool, agents: list[Agent]) -> None:
        if not attack:
            return
        radius = self.config.agents.interaction_radius
        candidates = [
            other for other in agents
            if other.id != agent.id and other.alive and agent.position.distance_to(other.position) <= radius
        ]
        if not candidates:
            return
        victim = min(candidates, key=lambda other: other.energy)
        victim.health -= self.config.agents.attack_damage / 100.0
        victim.energy -= self.config.agents.attack_damage
        agent.energy += self.config.agents.attack_energy_gain

    def _apply_costs(self, agent: Agent, local_agent_count: int) -> None:
        traits = agent.genome.traits
        movement_cost = traits.metabolism + 0.015 * traits.speed + 0.002 * traits.perception_range
        crowding_cost = max(0, local_agent_count - 2) * self.config.agents.crowding_cost
        hazard_cost = self.world.hazard_damage_at(agent.position) * (1.2 - 0.5 * traits.risk_sensitivity)
        agent.energy -= (movement_cost + crowding_cost + hazard_cost) * self.config.simulation.dt
        agent.health -= max(0.0, hazard_cost) * 0.002
        agent.age += 1

    def _check_death(self, agent: Agent) -> None:
        if agent.energy <= 0.0:
            agent.mark_dead("energy_depletion")
        elif agent.age >= self.config.agents.max_age:
            agent.mark_dead("senescence")
        elif agent.health <= 0.0:
            agent.mark_dead("health_failure")


def run_simulation(config: AppConfig) -> RunResult:
    """Convenience entry point for scripts and tests."""

    return SimulationEngine(config).run()
