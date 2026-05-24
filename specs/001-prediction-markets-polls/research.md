# Research: Prediction Markets vs. Polls Story

## Decision 1: Use a notebook-first Python workflow with a minimal dependency set

- **Decision**: Implement the deliverable as a single Jupyter notebook backed by
  `pandas`, `numpy`, `plotly`, `requests`, and the standard library.
- **Rationale**: The feature is a narrative data story with reproducibility as
  the primary requirement. A notebook is the final artifact, and these
  dependencies cover data loading, cleaning, charting, and HTTP downloads
  without introducing a larger application framework.
- **Alternatives considered**:
  - A script-plus-notebook split: rejected because it adds coordination overhead
    for a small project and weakens the "single reproducible notebook"
    requirement.
  - `matplotlib` only: rejected as the primary plan because interactive charts
    are more portable for downstream story embedding, though static exports can
    still be produced from Plotly.
  - Additional workflow tooling such as Airflow or dbt: rejected as unnecessary
    for a five-race notebook story.

## Decision 2: Store raw source files locally when small, otherwise download on first run

- **Decision**: Prefer checked-in raw CSV files when the total footprint remains
  below the repository size budget; otherwise, implement deterministic download
  helpers in the notebook and cache the downloaded files under `data/raw/`.
- **Rationale**: This satisfies the reproducibility-first principle while
  keeping the repo portable. The notebook remains self-contained either way
  because all acquisition logic lives in the notebook.
- **Alternatives considered**:
  - Always commit all raw files: rejected because some source extracts may push
    the repository beyond the stated size budget.
  - Always download remotely: rejected because local inclusion is simpler when
    feasible and reduces external points of failure.

## Decision 3: Compare favored side instead of converting polls into win probabilities

- **Decision**: Treat checkpoint judgments as directional classifications based
  on who leads the market and who leads the polling signal, with explicit
  toss-up rules.
- **Rationale**: The spec requires a binary favored-side comparison and
  explicitly warns that polling averages and market probabilities are not the
  same object. A directional comparison preserves methodological honesty.
- **Alternatives considered**:
  - Convert polling margins to synthetic win probabilities: rejected because it
    would imply a model not present in the underlying source.
  - Use only forecast probabilities: rejected because the brief names polling
    averages as the primary polling source and the story is about markets vs.
    polls, not markets vs. forecasters.

## Decision 4: Use nearest-valid checkpoint observations with documented fallback rules

- **Decision**: For each race and source, evaluate 90-day, 30-day, and
  election-eve checkpoints using the nearest valid observation on or before the
  checkpoint date; if unavailable, fall back to the nearest subsequent
  observation and record that fallback in the notebook narrative or provenance.
- **Rationale**: Historical daily and weekly source coverage will not always
  align exactly with checkpoint dates. A deterministic fallback rule is required
  by the constitution and avoids ad hoc interpolation.
- **Alternatives considered**:
  - Require exact same-day observations: rejected because it would create
    avoidable missing classifications.
  - Linearly interpolate market or polling values: rejected because it adds
    synthetic observations that the story does not need.

## Decision 5: Treat the notebook execution contract as the primary verification method

- **Decision**: Validate reproducibility by executing the notebook end to end
  from a clean environment using an automated notebook runner and by checking
  for the required output files.
- **Rationale**: The user-facing artifact is the notebook itself, so successful
  top-to-bottom execution is the strongest practical verification of the
  deliverable.
- **Alternatives considered**:
  - Only inspect outputs manually: rejected because it does not prove
    reproducibility.
  - Build a full unit-test suite around every helper: rejected for the first
    pass because end-to-end notebook execution provides higher value for this
    artifact, though targeted tests can be added later if helper complexity
    grows.

## Decision 6: Expose explicit file-level contracts for outputs and provenance

- **Decision**: Document a contract for processed per-race CSVs, summary-table
  fields, figure outputs, and notebook download/cache behavior in a dedicated
  contracts document.
- **Rationale**: The project has no API, but it does expose reproducible data
  products that downstream reviewers must be able to inspect and trust.
- **Alternatives considered**:
  - Skip contracts entirely because the project is notebook-based: rejected
    because output-file expectations are central to the feature requirements.
