
import random

from .traits import TRAITS
from .model import PossibilisticArchetypeModel


def ask_for_trait_value(trait_label: str) -> float:
    """
    Prompts the user for a single trait score, and keeps asking until
    they type a valid number between 0 and 100.
    """
    while True:
        raw = input(f"  {trait_label} (0-100): ").strip()
        if raw == "":
            # Empty input -> pick a random value so the demo still works
            # even if someone just wants to see output quickly.
            value = round(random.uniform(0, 100), 1)
            print(f"    (no input - using random value {value})")
            return value
        try:
            value = float(raw)
        except ValueError:
            print("    Please type a number between 0 and 100.")
            continue
        if 0 <= value <= 100:
            return value
        print("    Please enter a value between 0 and 100.")


def collect_user_vector() -> list:
    """Walks the user through entering a score for every trait."""
    print("\nRate yourself from 0 (very low) to 100 (very high) on each trait.")
    print("Press Enter on any question to auto-fill a random value.\n")

    vector = []
    for trait in TRAITS:
        value = ask_for_trait_value(trait.label)
        vector.append(value)
    return vector


def print_profile(profile: dict) -> None:
    """Nicely prints the ranked archetype match percentages."""
    print("\n================ YOUR ARCHETYPE PROFILE ================")
    for rank, (archetype, score) in enumerate(profile.items(), start=1):
        bar_length = int(score / 2)  # simple text bar, 0-50 characters
        bar = "#" * bar_length
        print(f"{rank}. {archetype:<12} {score:6.2f}%  {bar}")
    print("==========================================================\n")

    top_archetype = next(iter(profile))
    print(f"Your closest match is: {top_archetype}\n")


def main():
    print("Welcome to the Animal Archetype Human Behavior Model demo!")

    # Create the model. beta=800 is the default tuning value explained
    # in model.py - feel free to experiment by changing it here.
    model = PossibilisticArchetypeModel(beta=2500.0)

    user_vector = collect_user_vector()
    profile = model.profile(user_vector)
    print_profile(profile)


if __name__ == "__main__":
    main()
