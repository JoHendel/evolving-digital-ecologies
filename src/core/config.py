"""Configuration schema and loading utilities.

The dataclasses intentionally mirror the YAML structure so experiment files are
easy to read, diff, and modify in PyCharm.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, TypeVar, get_args, get_origin, get_type_hints

import yaml


T = TypeVar("T")


@dataclass(slots=True)
class ResourceConfig:
    initial_count: int = 250
    spawn_rate: float = 2.5
    max_count: int = 600
    energy_min: float = 8.0
    energy_max: float = 28.0
    radius: float = 2.3


@dataclass(slots=True)
class ZoneConfig:
    enabled: bool = True
    hazard_damage: float = 0.35
    fertile_spawn_multiplier: float = 2.0
    poor_spawn_multiplier: float = 0.35
    climate_period: int = 1500


@dataclass(slots=True)
class WorldConfig:
    width: float = 900.0
    height: float = 650.0
    toroidal: bool = True
    resources: ResourceConfig = field(default_factory=ResourceConfig)
    zones: ZoneConfig = field(default_factory=ZoneConfig)


@dataclass(slots=True)
class TraitConfig:
    speed: tuple[float, float] = (0.8, 3.2)
    perception_range: tuple[float, float] = (25.0, 110.0)
    turning_tendency: tuple[float, float] = (0.05, 0.8)
    metabolism: tuple[float, float] = (0.05, 0.35)
    reproduction_threshold: tuple[float, float] = (55.0, 130.0)
    fertility_cost: tuple[float, float] = (18.0, 55.0)
    aggression: tuple[float, float] = (0.0, 1.0)
    social_tendency: tuple[float, float] = (0.0, 1.0)
    exploration_tendency: tuple[float, float] = (0.0, 1.0)
    risk_sensitivity: tuple[float, float] = (0.0, 1.0)
    communication_tendency: tuple[float, float] = (0.0, 1.0)


@dataclass(slots=True)
class MutationConfig:
    rate: float = 0.08
    strength: float = 0.12
    major_event_rate: float = 0.01
    major_event_strength: float = 0.35
    neural_weight_sigma: float = 0.08


@dataclass(slots=True)
class AgentConfig:
    initial_population: int = 80
    initial_energy: float = 75.0
    max_age: int = 2800
    crowding_radius: float = 9.0
    crowding_cost: float = 0.015
    interaction_radius: float = 8.0
    attack_energy_gain: float = 3.0
    attack_damage: float = 2.5
    trait_bounds: TraitConfig = field(default_factory=TraitConfig)


@dataclass(slots=True)
class BehaviorConfig:
    mode: str = "heuristic"
    neural_hidden_size: int = 10
    hybrid_neural_fraction: float = 0.0


@dataclass(slots=True)
class SimulationConfig:
    steps: int = 5000
    seed: int = 42
    dt: float = 1.0
    metrics_interval: int = 10
    output_dir: str = "data/runs"
    run_name: str = "baseline"
    stop_on_extinction: bool = True


@dataclass(slots=True)
class VisualizationConfig:
    enabled: bool = False
    width: int = 1100
    height: int = 800
    fps: int = 60
    draw_perception: bool = False
    audio_enabled: bool = False
    audio_interval_steps: int = 30
    audio_duration_ms: int = 140
    audio_volume: float = 0.22


@dataclass(slots=True)
class ExperimentConfig:
    name: str = "mutation_sweep"
    base_config: str = "configs/default.yaml"
    repeats: int = 3
    sweep: dict[str, list[Any]] = field(default_factory=dict)


@dataclass(slots=True)
class AppConfig:
    world: WorldConfig = field(default_factory=WorldConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    behavior: BehaviorConfig = field(default_factory=BehaviorConfig)
    mutation: MutationConfig = field(default_factory=MutationConfig)
    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)


def _coerce_dataclass(cls: type[T], data: dict[str, Any]) -> T:
    kwargs: dict[str, Any] = {}
    hints = get_type_hints(cls)
    for f in fields(cls):
        if f.name in data:
            raw = data[f.name]
        elif callable(f.default_factory):
            raw = f.default_factory()
        else:
            raw = f.default
        field_type = hints.get(f.name, f.type)
        origin = get_origin(field_type)
        if isinstance(raw, dict) and isinstance(field_type, type) and is_dataclass(field_type):
            kwargs[f.name] = _coerce_dataclass(field_type, raw)
        elif origin is tuple and isinstance(raw, list):
            kwargs[f.name] = tuple(raw)
        elif origin is dict:
            kwargs[f.name] = dict(raw)
        elif origin is list:
            kwargs[f.name] = list(raw)
        elif get_args(field_type) and isinstance(raw, list):
            kwargs[f.name] = tuple(raw)
        else:
            kwargs[f.name] = raw
    return cls(**kwargs)


def load_config(path: str | Path) -> AppConfig:
    """Load an application configuration from YAML."""

    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return _coerce_dataclass(AppConfig, data)


def save_config(config: AppConfig, path: str | Path) -> None:
    """Write a configuration snapshot to YAML."""

    with Path(path).open("w", encoding="utf-8") as fh:
        yaml.safe_dump(asdict(config), fh, sort_keys=False)


def set_nested(config: AppConfig, dotted_key: str, value: Any) -> AppConfig:
    """Set a dotted configuration value in-place and return the config."""

    target: Any = config
    parts = dotted_key.split(".")
    for part in parts[:-1]:
        target = getattr(target, part)
    setattr(target, parts[-1], value)
    return config


def config_to_dict(config: AppConfig) -> dict[str, Any]:
    """Convert config dataclasses to plain dictionaries for exports."""

    return asdict(config)
