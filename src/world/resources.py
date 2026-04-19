"""Resource entities consumed by agents."""

from __future__ import annotations

from dataclasses import dataclass

from src.core.geometry import Vec2


@dataclass(slots=True)
class Resource:
    """Localized energy packet in the environment."""

    position: Vec2
    energy: float
    radius: float
    id: str = ""
