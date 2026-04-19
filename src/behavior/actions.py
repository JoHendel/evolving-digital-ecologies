"""Action schema returned by behavior controllers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Action:
    """Low-level motor and interaction command for one simulation step."""

    turn: float = 0.0
    thrust: float = 1.0
    reproduce: bool = False
    attack: bool = False
    signal: float = 0.0

