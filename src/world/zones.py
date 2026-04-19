"""Environmental zones that alter risk and resource availability."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.core.geometry import Vec2


class ZoneType(str, Enum):
    NEUTRAL = "neutral"
    FERTILE = "fertile"
    POOR = "poor"
    HAZARD = "hazard"


@dataclass(frozen=True, slots=True)
class Zone:
    """Circular environmental zone."""

    center: Vec2
    radius: float
    zone_type: ZoneType

    def contains(self, position: Vec2) -> bool:
        return self.center.distance_to(position) <= self.radius

