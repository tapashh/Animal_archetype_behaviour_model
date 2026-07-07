
from typing import Dict, List
import numpy as np  # NumPy = fast, vectorized math library for Python

from .traits import NUM_DIMENSIONS, TRAIT_NAMES, validate_vector
from .archetypes import ARCHETYPE_CENTROIDS


class PossibilisticArchetypeModel:
    
    def __init__(self, beta: float = 2500.0):
        
        if beta <= 0:
            raise ValueError("beta must be a positive number.")
        self.beta = beta

        # Pre-convert every archetype centroid from a plain Python list
        # into a NumPy array, once, so that later calculations are fast.
        # (NumPy arrays support fast vectorized subtraction/squaring,
        # which a plain Python list does not.)
        self._centroids: Dict[str, np.ndarray] = {
            name: np.array(vector, dtype=float)
            for name, vector in ARCHETYPE_CENTROIDS.items()
        }

    # ------------------------------------------------------------------
    # Core math functions
    # ------------------------------------------------------------------

    @staticmethod
    def squared_euclidean_distance(x: np.ndarray, c: np.ndarray) -> float:
    
        diff = x - c              # element-wise subtraction
        squared = diff ** 2       # element-wise squaring
        return float(np.sum(squared))

    def decay(self, distance_sq: float) -> float:
        
        match_fraction = np.exp(-distance_sq / self.beta)  # value in (0, 1]
        return float(match_fraction * 100.0)

    # ------------------------------------------------------------------
    # Public-facing methods
    # ------------------------------------------------------------------

    def match_single(self, user_vector: List[float], archetype_name: str) -> float:
        
        if archetype_name not in self._centroids:
            available = ", ".join(self._centroids.keys())
            raise KeyError(
                f"Unknown archetype '{archetype_name}'. "
                f"Available archetypes: {available}"
            )

        validate_vector(user_vector)  # catches bad input early with a clear error
        x = np.array(user_vector, dtype=float)
        c = self._centroids[archetype_name]

        distance_sq = self.squared_euclidean_distance(x, c)
        return self.decay(distance_sq)

    def profile(self, user_vector: List[float]) -> Dict[str, float]:
        
        validate_vector(user_vector)
        x = np.array(user_vector, dtype=float)

        raw_scores = {}
        for name, centroid in self._centroids.items():
            distance_sq = self.squared_euclidean_distance(x, centroid)
            raw_scores[name] = self.decay(distance_sq)

        # Sort so the best match appears first - much nicer for reports/UIs.
        sorted_scores = dict(
            sorted(raw_scores.items(), key=lambda item: item[1], reverse=True)
        )
        return sorted_scores

    def best_match(self, user_vector: List[float]) -> str:
        
        profile = self.profile(user_vector)
        return next(iter(profile))  # first key of the sorted dict = best match
