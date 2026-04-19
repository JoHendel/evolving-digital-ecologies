"""Generate a static README preview of the live simulation view."""

from __future__ import annotations

import os
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from src.core.config import load_config
from src.simulation.engine import SimulationEngine
from src.visualization.live import _draw_dashboard, _draw_zones, _lineage_color
from src.visualization.sonification import summarize_for_sound


def generate_preview(
    config_path: str = "configs/long_live_analysis.yaml",
    output_path: str = "media/live_preview.png",
    steps: int = 260,
) -> Path:
    """Render a deterministic live-view snapshot without opening a window."""

    config = load_config(config_path)
    config.visualization.audio_enabled = False
    engine = SimulationEngine(config)
    engine.initialize()

    cfg = config.visualization
    scale_x = cfg.width / config.world.width
    scale_y = cfg.height / config.world.height
    history: deque[tuple[int, int, float, float]] = deque(maxlen=260)

    for _ in range(min(steps, config.simulation.steps)):
        metric = engine.step()
        if metric is not None:
            history.append((metric.population, metric.resources, metric.trait_diversity, metric.baseline_distance))
        if not engine.agents:
            break

    pygame.init()
    font = pygame.font.SysFont("consolas", 16)
    screen = pygame.Surface((cfg.width, cfg.height))
    screen.fill((18, 20, 24))

    _draw_zones(screen, engine, scale_x, scale_y)
    for resource in engine.world.resources:
        pygame.draw.circle(
            screen,
            (85, 190, 105),
            (int(resource.position.x * scale_x), int(resource.position.y * scale_y)),
            3,
        )

    lineage_counts = Counter(agent.lineage_id for agent in engine.agents)
    dominant_lineage = lineage_counts.most_common(1)[0][0] if lineage_counts else ""
    for agent in engine.agents:
        color = _lineage_color(agent.lineage_id)
        radius = 5 if agent.lineage_id == dominant_lineage else 4
        position = (int(agent.position.x * scale_x), int(agent.position.y * scale_y))
        pygame.draw.circle(screen, color, position, radius)
        if agent.lineage_id == dominant_lineage:
            pygame.draw.circle(screen, (245, 245, 210), position, radius + 2, width=1)

    latest_diversity = history[-1][2] if history else 0.0
    latest_baseline_distance = history[-1][3] if history else 0.0
    sound_state = summarize_for_sound(engine.agents, latest_diversity, latest_baseline_distance)
    _draw_dashboard(screen, font, engine, history, sound_state, audio_ready=False)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(screen, output)
    pygame.quit()
    return output


if __name__ == "__main__":
    path = generate_preview()
    print(path)
