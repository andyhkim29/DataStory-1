# Quickstart: Prediction Markets vs. Polls Story

## Prerequisites

- Python 3.10 or newer
- A shell environment that can create a virtual environment

## Setup

1. Create and activate a virtual environment.
2. Install project dependencies from the pinned requirements file that will be
   committed with the notebook implementation.
3. Ensure you are at the repository root before running notebook commands.

## Run the notebook end to end

1. Open `prediction-markets-story/notebook.ipynb` in Jupyter and run all cells
   from top to bottom.
2. Alternatively, execute the notebook non-interactively with a notebook runner
   so reproducibility can be checked in one command.
3. Confirm that the notebook creates or refreshes:
   - `prediction-markets-story/data/raw/` source assets
   - `prediction-markets-story/data/processed/` per-race cleaned CSVs
   - `prediction-markets-story/figures/` exported charts
   - The rendered five-row summary table inside the notebook output

## Verification checklist

- The notebook completes with no manual file downloads.
- Each of the five analytical rows has a processed CSV.
- Each analytical row has a corresponding exported figure.
- The final notebook section includes a short findings summary under 500 words.
- Inline source documentation identifies the exact market and polling datasets
  used for each race.

## Expected repository layout after implementation

```text
prediction-markets-story/
├── notebook.ipynb
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
└── figures/
```
