# Feature Specification: Prediction Markets vs. Polls Story

**Feature Branch**: `001-prediction-markets-polls`  
**Created**: 2026-05-24  
**Status**: Draft  
**Input**: User description: "Data Analysis Brief: Prediction Markets vs. Polls in US Elections (2020, 2022, 2024)"

## Clarifications

### Session 2026-05-24

- Q: How should the notebook select a source observation when no record exists exactly on a checkpoint date? → A: Use the latest observation on or before the checkpoint date.
- Q: For the 2022 House and Senate control rows, what should count as the polling-side signal? → A: Use a chamber-control forecast source for House and Senate instead of raw polling averages.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reproduce the full analysis notebook (Priority: P1)

A data journalist or reviewer can clone the project, run a single notebook from top to bottom, and regenerate the cleaned datasets, summary table, figures, and written findings without any manual setup steps beyond installing dependencies.

**Why this priority**: Reproducibility is the core value of the deliverable. If the notebook cannot be rerun cleanly, the story cannot be verified or reused.

**Independent Test**: Can be fully tested by starting from a clean project checkout, restarting the notebook kernel, running all cells in order, and confirming that all required outputs are recreated with no manual data downloads or path edits.

**Acceptance Scenarios**:

1. **Given** a clean clone of the repository, **When** a reviewer runs the notebook from the first cell to the last, **Then** the notebook completes using only included or automatically downloaded data and produces the expected tables, charts, and processed files.
2. **Given** a project clone on a different machine, **When** the notebook is run with the documented setup steps, **Then** all data paths resolve relative to the project and no hidden local state is required.

---

### User Story 2 - Compare who was favored at fixed checkpoints (Priority: P2)

A reader can see, for each target race, whether prediction markets and polling each favored the eventual winner 90 days before election day, 30 days before election day, and on election eve.

**Why this priority**: The story exists to test a narrow factual claim about directional accuracy, not broader forecasting quality.

**Independent Test**: Can be fully tested by checking the summary table and supporting race-level data to confirm that each checkpoint receives a market and polling judgment of `yes`, `no`, or `toss-up` under the defined rules.

**Acceptance Scenarios**:

1. **Given** a race with aligned market and polling source data, **When** the notebook evaluates the three checkpoints, **Then** it records whether each source favored the eventual winner or not using the defined toss-up thresholds.
2. **Given** a checkpoint where the polling or market signal falls inside the toss-up threshold, **When** the notebook classifies that checkpoint, **Then** the result is labeled `toss-up` rather than forcing a favored side.

---

### User Story 3 - Read a narrative story with race-level context (Priority: P3)

A reader can move through the notebook as a coherent data story, understand the source choices and methodological caveats, and read a short findings summary for each race and for the full set of races together.

**Why this priority**: The deliverable is not only an analysis artifact but a story intended to communicate what happened, what was compared, and what the comparison does and does not show.

**Independent Test**: Can be fully tested by reading the notebook in order and confirming that every major section explains its purpose, each race has its own chart and short summary, and the conclusion stays within the stated scope.

**Acceptance Scenarios**:

1. **Given** a reader who opens the notebook, **When** they follow it from introduction to conclusion, **Then** they encounter clearly labeled sections for question, sources, cleaning, per-race analysis, summary table, and findings.
2. **Given** the final written summary, **When** a reader reviews it, **Then** it stays under 500 words, describes timing and flips where relevant, and avoids claims that extend beyond the specific races analyzed.

---

### Edge Cases

- What happens when a source does not have an observation exactly on the 90-day, 30-day, or election-eve checkpoint date?
- When no exact checkpoint-date observation exists, the notebook uses the latest observation on or before the checkpoint date rather than looking ahead.
- How does the notebook handle races where polling and market series use different units, update frequencies, or date coverage?
- What happens when a source is unavailable locally because the dataset is hosted remotely or exceeds the repository size budget?
- How does the analysis label checkpoints where the margin or implied probability falls within the defined toss-up window?
- How does the story handle cases where a source favored one side earlier in the cycle and flipped later?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST produce a single main notebook that runs top to bottom as a narrative data story rather than an unordered analysis script.
- **FR-002**: The notebook MUST state the core question as a binary favored-side comparison at three checkpoints per race: 90 days before election day, 30 days before election day, and election eve.
- **FR-003**: The notebook MUST cover exactly these analytical rows in its cross-race summary: 2020 presidential election, 2022 House control, 2022 Senate control, 2022 Pennsylvania Senate race, and 2024 presidential election.
- **FR-004**: The notebook MUST identify the eventual winner or winning side for each row and use that outcome as the basis for determining whether markets and polls favored the winner.
- **FR-005**: The notebook MUST use prediction market data from the identified primary source and MUST document the specific source used for each race inline, including the source location.
- **FR-006**: The notebook MUST use polling data from the identified primary source and MUST document the specific polling dataset used for each race inline, including the source location.
- **FR-006a**: For the 2022 House control and 2022 Senate control rows, the notebook MUST use a chamber-control forecast source for the polling-side comparison rather than raw generic-ballot or aggregated race polling, and it MUST document that source inline.
- **FR-007**: The notebook MUST include all data-loading logic needed to obtain source files, whether by reading local files in the repository or downloading remote files on first run without manual intervention.
- **FR-008**: The project MUST include the folder structure `prediction-markets-story/` with a main notebook, `data/raw/`, `data/processed/`, `figures/`, and `README.md`.
- **FR-009**: The notebook MUST save cleaned per-race files in `data/processed/`, with one file per analytical row and with the fields `date`, `market_prob_winner`, `market_prob_loser`, `poll_value_winner`, `poll_value_loser`, `source_market`, and `source_poll`.
- **FR-010**: The cleaned per-race files MUST represent the finest practical regular time interval available from the source data, using daily resolution where available and weekly resolution otherwise.
- **FR-011**: The notebook MUST define election eve as the day before election day and MUST use that definition consistently in all tables, charts, and summaries.
- **FR-011a**: When no source observation exists exactly on a checkpoint date, the notebook MUST use the latest available observation on or before that checkpoint date for classification.
- **FR-012**: The notebook MUST classify each checkpoint for both markets and polls as `yes`, `no`, or `toss-up`, where `toss-up` means either a market probability inside 48 to 52 or a polling margin inside 2 percentage points.
- **FR-013**: The notebook MUST explain why the comparison is not apples to apples, specifically that polls measure vote share while markets reflect win expectations, and MUST explain the chosen comparison method.
- **FR-014**: The notebook MUST avoid presenting raw poll averages as win probabilities unless it explicitly relies on a forecast source designed for that purpose.
- **FR-014a**: The notebook MUST treat the 2022 House control and 2022 Senate control rows as forecast-versus-market comparisons on the non-market side and MUST explain why this differs from the candidate-race polling treatment.
- **FR-015**: The notebook MUST produce one chart per analytical row in `figures/`, showing the eventual winner’s market signal over time and the polling-derived signal over time with the three checkpoints clearly marked.
- **FR-016**: Each race section in the notebook MUST include a short written finding that summarizes whether markets and polls favored the eventual winner at the three checkpoints and notes any meaningful timing differences.
- **FR-017**: The notebook MUST render a five-row summary table with the columns `race`, `eventual_winner`, `market_favored_90d`, `market_favored_30d`, `market_favored_eve`, `polls_favored_90d`, `polls_favored_30d`, and `polls_favored_eve`.
- **FR-018**: The final written summary in the notebook MUST remain under 500 words and MUST describe only what happened in these selected races rather than making general statistical claims about prediction markets overall.
- **FR-019**: The final written summary MUST note, as contextual caveat, that 2024 presidential market pricing on Polymarket was influenced by a small number of large traders.
- **FR-020**: The notebook MUST include section-opening explanations, non-trivial function docstrings, and inline comments that explain reasoning choices rather than restating code actions.
- **FR-021**: The project README MUST provide a short description of the story and tell a reviewer how to run the notebook end to end.

### Key Entities *(include if feature involves data)*

- **Analytical Row**: One race or chamber-control question in the final comparison table, defined by election year, contest type, eventual winner, election date, and source references.
- **Checkpoint Evaluation**: A dated judgment for one source type at one checkpoint indicating whether the eventual winner was favored, not favored, or in toss-up range.
- **Race Time Series Record**: A cleaned observation for one race and date containing market values, polling values, and source provenance fields used for downstream charts and summaries.
- **Source Asset**: A raw local or remotely downloaded file used in the analysis, identified by source type, location, and role in the notebook.
- **Figure Output**: A saved race-specific chart that visualizes the eventual winner’s market and polling signals over time and highlights the three checkpoints.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reviewer can run the notebook from a clean clone with no manual data placement, path editing, or hidden preparatory steps.
- **SC-002**: The notebook produces five cleaned per-race files, five race charts, and one five-row summary table every time it is run successfully.
- **SC-003**: Every analytical row contains completed `yes`, `no`, or `toss-up` classifications for both markets and polls at all three checkpoints, unless the notebook explicitly documents missing source coverage.
- **SC-004**: Every race section includes a readable written takeaway, and the notebook conclusion stays under 500 words while covering methodology limits and timing observations.
- **SC-005**: A reviewer can trace every chart and checkpoint judgment back to an inline-documented source dataset and source location from within the notebook itself.

## Assumptions

- The deliverable focuses on the specific races named in the brief and does not expand to additional elections or broader forecast-evaluation questions in this pass.
- The favored-side comparison is the authoritative method for comparing polls and markets unless a forecast source designed to express win probability is explicitly introduced and documented.
- Chamber-control rows use a forecast source on the non-market side because chamber control is not directly observed through a single raw polling average in the same way as candidate races.
- Local inclusion of raw files is preferred when the total repository footprint remains small enough; otherwise, remote download during notebook execution is acceptable as long as it is automated and reproducible.
- A race-level chart may use different visual encodings for market and polling signals as long as the chart makes checkpoint comparisons interpretable for a reader.
- The notebook may rely on the nearest valid source observation to each checkpoint when an exact same-day record is unavailable, provided the method is explained clearly.
- Checkpoint classification uses the latest available source observation on or before the checkpoint date when an exact same-day record is unavailable.
