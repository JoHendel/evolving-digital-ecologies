"""Behavior controllers for rule-based, neural, and hybrid organisms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from math import atan2, pi

from src.agents.agent import Agent
from src.behavior.actions import Action
from src.behavior.perception import Perception
from src.core.geometry import clamp
from src.core.rng import RandomStreams
from src.world.world import World


def _angle_delta(target: float, current: float) -> float:
    delta = (target - current + pi) % (2.0 * pi) - pi
    return delta


class BehaviorController(ABC):
    """Interface for policy modules."""

    @abstractmethod
    def decide(self, agent: Agent, perception: Perception, world: World, rng: RandomStreams) -> Action:
        """Choose an action for the current step."""


class HeuristicController(BehaviorController):
    """Ecologically interpretable baseline using local resource and hazard cues."""

    def decide(self, agent: Agent, perception: Perception, world: World, rng: RandomStreams) -> Action:
        traits = agent.genome.traits
        turn_noise = rng.py.uniform(-traits.turning_tendency, traits.turning_tendency) * traits.exploration_tendency
        if perception.nearest_resource_distance < traits.perception_range:
            target_angle = atan2(perception.nearest_resource_vector.y, perception.nearest_resource_vector.x)
            turn = clamp(_angle_delta(target_angle, agent.heading), -traits.turning_tendency, traits.turning_tendency)
        else:
            turn = turn_noise

        if perception.hazard > 0.0 and rng.py.random() < traits.risk_sensitivity:
            turn += pi * 0.25
        crowding = min(1.0, perception.local_agent_count / 8.0)
        if crowding > 0.5 and traits.social_tendency < 0.45:
            turn += rng.py.choice([-1.0, 1.0]) * traits.turning_tendency

        reproduce = agent.energy >= traits.reproduction_threshold and perception.hazard < 0.4
        attack = (
            traits.aggression > 0.72
            and perception.local_agent_count > 0
            and agent.energy < 0.85 * traits.reproduction_threshold
            and rng.py.random() < traits.aggression * 0.06
        )
        thrust = clamp(0.55 + traits.exploration_tendency * 0.45 - perception.hazard * traits.risk_sensitivity * 0.25, 0.15, 1.0)
        return Action(turn=turn, thrust=thrust, reproduce=reproduce, attack=attack, signal=traits.communication_tendency)


class NeuralController(BehaviorController):
    """Controller using evolved neural weights; no gradient learning is used."""

    def decide(self, agent: Agent, perception: Perception, world: World, rng: RandomStreams) -> Action:
        if agent.genome.neural is None:
            return HeuristicController().decide(agent, perception, world, rng)
        out = agent.genome.neural.forward(perception.neural_inputs(agent, world))
        return Action(
            turn=float(out[0]) * agent.genome.traits.turning_tendency,
            thrust=clamp((float(out[1]) + 1.0) / 2.0, 0.05, 1.0),
            reproduce=bool(out[2] > 0.15 and agent.energy >= agent.genome.traits.reproduction_threshold),
            attack=bool(out[3] > 0.55 and agent.genome.traits.aggression > 0.5),
            signal=clamp((float(out[4]) + 1.0) / 2.0, 0.0, 1.0),
        )


def controller_for_mode(mode: str) -> BehaviorController:
    """Create the policy object for a configured behavior mode."""

    if mode in {"neural", "hybrid"}:
        return NeuralController()
    return HeuristicController()

