"""Pygame live visualization for inspecting spatial dynamics."""

from __future__ import annotations

from collections import deque
from collections import Counter
from hashlib import blake2b

from src.simulation.engine import RunResult, SimulationEngine
from src.visualization.sonification import summarize_for_sound, synthesize_tone
from src.world.zones import ZoneType


def run_live(engine: SimulationEngine) -> RunResult:
    """Run a live visual simulation window and return exportable run state."""

    import pygame

    cfg = engine.config.visualization
    audio_ready = _initialize_audio(pygame, cfg.audio_enabled)
    pygame.init()
    font = pygame.font.SysFont("consolas", 16)
    screen = pygame.display.set_mode((cfg.width, cfg.height))
    clock = pygame.time.Clock()
    engine.initialize()
    scale_x = cfg.width / engine.config.world.width
    scale_y = cfg.height / engine.config.world.height
    history: deque[tuple[int, int, float, float]] = deque(maxlen=260)
    running = True
    while running and engine.step_index < engine.config.simulation.steps and engine.agents:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        metric = engine.step()
        if metric is not None:
            history.append((metric.population, metric.resources, metric.trait_diversity, metric.baseline_distance))
        latest_diversity = history[-1][2] if history else 0.0
        latest_baseline_distance = history[-1][3] if history else 0.0
        sound_state = summarize_for_sound(engine.agents, latest_diversity, latest_baseline_distance)
        if audio_ready and engine.step_index % max(1, cfg.audio_interval_steps) == 0:
            _play_sound(pygame, sound_state, cfg.audio_duration_ms, cfg.audio_volume)
        screen.fill((18, 20, 24))
        _draw_zones(screen, engine, scale_x, scale_y)
        for resource in engine.world.resources:
            pygame.draw.circle(screen, (85, 190, 105), (int(resource.position.x * scale_x), int(resource.position.y * scale_y)), 3)
        lineage_counts = Counter(agent.lineage_id for agent in engine.agents)
        dominant_lineage = lineage_counts.most_common(1)[0][0] if lineage_counts else ""
        for agent in engine.agents:
            traits = agent.genome.traits
            color = _lineage_color(agent.lineage_id)
            radius = 5 if agent.lineage_id == dominant_lineage else 4
            pygame.draw.circle(screen, color, (int(agent.position.x * scale_x), int(agent.position.y * scale_y)), radius)
            if agent.lineage_id == dominant_lineage:
                pygame.draw.circle(screen, (245, 245, 210), (int(agent.position.x * scale_x), int(agent.position.y * scale_y)), radius + 2, width=1)
            if cfg.draw_perception:
                pygame.draw.circle(
                    screen,
                    (80, 80, 90),
                    (int(agent.position.x * scale_x), int(agent.position.y * scale_y)),
                    max(1, int(traits.perception_range * scale_x)),
                    width=1,
                )
        _draw_dashboard(screen, font, engine, history, sound_state, audio_ready)
        pygame.display.set_caption(f"ALife thesis simulation | step={engine.step_index} pop={len(engine.agents)}")
        pygame.display.flip()
        clock.tick(cfg.fps)
    pygame.quit()
    return engine.finish()


def _initialize_audio(pygame, enabled: bool) -> bool:
    if not enabled:
        return False
    try:
        pygame.mixer.pre_init(44100, -16, 2, 256)
        pygame.mixer.init()
        return True
    except pygame.error:
        return False


def _play_sound(pygame, state, duration_ms: int, volume: float) -> None:
    if not pygame.mixer.get_init():
        return
    sample_rate = pygame.mixer.get_init()[0]
    samples = synthesize_tone(state, sample_rate, duration_ms, volume)
    pygame.sndarray.make_sound(samples).play()


def _lineage_color(lineage_id: str) -> tuple[int, int, int]:
    digest = blake2b(lineage_id.encode("utf-8"), digest_size=3).digest()
    return tuple(80 + int(byte * 0.65) for byte in digest)


def _draw_zones(screen, engine: SimulationEngine, scale_x: float, scale_y: float) -> None:
    import pygame

    colors = {
        ZoneType.FERTILE: (32, 76, 48),
        ZoneType.POOR: (70, 62, 42),
        ZoneType.HAZARD: (88, 38, 52),
        ZoneType.NEUTRAL: (35, 35, 42),
    }
    for zone in engine.world.zones:
        radius = int(zone.radius * (scale_x + scale_y) / 2.0)
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        color = colors[zone.zone_type] + (95,)
        pygame.draw.circle(surface, color, (radius, radius), radius)
        screen.blit(surface, (int(zone.center.x * scale_x) - radius, int(zone.center.y * scale_y) - radius))


def _draw_dashboard(screen, font, engine: SimulationEngine, history: deque[tuple[int, int, float, float]], sound_state, audio_ready: bool) -> None:
    import pygame

    panel = pygame.Surface((420, 215), pygame.SRCALPHA)
    panel.fill((10, 12, 16, 185))
    screen.blit(panel, (12, 12))
    latest_diversity = history[-1][2] if history else 0.0
    dominant_short = sound_state.dominant_lineage[-8:] if sound_state.dominant_lineage else "none"
    lines = [
        f"step {engine.step_index}/{engine.config.simulation.steps}",
        f"population {len(engine.agents)}",
        f"resources {len(engine.world.resources)}",
        f"trait diversity {latest_diversity:.3f}",
        f"baseline distance {sound_state.baseline_distance:.3f}",
        f"dominant lineage {dominant_short} ({sound_state.dominance:.0%})",
        f"mean generation {sound_state.mean_generation:.1f}",
        f"audio {'on' if audio_ready else 'off'}",
        "color=lineage, outline=dominant",
        "ESC: stop and export",
    ]
    for idx, line in enumerate(lines):
        screen.blit(font.render(line, True, (230, 232, 236)), (24, 22 + idx * 20))
    _sparkline(screen, history, 24, 187, 85, 24, 0, (236, 115, 96))
    _sparkline(screen, history, 126, 187, 85, 24, 1, (94, 190, 120))
    _sparkline(screen, history, 228, 187, 85, 24, 2, (120, 160, 235))
    _sparkline(screen, history, 330, 187, 75, 24, 3, (235, 210, 105))


def _sparkline(screen, history: deque[tuple[int, int, float, float]], x: int, y: int, width: int, height: int, index: int, color: tuple[int, int, int]) -> None:
    import pygame

    pygame.draw.rect(screen, (58, 63, 72), (x, y, width, height), width=1)
    if len(history) < 2:
        return
    values = [entry[index] for entry in history]
    low = min(values)
    high = max(values)
    span = max(1e-9, high - low)
    points = []
    for i, value in enumerate(values):
        px = x + int(i * width / max(1, len(values) - 1))
        py = y + height - int((value - low) / span * (height - 2)) - 1
        points.append((px, py))
    pygame.draw.lines(screen, color, False, points, width=2)
