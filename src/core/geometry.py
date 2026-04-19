"""Geometry primitives used by the continuous two-dimensional world."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, sin


@dataclass(frozen=True, slots=True)
class Vec2:
    """Immutable two-dimensional vector with small numerical helpers."""

    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def length(self) -> float:
        return hypot(self.x, self.y)

    def distance_to(self, other: "Vec2") -> float:
        return (self - other).length()

    def normalized(self) -> "Vec2":
        norm = self.length()
        if norm <= 1e-12:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / norm, self.y / norm)

    def angle(self) -> float:
        return atan2(self.y, self.x)

    def clipped(self, max_length: float) -> "Vec2":
        norm = self.length()
        if norm <= max_length or norm <= 1e-12:
            return self
        return self.normalized() * max_length


def from_angle(angle: float) -> Vec2:
    """Return a unit vector for an angle in radians."""

    return Vec2(cos(angle), sin(angle))


def clamp(value: float, low: float, high: float) -> float:
    """Clamp a scalar to a closed interval."""

    return max(low, min(high, value))


def wrap_position(position: Vec2, width: float, height: float) -> Vec2:
    """Wrap a position around a toroidal world."""

    return Vec2(position.x % width, position.y % height)


def bound_position(position: Vec2, width: float, height: float) -> Vec2:
    """Constrain a position inside rectangular boundaries."""

    return Vec2(clamp(position.x, 0.0, width), clamp(position.y, 0.0, height))

