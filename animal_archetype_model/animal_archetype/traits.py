
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Trait:
    """
    A single trait definition.

    name     -> short machine-friendly identifier (e.g. "strategic_thinking")
    label    -> human-friendly display name (e.g. "Strategic Thinking")
    category -> which group it belongs to, useful for grouping in reports/UI
    """
    name: str
    label: str
    category: str


# The ordered list of all traits tracked by the model.
# ORDER MATTERS: this list defines the position of each trait inside
# every vector used throughout the whole project.
TRAITS: List[Trait] = [
    # --- Cognitive Traits ---
    Trait("strategic_thinking", "Strategic Thinking", "Cognitive"),
    Trait("learning_speed",     "Learning Speed",     "Cognitive"),
    Trait("creativity",         "Creativity",         "Cognitive"),
    Trait("curiosity",          "Curiosity",          "Cognitive"),

    # --- Social & Emotional Traits ---
    Trait("empathy",             "Empathy",             "Social & Emotional"),
    Trait("agreeableness",       "Agreeableness",       "Social & Emotional"),
    Trait("social_dependence",   "Social Dependence",   "Social & Emotional"),
    Trait("communication_style", "Communication Style", "Social & Emotional"),
    Trait("emotional_stability", "Emotional Stability", "Social & Emotional"),

    # --- Action-Oriented Traits ---
    Trait("dominance",        "Dominance",         "Action-Oriented"),
    Trait("independence",     "Independence",      "Action-Oriented"),
    Trait("long_term_planning", "Long-term Planning", "Action-Oriented"),
    Trait("impulsiveness",    "Impulsiveness",      "Action-Oriented"),
    Trait("discipline",       "Discipline",         "Action-Oriented"),
    Trait("adaptability",     "Adaptability",       "Action-Oriented"),
    Trait("risk_taking",      "Risk Taking",        "Action-Oriented"),
    Trait("ambition",         "Ambition",           "Action-Oriented"),
    Trait("persistence",      "Persistence",        "Action-Oriented"),
]

# Convenience list of just the machine-friendly names, in the fixed order.
TRAIT_NAMES: List[str] = [t.name for t in TRAITS]

# How many dimensions the vector actually has (18, per the reasoning above).
NUM_DIMENSIONS: int = len(TRAITS)

# The valid range for every trait score.
MIN_SCORE = 0
MAX_SCORE = 100


def validate_vector(values: List[float]) -> None:
    
    if len(values) != NUM_DIMENSIONS:
        raise ValueError(
            f"Expected {NUM_DIMENSIONS} trait values (one per trait in "
            f"TRAITS), but got {len(values)}. "
            f"Traits expected, in order: {TRAIT_NAMES}"
        )
    for name, value in zip(TRAIT_NAMES, values):
        if not (MIN_SCORE <= value <= MAX_SCORE):
            raise ValueError(
                f"Trait '{name}' has value {value}, which is outside the "
                f"allowed range [{MIN_SCORE}, {MAX_SCORE}]."
            )
