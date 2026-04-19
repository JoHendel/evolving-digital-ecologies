"""Data export helpers for reproducible runs."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from src.agents.agent import Agent
from src.analytics.metrics import StepMetrics
from src.core.config import AppConfig, config_to_dict


def metrics_to_frame(metrics: list[StepMetrics]) -> pd.DataFrame:
    return pd.DataFrame([m.to_dict() for m in metrics])


def export_metrics(metrics: list[StepMetrics], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "metrics.csv"
    metrics_to_frame(metrics).to_csv(path, index=False)
    return path


def export_final_population(agents: list[Agent], output_dir: Path) -> Path:
    rows = []
    for agent in agents:
        row = {
            "id": agent.id,
            "parent_id": agent.parent_id,
            "lineage_id": agent.lineage_id,
            "generation": agent.generation,
            "age": agent.age,
            "energy": agent.energy,
            "x": agent.position.x,
            "y": agent.position.y,
        }
        row.update({f"trait_{name}": value for name, value in agent.genome.traits.items()})
        rows.append(row)
    path = output_dir / "final_population.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def export_summary(config: AppConfig, metrics: list[StepMetrics], output_dir: Path, extinct: bool) -> Path:
    final = metrics[-1].to_dict() if metrics else {}
    summary = {"config": config_to_dict(config), "final_metrics": final, "extinct": extinct}
    path = output_dir / "summary.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    return path


def export_accessible_summary(metrics: list[StepMetrics], agents: list[Agent], output_dir: Path) -> Path:
    """Write a plain-language text summary for accessible post-run review."""

    path = output_dir / "accessible_summary.txt"
    if not metrics:
        text = "Es wurden keine Metriken aufgezeichnet.\n"
    else:
        first = metrics[0]
        final = metrics[-1]
        peak = max(metrics, key=lambda metric: metric.population)
        min_resources = min(metrics, key=lambda metric: metric.resources)
        lineage_count = len({agent.lineage_id for agent in agents})
        text = (
            "Barrierearme Zusammenfassung des Simulationslaufs\n"
            "================================================\n\n"
            f"Erster Messpunkt: Schritt {first.step}, Population {first.population}, Ressourcen {first.resources}.\n"
            f"Finaler Messpunkt: Schritt {final.step}, Population {final.population}, Ressourcen {final.resources}.\n"
            f"Maximale Population: {peak.population} bei Schritt {peak.step}.\n"
            f"Minimale Ressourcenanzahl: {min_resources.resources} bei Schritt {min_resources.step}.\n"
            f"Finale mittlere Energie: {final.mean_energy:.2f}.\n"
            f"Finale Trait-Diversitaet: {final.trait_diversity:.3f}.\n"
            f"Finale Baseline Distance: {final.baseline_distance:.3f}.\n"
            f"Trait-Baseline-Distanz: {final.trait_baseline_distance:.3f}.\n"
            f"Sound-Baseline-Distanz: {final.sound_baseline_distance:.3f}.\n"
            f"Visual-Baseline-Distanz: {final.visual_baseline_distance:.3f}.\n"
            f"Finale lebende Abstammungslinien: {lineage_count}.\n\n"
            "Interpretationshilfe:\n"
            "- Sinkende Ressourcen bei wachsender Population deuten auf Ressourcenknappheit hin.\n"
            "- Sinkende Trait-Diversitaet kann auf Selektion und Konvergenz hindeuten.\n"
            "- Wenige finale Abstammungslinien deuten auf Linien-Dominanz hin.\n"
            "- Eine einzelne finale Linie spricht fuer einen evolutionaeren Sweep.\n"
            "- Eine steigende Baseline Distance bedeutet, dass sich das System vom Anfangszustand entfernt.\n"
        )
    with path.open("w", encoding="utf-8") as fh:
        fh.write(text)
    return path
