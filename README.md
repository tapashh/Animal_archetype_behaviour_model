# Animal Archetype Human Behavior Model

A possibilistic membership model that matches a person's behavioral traits
against evolutionary animal archetypes (Chimpanzee, Wolf, Raven, Octopus,
and others), using distance-decay math instead of forced either/or
classification.

This README explains what's in this project and exactly how to run each
piece, written for someone who isn't deeply technical yet.

---

## What's in this folder

```
animal_archetype/
├── animal_archetype/          <- the core Python package (the "brain")
│   ├── traits.py               - defines the 18 traits and their order
│   ├── archetypes.py           - defines animal centroid trait values
│   ├── model.py                - the possibilistic math itself
│   ├── api.py                  - FastAPI REST API (roadmap item #2)
│   ├── cli.py                  - a terminal demo you can run right now
│   └── __init__.py             - makes the folder an importable package
├── frontend/
│   └── index.html               - the front-end UI (roadmap item #3)
├── notebooks/
│   └── exploration.ipynb        - JupyterLab notebook for experimenting
├── requirements.txt             - list of Python packages needed
└── README.md                    - this file
```

Every file has extensive comments inside explaining what each part does
and why - open any `.py` file in a text editor to read along.

---


## Quickest way to try it: the front-end (no installation needed)

Just open `frontend/index.html` in any web browser (double-click it).
Move the sliders, click "Randomize," and watch the archetype match
percentages and the radar chart update instantly. This runs entirely in
your browser - no Python, no server, nothing to install.

---

## Option 2: Run the terminal demo

This requires Python installed on your computer (version 3.9 or newer).

```bash
# 1. Move into the project folder
cd animal_archetype

# 2. Install the required libraries (only needed once)
pip install -r requirements.txt

# 3. Run the interactive demo
python -m animal_archetype.cli
```

It will ask you to rate yourself on all 18 traits (or press Enter to
auto-fill random values), then print your ranked archetype matches.

---

## Option 3: Run the production REST API


```bash
cd animal_archetype
pip install -r requirements.txt
uvicorn animal_archetype.api:app --reload
```

Then open your browser to **http://127.0.0.1:8000/docs** - FastAPI
automatically builds an interactive test page there where you can try
every endpoint by clicking buttons, no coding required.

Available endpoints:
- `GET /traits` - lists all 18 traits the model expects, in order
- `GET /archetypes` - lists all available animal archetypes
- `POST /profile` - send a person's 18 trait scores, get back their
  full match profile

---

## Option 4: Use it directly in Python code / Jupyter

```python
from animal_archetype import PossibilisticArchetypeModel, TRAIT_NAMES

model = PossibilisticArchetypeModel(beta=2500.0)

# Build a trait vector - order must match TRAIT_NAMES
my_traits = [70, 65, 55, 80, 60, 55, 40, 65, 70,
             50, 75, 60, 35, 70, 80, 60, 65, 75]

profile = model.profile(my_traits)
for archetype, match_percent in profile.items():
    print(f"{archetype}: {match_percent:.1f}%")
```

See `notebooks/exploration.ipynb` for a ready-to-run notebook version of
this, plus experiments with different `beta` values.

---

## How the math works (plain-language summary)

1. **Vector representation** - you (or any person) become a list of 18
   numbers, one per trait, each from 0-100.
2. **Euclidean distance** - for each animal archetype, we measure how far
   your numbers are from that archetype's "typical" numbers, using
   squared distance: `sum((your_value - archetype_value)^2)` across all
   18 traits.
3. **Possibilistic decay** - that raw distance number gets converted into
   a friendly 0-100% match score using: `match = 100 * exp(-distance / beta)`.
   A perfect match (distance = 0) always scores 100%. Bigger distances
   score lower. The `beta` parameter controls how strict or lenient this
   grading is - see the big comment block at the top of `model.py` for a
   full walkthrough with real numbers.

Because every archetype is scored independently (not forced to add up to
100% across archetypes), you can genuinely be "88% Wolf AND 85% Octopus"
at the same time - which is the whole point of a possibilistic model
versus a traditional either/or classifier.

---

## Where collaborators should look

- **Data Scientists**: `model.py`, specifically the `beta` parameter and
  the `decay()` function. Also see `notebooks/exploration.ipynb`.
- **Software Engineers**: the whole `animal_archetype/` package is
  already modularized out of notebook form, ready for packaging /
  deployment (e.g. Docker, cloud hosting for `api.py`).
- **Researchers**: `traits.py` (trait definitions) and `archetypes.py`
  (the animal centroid values) are the two files to refine.
