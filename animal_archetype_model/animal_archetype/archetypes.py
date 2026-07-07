
from typing import Dict, List
from .traits import TRAIT_NAMES, validate_vector


# Order reminder (matches traits.py exactly):
# 0 strategic_thinking   1 learning_speed      2 creativity
# 3 curiosity            4 empathy             5 agreeableness
# 6 social_dependence    7 communication_style 8 emotional_stability
# 9 dominance            10 independence       11 long_term_planning
# 12 impulsiveness       13 discipline         14 adaptability
# 15 risk_taking         16 ambition           17 persistence

ARCHETYPE_CENTROIDS: Dict[str, List[float]] = {

    # Chimpanzee: highly social, political, strategic, ambitious,
    # dominance-seeking, but still capable of strong group cooperation.
    "Chimpanzee": [
        85, 75, 55, 65,   # strategic_thinking, learning_speed, creativity, curiosity
        45, 50, 80, 70,   # empathy, agreeableness, social_dependence, communication_style
        55,               # emotional_stability
        85, 40, 60,       # dominance, independence, long_term_planning
        55, 50, 65,       # impulsiveness, discipline, adaptability
        60, 80, 70,       # risk_taking, ambition, persistence
    ],

    # Wolf: loyal pack-oriented, disciplined, protective, cooperative
    # but independent-minded when needed, high persistence and stability.
    "Wolf": [
        65, 60, 40, 50,
        70, 75, 85, 55,
        75,
        60, 55, 70,
        30, 80, 60,
        45, 60, 85,
    ],

    # Raven: highly intelligent, curious, creative problem-solvers,
    # independent, adaptable, playful risk-takers, less socially bound.
    "Raven": [
        80, 90, 90, 95,
        40, 45, 30, 60,
        60,
        45, 85, 55,
        60, 45, 90,
        70, 55, 60,
    ],

    # Octopus: solitary, extremely adaptable and creative problem-solver,
    # low social dependence, high independence, low long-term planning
    # (short lifespan / opportunistic), high curiosity, impulsive.
    "Octopus": [
        60, 85, 95, 90,
        30, 35, 10, 30,
        50,
        20, 95, 25,
        75, 35, 95,
        80, 40, 45,
    ],

    # --- A few extra archetypes so the demo has more variety.
    # Feel free to delete these if you only want the four named
    # in your project description. ---

    # Lion: dominant, confident, ambitious, socially embedded within a
    # pride, moderate strategic thinking, lower adaptability (relies on
    # strength/status rather than flexibility).
    "Lion": [
        60, 50, 35, 40,
        45, 55, 70, 65,
        70,
        95, 45, 55,
        50, 55, 40,
        55, 85, 75,
    ],

    # Owl: quiet, observant, highly strategic and disciplined, low
    # impulsiveness, moderate social dependence, calm and stable.
    "Owl": [
        90, 65, 60, 70,
        55, 60, 40, 45,
        85,
        40, 70, 85,
        15, 85, 55,
        30, 55, 80,
    ],

    # Dolphin: highly social, empathetic, playful, creative communicator,
    # emotionally stable, adaptable, curious.
    "Dolphin": [
        70, 80, 80, 85,
        85, 85, 75, 90,
        80,
        45, 50, 55,
        45, 55, 80,
        55, 50, 60,
    ],
}


def get_archetype_names() -> List[str]:
    """Returns the list of all archetype names currently defined."""
    return list(ARCHETYPE_CENTROIDS.keys())


# --- Safety check: run validation once, when this module is imported ---
# This guarantees every centroid has exactly 18 values, all within 0-100,
# so a typo (like an extra/missing number) is caught immediately instead
# of causing a confusing bug later.
for _name, _vector in ARCHETYPE_CENTROIDS.items():
    try:
        validate_vector(_vector)
    except ValueError as e:
        raise ValueError(f"Archetype '{_name}' has an invalid vector: {e}")
