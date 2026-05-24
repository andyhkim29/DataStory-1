# Prediction Markets vs. Polls Story

This project builds a notebook-first comparison of prediction-market signals and
polling or forecast-side signals across five U.S. election case studies:
2020 president, 2022 House control, 2022 Senate control, 2022 Pennsylvania
Senate, and 2024 president.

## Run

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r prediction-markets-story/requirements.txt
```

3. Execute the notebook logic from the repository root:

```bash
python tools/run_notebook_cells.py prediction-markets-story/notebook.ipynb
```

## Outputs

Running the notebook refreshes:

- `prediction-markets-story/data/raw/` for downloaded or checked-in source
  assets
- `prediction-markets-story/data/processed/` for one cleaned CSV per race plus
  the summary table
- `prediction-markets-story/figures/` for one exported Plotly HTML chart per
  race

## Notes

- Market history is parsed from ElectionBettingOdds historical chart pages.
- Candidate-race polling checkpoints are stored in a checked-in fixture built
  from archived polling-average reporting.
- The chamber-control comparison also uses a checked-in checkpoint fixture based
  on published FiveThirtyEight forecast writeups because the old historical CSV
  endpoints no longer provide a reliable machine-readable archive.
