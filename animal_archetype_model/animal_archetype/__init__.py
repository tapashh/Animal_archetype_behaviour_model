"""
__init__.py
============
This file turns the `animal_archetype` folder into an importable Python
"package". It also re-exports the most important pieces so that other
code can simply write:

    from animal_archetype import PossibilisticArchetypeModel, TRAITS

instead of having to remember which exact file each class lives in.
"""

from .model import PossibilisticArchetypeModel
from .traits import TRAITS, TRAIT_NAMES, NUM_DIMENSIONS
from .archetypes import ARCHETYPE_CENTROIDS, get_archetype_names

__all__ = [
    "PossibilisticArchetypeModel",
    "TRAITS",
    "TRAIT_NAMES",
    "NUM_DIMENSIONS",
    "ARCHETYPE_CENTROIDS",
    "get_archetype_names",
]
