"""Compact feedforward networks evolved without backpropagation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.core.rng import RandomStreams


@dataclass(slots=True)
class NeuralGenome:
    """Two-layer tanh network parameters inherited by neural organisms."""

    w1: np.ndarray
    b1: np.ndarray
    w2: np.ndarray
    b2: np.ndarray

    @classmethod
    def random(cls, input_size: int, hidden_size: int, output_size: int, rng: RandomStreams) -> "NeuralGenome":
        scale1 = 1.0 / np.sqrt(input_size)
        scale2 = 1.0 / np.sqrt(hidden_size)
        return cls(
            w1=rng.np.normal(0.0, scale1, size=(hidden_size, input_size)),
            b1=np.zeros(hidden_size),
            w2=rng.np.normal(0.0, scale2, size=(output_size, hidden_size)),
            b2=np.zeros(output_size),
        )

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        hidden = np.tanh(self.w1 @ inputs + self.b1)
        return np.tanh(self.w2 @ hidden + self.b2)

    def copy(self) -> "NeuralGenome":
        return NeuralGenome(self.w1.copy(), self.b1.copy(), self.w2.copy(), self.b2.copy())

    def mutated(self, sigma: float, rng: RandomStreams) -> "NeuralGenome":
        child = self.copy()
        child.w1 += rng.np.normal(0.0, sigma, child.w1.shape)
        child.b1 += rng.np.normal(0.0, sigma, child.b1.shape)
        child.w2 += rng.np.normal(0.0, sigma, child.w2.shape)
        child.b2 += rng.np.normal(0.0, sigma, child.b2.shape)
        return child

