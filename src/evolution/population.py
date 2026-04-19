"""Population initialization and reproduction helpers."""

from __future__ import annotations

from math import pi

from src.agents.agent import Agent
from src.agents.genome import Genome
from src.agents.traits import Traits
from src.core.config import AgentConfig, BehaviorConfig, MutationConfig
from src.core.geometry import Vec2
from src.core.rng import RandomStreams
from src.evolution.mutation import mutate_genome
from src.neuroevolution.network import NeuralGenome


NEURAL_INPUTS = 10
NEURAL_OUTPUTS = 5


def random_genome(agent_cfg: AgentConfig, behavior_cfg: BehaviorConfig, rng: RandomStreams) -> Genome:
    traits = Traits.random(agent_cfg.trait_bounds, rng)
    neural = None
    if behavior_cfg.mode == "neural" or (behavior_cfg.mode == "hybrid" and rng.py.random() < behavior_cfg.hybrid_neural_fraction):
        neural = NeuralGenome.random(NEURAL_INPUTS, behavior_cfg.neural_hidden_size, NEURAL_OUTPUTS, rng)
    return Genome(traits=traits, neural=neural)


def initialize_population(agent_cfg: AgentConfig, behavior_cfg: BehaviorConfig, width: float, height: float, rng: RandomStreams) -> list[Agent]:
    return [
        Agent.random(random_genome(agent_cfg, behavior_cfg, rng), agent_cfg.initial_energy, width, height, rng)
        for _ in range(agent_cfg.initial_population)
    ]


def reproduce(parent: Agent, agent_cfg: AgentConfig, mutation_cfg: MutationConfig, rng: RandomStreams) -> Agent:
    """Produce an offspring with inherited bounded traits and a mutated neural genome."""

    child_genome = mutate_genome(parent.genome, agent_cfg.trait_bounds, mutation_cfg, rng)
    jitter = Vec2(rng.py.uniform(-4.0, 4.0), rng.py.uniform(-4.0, 4.0))
    child = Agent(
        genome=child_genome,
        position=parent.position + jitter,
        energy=max(1.0, parent.genome.traits.fertility_cost * 0.55),
        heading=parent.heading + rng.py.uniform(-pi, pi),
        id=f"agent-{rng.py.getrandbits(96):024x}",
        parent_id=parent.id,
        lineage_id=parent.lineage_id,
        generation=parent.generation + 1,
    )
    parent.energy -= parent.genome.traits.fertility_cost
    parent.births += 1
    return child
