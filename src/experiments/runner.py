"""Experiment runner supporting parameter sweeps and independent repeats."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.analytics.export import export_final_population, export_metrics, export_summary
from src.core.config import AppConfig, ExperimentConfig, load_config, set_nested
from src.simulation.engine import run_simulation
from src.visualization.plots import plot_run_metrics


@dataclass(slots=True)
class ExperimentResult:
    """Summary of an experiment sweep."""

    summary_csv: Path
    run_directories: list[Path]


def load_experiment(path: str | Path) -> ExperimentConfig:
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return ExperimentConfig(**data)


def iter_conditions(sweep: dict[str, list[Any]]) -> list[dict[str, Any]]:
    if not sweep:
        return [{}]
    keys = list(sweep)
    return [dict(zip(keys, values)) for values in product(*(sweep[k] for k in keys))]


def condition_name(condition: dict[str, Any]) -> str:
    if not condition:
        return "baseline"
    return "__".join(f"{k.replace('.', '-')}_{str(v).replace('.', 'p')}" for k, v in condition.items())


def run_experiment(path: str | Path) -> ExperimentResult:
    exp = load_experiment(path)
    base = load_config(exp.base_config)
    rows: list[dict[str, Any]] = []
    run_dirs: list[Path] = []
    for condition in iter_conditions(exp.sweep):
        for repeat in range(exp.repeats):
            config: AppConfig = deepcopy(base)
            for key, value in condition.items():
                set_nested(config, key, value)
            name = f"{exp.name}/{condition_name(condition)}/repeat_{repeat:03d}"
            config.simulation.run_name = name
            config.simulation.seed = base.simulation.seed + repeat + 10_000 * len(rows)
            result = run_simulation(config)
            metrics_path = export_metrics(result.metrics, result.output_dir)
            export_final_population(result.agents, result.output_dir)
            export_summary(config, result.metrics, result.output_dir, result.extinct)
            plot_run_metrics(metrics_path, result.output_dir / "plots")
            final_population = result.metrics[-1].population if result.metrics else len(result.agents)
            rows.append(
                {
                    "experiment": exp.name,
                    "condition": condition_name(condition),
                    "repeat": repeat,
                    "run_dir": str(result.output_dir),
                    "extinct": result.extinct,
                    "final_population": final_population,
                    "final_trait_diversity": result.metrics[-1].trait_diversity if result.metrics else 0.0,
                    **{f"param_{k}": v for k, v in condition.items()},
                }
            )
            run_dirs.append(result.output_dir)
    summary_dir = Path(base.simulation.output_dir) / exp.name
    summary_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = summary_dir / "experiment_summary.csv"
    pd.DataFrame(rows).to_csv(summary_csv, index=False)
    return ExperimentResult(summary_csv=summary_csv, run_directories=run_dirs)

