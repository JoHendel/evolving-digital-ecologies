"""Lineage accounting for evolutionary history reconstruction."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LineageRecord:
    lineage_id: str
    ancestor_id: str
    births: int = 0
    deaths: int = 0
    max_generation: int = 0
    last_seen_step: int = 0


@dataclass(slots=True)
class LineageTracker:
    """Track birth/death counts and persistence of inherited lines."""

    records: dict[str, LineageRecord] = field(default_factory=dict)

    def register_founder(self, agent_id: str, lineage_id: str) -> None:
        self.records[lineage_id] = LineageRecord(lineage_id=lineage_id, ancestor_id=agent_id)

    def birth(self, lineage_id: str, generation: int, step: int) -> None:
        rec = self.records.setdefault(lineage_id, LineageRecord(lineage_id, ancestor_id=lineage_id))
        rec.births += 1
        rec.max_generation = max(rec.max_generation, generation)
        rec.last_seen_step = step

    def death(self, lineage_id: str, step: int) -> None:
        rec = self.records.setdefault(lineage_id, LineageRecord(lineage_id, ancestor_id=lineage_id))
        rec.deaths += 1
        rec.last_seen_step = step

    def live_lineage_count(self, living_lineage_ids: set[str]) -> int:
        return len(living_lineage_ids)

