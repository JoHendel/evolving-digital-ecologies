from pathlib import Path
from uuid import uuid4

import yaml

from src.experiments.runner import run_experiment


def test_experiment_runner_creates_summary() -> None:
    root = Path("data/test_runs") / f"experiment_runner_{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=True)
    base = {
        "simulation": {
            "steps": 20,
            "seed": 5,
            "metrics_interval": 5,
            "output_dir": str(root / "runs"),
            "run_name": "base",
        },
        "agents": {"initial_population": 8, "initial_energy": 80.0},
        "world": {"resources": {"initial_count": 20, "spawn_rate": 0.5, "max_count": 40}},
    }
    base_path = root / "base.yaml"
    exp_path = root / "exp.yaml"
    base_path.write_text(yaml.safe_dump(base), encoding="utf-8")
    exp_path.write_text(
        yaml.safe_dump({"name": "tiny", "base_config": str(base_path), "repeats": 1, "sweep": {"mutation.rate": [0.01, 0.02]}}),
        encoding="utf-8",
    )
    result = run_experiment(exp_path)
    assert result.summary_csv.exists()
    assert len(result.run_directories) == 2
