"""Logging setup for command-line runs."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_dir: str | Path = "data/logs", level: int = logging.INFO) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(Path(log_dir) / "alife_simulation.log", encoding="utf-8"),
        ],
    )

