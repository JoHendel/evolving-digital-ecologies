"""Continuous 2D world with resources, zones, hazards, and climate cycles."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import sin, tau

from src.core.config import WorldConfig
from src.core.geometry import Vec2, bound_position, wrap_position
from src.core.rng import RandomStreams
from src.world.resources import Resource
from src.world.zones import Zone, ZoneType


@dataclass(slots=True)
class World:
    """Stateful simulation environment."""

    config: WorldConfig
    rng: RandomStreams
    resources: list[Resource] = field(default_factory=list)
    zones: list[Zone] = field(default_factory=list)
    step_index: int = 0
    climate_factor: float = 1.0

    def initialize(self) -> None:
        self.resources.clear()
        self.zones = self._default_zones() if self.config.zones.enabled else []
        for _ in range(self.config.resources.initial_count):
            self.resources.append(self.spawn_resource())

    def _default_zones(self) -> list[Zone]:
        w, h = self.config.width, self.config.height
        return [
            Zone(Vec2(0.24 * w, 0.35 * h), 0.20 * min(w, h), ZoneType.FERTILE),
            Zone(Vec2(0.73 * w, 0.55 * h), 0.24 * min(w, h), ZoneType.POOR),
            Zone(Vec2(0.55 * w, 0.23 * h), 0.14 * min(w, h), ZoneType.HAZARD),
        ]

    def update(self) -> None:
        self.step_index += 1
        period = max(1, self.config.zones.climate_period)
        self.climate_factor = 1.0 + 0.35 * sin(tau * self.step_index / period)
        expected = self.config.resources.spawn_rate * self.climate_factor
        spawn_count = int(expected)
        if self.rng.py.random() < expected - spawn_count:
            spawn_count += 1
        capacity = max(0, self.config.resources.max_count - len(self.resources))
        for _ in range(min(spawn_count, capacity)):
            self.resources.append(self.spawn_resource())

    def spawn_resource(self) -> Resource:
        position = self._biased_resource_position()
        cfg = self.config.resources
        return Resource(
            position=position,
            energy=self.rng.py.uniform(cfg.energy_min, cfg.energy_max),
            radius=cfg.radius,
            id=f"resource-{self.rng.py.getrandbits(96):024x}",
        )

    def _biased_resource_position(self) -> Vec2:
        for _ in range(16):
            p = Vec2(self.rng.py.uniform(0.0, self.config.width), self.rng.py.uniform(0.0, self.config.height))
            multiplier = self.resource_multiplier_at(p)
            if self.rng.py.random() < min(1.0, 0.35 * multiplier):
                return p
        return Vec2(self.rng.py.uniform(0.0, self.config.width), self.rng.py.uniform(0.0, self.config.height))

    def resource_multiplier_at(self, position: Vec2) -> float:
        multiplier = 1.0
        for zone in self.zones:
            if zone.contains(position):
                if zone.zone_type == ZoneType.FERTILE:
                    multiplier *= self.config.zones.fertile_spawn_multiplier
                elif zone.zone_type == ZoneType.POOR:
                    multiplier *= self.config.zones.poor_spawn_multiplier
                elif zone.zone_type == ZoneType.HAZARD:
                    multiplier *= 0.2
        return multiplier

    def hazard_damage_at(self, position: Vec2) -> float:
        return sum(
            self.config.zones.hazard_damage
            for zone in self.zones
            if zone.zone_type == ZoneType.HAZARD and zone.contains(position)
        )

    def normalize_position(self, position: Vec2) -> Vec2:
        if self.config.toroidal:
            return wrap_position(position, self.config.width, self.config.height)
        return bound_position(position, self.config.width, self.config.height)

    def nearest_resource(self, position: Vec2, radius: float) -> Resource | None:
        best: Resource | None = None
        best_dist = radius
        for resource in self.resources:
            dist = position.distance_to(resource.position)
            if dist <= best_dist:
                best = resource
                best_dist = dist
        return best

    def consume_resource(self, resource: Resource) -> None:
        self.resources = [r for r in self.resources if r.id != resource.id]
