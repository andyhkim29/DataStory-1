# Contract: Notebook Inputs and Outputs

## Execution Entry Point

- **Primary entry point**: `prediction-markets-story/notebook.ipynb`
- **Execution contract**: Running the notebook from the first cell to the last
  cell MUST complete the full workflow of acquisition, cleaning, classification,
  charting, and summary generation without manual intervention.

## Input Contract

### Source acquisition

- Market and polling source assets MUST be read from `prediction-markets-story/data/raw/`
  when already present.
- If required assets are absent and remote retrieval is allowed by the chosen
  implementation path, the notebook MUST download them to deterministic paths in
  `prediction-markets-story/data/raw/` before processing.
- Each source asset used in the notebook MUST be documented inline with a source
  name and source URL.

### Race coverage

The notebook MUST produce outputs for exactly these analytical rows:

1. 2020 US presidential election
2. 2022 House control
3. 2022 Senate control
4. 2022 Pennsylvania Senate race
5. 2024 US presidential election

## Processed file contract

The notebook MUST write one processed CSV per analytical row under
`prediction-markets-story/data/processed/`.

Each processed CSV MUST contain these columns exactly:

- `date`
- `market_prob_winner`
- `market_prob_loser`
- `poll_value_winner`
- `poll_value_loser`
- `source_market`
- `source_poll`

Additional derived columns MAY appear in notebook memory for analysis, but the
persisted per-race CSVs MUST contain at least the required columns above.

## Checkpoint classification contract

- Checkpoints are `90d`, `30d`, and `eve`.
- `eve` means the day before election day.
- Market classifications use `yes`, `no`, or `toss-up`, where probabilities
  inside 48 to 52 are `toss-up`.
- Poll classifications use `yes`, `no`, or `toss-up`, where winner-vs-loser
  gaps inside 2 percentage points are `toss-up`.
- If an exact checkpoint observation is unavailable, the notebook MUST apply the
  documented nearest-valid fallback rule consistently and expose the rule in the
  notebook narrative or helper metadata.

## Figure contract

- The notebook MUST export one figure per analytical row to
  `prediction-markets-story/figures/`.
- Each figure MUST show the eventual winner’s market signal and polling-derived
  signal over time.
- Each figure MUST mark the three checkpoint dates clearly.

## Summary table contract

The notebook MUST render a five-row summary table with these columns:

- `race`
- `eventual_winner`
- `market_favored_90d`
- `market_favored_30d`
- `market_favored_eve`
- `polls_favored_90d`
- `polls_favored_30d`
- `polls_favored_eve`
