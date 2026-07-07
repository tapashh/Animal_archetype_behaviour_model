
from typing import Dict, List

from fastapi import FastAPI, HTTPException
# Pydantic is the library FastAPI uses to validate incoming data
# automatically - if someone sends bad data, it rejects it with a clear
# error before our code even runs, which prevents a lot of bugs.
from pydantic import BaseModel, Field

from .traits import TRAITS, TRAIT_NAMES, NUM_DIMENSIONS
from .archetypes import get_archetype_names
from .model import PossibilisticArchetypeModel


# Create the FastAPI application object. This is the "server" itself.
app = FastAPI(
    title="Animal Archetype Human Behavior Model API",
    description=(
        "Possibilistic membership model that matches a person's trait "
        "vector against evolutionary animal archetypes."
    ),
    version="0.1.0",
)

# Create ONE shared instance of the model when the server starts up,
# instead of recreating it on every request (that would be wasteful).
# beta=2500.0 is the default tuning parameter - see model.py for details.
model = PossibilisticArchetypeModel(beta=2500.0)


class TraitVectorRequest(BaseModel):
    
    traits: Dict[str, float] = Field(
        ...,
        description=(
            "A dictionary of all 18 trait names mapped to scores "
            "between 0 and 100. See GET /traits for the exact list "
            "of expected names."
        ),
        examples=[{name: 50.0 for name in TRAIT_NAMES}],
    )


class ArchetypeProfileResponse(BaseModel):
    """Defines exactly what shape of data the /profile endpoint returns."""
    profile: Dict[str, float] = Field(
        ..., description="Archetype name -> match percentage (0-100), best match first."
    )
    best_match: str = Field(..., description="The single closest archetype.")


def _traits_dict_to_ordered_vector(traits_dict: Dict[str, float]) -> List[float]:
    """
    Converts a {trait_name: value} dictionary (order doesn't matter, as
    received over the web) into the fixed-order list the model expects
    internally (order DOES matter - see traits.py).

    Also gives friendly errors if a trait is missing or misspelled,
    instead of a confusing crash.
    """
    missing = [name for name in TRAIT_NAMES if name not in traits_dict]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing trait(s) in request: {missing}. "
                   f"Call GET /traits to see the required trait names.",
        )

    unknown = [name for name in traits_dict if name not in TRAIT_NAMES]
    if unknown:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown trait name(s) in request: {unknown}. "
                   f"Call GET /traits to see the valid trait names.",
        )

    return [traits_dict[name] for name in TRAIT_NAMES]


@app.get("/traits", summary="List all traits the model expects")
def list_traits():
    """Returns every trait name, display label, and category, in order."""
    return [
        {"name": t.name, "label": t.label, "category": t.category}
        for t in TRAITS
    ]


@app.get("/archetypes", summary="List all available animal archetypes")
def list_archetypes():
    """Returns the names of every archetype the model can match against."""
    return {"archetypes": get_archetype_names()}


@app.post(
    "/profile",
    response_model=ArchetypeProfileResponse,
    summary="Get a person's archetype match profile",
)
def get_profile(request: TraitVectorRequest):
    """
    Main endpoint. Send a person's 18 trait scores, receive back their
    match percentage against every animal archetype, sorted from best
    to worst match.
    """
    try:
        vector = _traits_dict_to_ordered_vector(request.traits)
        profile = model.profile(vector)
        best = next(iter(profile))
        return ArchetypeProfileResponse(profile=profile, best_match=best)
    except ValueError as e:
        # Turns a plain Python error (e.g. value out of 0-100 range)
        # into a proper web error response with a clear message.
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/", summary="Health check")
def root():
    """Simple endpoint to confirm the server is running."""
    return {
        "status": "ok",
        "message": "Animal Archetype API is running. Visit /docs to try it out.",
        "num_dimensions": NUM_DIMENSIONS,
    }
