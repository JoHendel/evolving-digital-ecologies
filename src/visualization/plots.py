"""Post-run scientific plotting utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_run_metrics(metrics_csv: str | Path, output_dir: str | Path) -> list[Path]:
    """Generate standard population and trait-evolution plots for one run."""

    df = pd.read_csv(metrics_csv)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    if df.empty:
        return paths

    paths.append(_line_plot(df, "step", ["population", "resources"], out / "population_resources.png", "Population and resources"))
    paths.append(_line_plot(df, "step", ["mean_energy", "trait_diversity"], out / "energy_diversity.png", "Energy and diversity"))
    paths.append(_line_plot(df, "step", ["mean_speed", "mean_perception_range", "mean_metabolism"], out / "trait_evolution.png", "Trait evolution"))
    paths.append(_line_plot(df, "step", ["clustering_index", "live_lineages"], out / "spatial_lineage.png", "Spatial aggregation and lineages"))
    paths.append(_line_plot(df, "step", ["baseline_distance", "trait_baseline_distance", "sound_baseline_distance", "visual_baseline_distance"], out / "baseline_distance.png", "Distance from original baseline"))
    paths.append(_phase_plot(df, out / "population_energy_phase.png"))
    return paths


def plot_population_snapshot(final_population_csv: str | Path, output_dir: str | Path) -> list[Path]:
    """Generate final spatial and trait-distribution plots from surviving agents."""

    df = pd.read_csv(final_population_csv)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    if df.empty:
        return []
    paths = [
        _scatter_plot(df, out / "final_spatial_traits.png"),
        _histogram_grid(df, out / "final_trait_histograms.png"),
    ]
    return paths


def plot_experiment_comparison(summary_csv: str | Path, output_path: str | Path) -> Path:
    """Plot final population by experimental condition."""

    df = pd.read_csv(summary_csv)
    fig, ax = plt.subplots(figsize=(9, 5))
    df.boxplot(column="final_population", by="condition", ax=ax, rot=25)
    ax.set_title("Final population by condition")
    ax.set_ylabel("Final population")
    fig.suptitle("")
    fig.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _line_plot(df: pd.DataFrame, x: str, columns: list[str], path: Path, title: str) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in columns:
        if col in df:
            ax.plot(df[x], df[col], label=col)
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _phase_plot(df: pd.DataFrame, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(df["population"], df["mean_energy"], c=df["step"], s=18, cmap="viridis")
    ax.set_title("Population-energy trajectory")
    ax.set_xlabel("population")
    ax.set_ylabel("mean energy")
    ax.grid(alpha=0.25)
    fig.colorbar(scatter, ax=ax, label="step")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _scatter_plot(df: pd.DataFrame, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(
        df["x"],
        df["y"],
        c=df["trait_social_tendency"],
        s=20 + 16 * df["trait_aggression"],
        cmap="coolwarm",
        alpha=0.78,
        edgecolors="none",
    )
    ax.set_title("Final spatial distribution: color=social tendency, size=aggression")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="box")
    fig.colorbar(scatter, ax=ax, label="social tendency")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _histogram_grid(df: pd.DataFrame, path: Path) -> Path:
    columns = [
        "trait_speed",
        "trait_perception_range",
        "trait_metabolism",
        "trait_aggression",
        "trait_social_tendency",
        "trait_risk_sensitivity",
    ]
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    for ax, col in zip(axes.ravel(), columns):
        ax.hist(df[col], bins=24, color="#5a82c8", alpha=0.85)
        ax.set_title(col.replace("trait_", ""))
        ax.grid(alpha=0.2)
    fig.suptitle("Final surviving trait distributions")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
