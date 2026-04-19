"""Command-line interface for running artificial-life simulations.

The file intentionally lives at the repository root so PyCharm users can run
the project directly without installing it as a package first.
"""

from __future__ import annotations

import argparse
import logging

from src.analytics.export import export_accessible_summary, export_final_population, export_metrics, export_summary
from src.core.config import load_config
from src.experiments.runner import run_experiment
from src.simulation.engine import SimulationEngine
from src.utils.logging import configure_logging
from src.visualization.live import run_live
from src.visualization.plots import plot_population_snapshot, plot_run_metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Artificial Life thesis simulation framework")
    parser.add_argument("--config", default="configs/default.yaml", help="YAML simulation config")
    parser.add_argument("--experiment", help="YAML experiment config with parameter sweep")
    parser.add_argument("--live", action="store_true", help="Run the live pygame visualization")
    parser.add_argument("--plot", action="store_true", help="Generate post-run plots")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging()
    log = logging.getLogger("alife.main")
    if args.experiment:
        result = run_experiment(args.experiment)
        log.info("Experiment complete: %s", result.summary_csv)
        return

    config = load_config(args.config)
    if args.live or config.visualization.enabled:
        result = run_live(SimulationEngine(config))
        metrics_path = export_metrics(result.metrics, result.output_dir)
        population_path = export_final_population(result.agents, result.output_dir)
        export_summary(config, result.metrics, result.output_dir, result.extinct)
        export_accessible_summary(result.metrics, result.agents, result.output_dir)
        plot_run_metrics(metrics_path, result.output_dir / "plots")
        plot_population_snapshot(population_path, result.output_dir / "plots")
        log.info("Live run exported: %s | extinct=%s | final_population=%s", result.output_dir, result.extinct, len(result.agents))
        return

    engine = SimulationEngine(config)
    last_reported = -1

    def report_progress(active_engine: SimulationEngine) -> None:
        nonlocal last_reported
        interval = max(1, config.simulation.steps // 10)
        if active_engine.step_index == 1 or active_engine.step_index - last_reported >= interval:
            last_reported = active_engine.step_index
            log.info(
                "Progress: step %s/%s | population=%s | resources=%s",
                active_engine.step_index,
                config.simulation.steps,
                len(active_engine.agents),
                len(active_engine.world.resources),
            )

    result = engine.run(progress_callback=report_progress)
    metrics_path = export_metrics(result.metrics, result.output_dir)
    population_path = export_final_population(result.agents, result.output_dir)
    export_summary(config, result.metrics, result.output_dir, result.extinct)
    export_accessible_summary(result.metrics, result.agents, result.output_dir)
    if args.plot:
        plot_run_metrics(metrics_path, result.output_dir / "plots")
        plot_population_snapshot(population_path, result.output_dir / "plots")
    log.info("Run complete: %s | extinct=%s | final_population=%s", result.output_dir, result.extinct, len(result.agents))


if __name__ == "__main__":
    main()
